from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Booking(models.Model):
    _name = 'thimo.booking'
    _description = 'Guest House Booking'
    _order = 'check_in_date desc, id desc'

    name = fields.Char(string='Booking Reference', required=True, copy=False, default='New')
    guest_id = fields.Many2one('thimo.guest', required=True, ondelete='restrict')
    room_id = fields.Many2one('thimo.room', required=True, ondelete='restrict')
    room_type_id = fields.Many2one(related='room_id.room_type_id', store=True, readonly=True)
    rate_id = fields.Many2one('thimo.rate', ondelete='restrict')
    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    nights = fields.Integer(compute='_compute_nights', store=True)
    price_per_night = fields.Float(compute='_compute_price', store=True)
    total_amount = fields.Float(compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], default='draft', required=True)
    notes = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('thimo.booking') or 'New'
        return super().create(vals_list)

    @api.depends('check_in_date', 'check_out_date')
    def _compute_nights(self):
        for rec in self:
            if rec.check_in_date and rec.check_out_date:
                rec.nights = max((rec.check_out_date - rec.check_in_date).days, 0)
            else:
                rec.nights = 0

    @api.depends('rate_id', 'rate_id.price')
    def _compute_price(self):
        for rec in self:
            rec.price_per_night = rec.rate_id.price if rec.rate_id else 0.0

    @api.depends('nights', 'price_per_night')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = rec.nights * rec.price_per_night

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for rec in self:
            if rec.check_in_date and rec.check_out_date and rec.check_out_date <= rec.check_in_date:
                raise ValidationError('Check-out date must be after check-in date.')

    @api.constrains('room_id', 'check_in_date', 'check_out_date', 'state')
    def _check_room_overlap(self):
        for rec in self:
            if rec.state in ('cancelled', 'checked_out') or not rec.room_id:
                continue
            overlap = self.search([
                ('id', '!=', rec.id),
                ('room_id', '=', rec.room_id.id),
                ('state', 'in', ('confirmed', 'checked_in')),
                ('check_in_date', '<', rec.check_out_date),
                ('check_out_date', '>', rec.check_in_date),
            ], limit=1)
            if overlap:
                raise ValidationError('This room is already booked for an overlapping date range.')

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                continue
            if rec.room_id.state not in ('available', 'reserved'):
                raise UserError('The selected room is not available for booking.')
            rec.state = 'confirmed'
            rec.room_id.state = 'reserved'
        return True

    def action_check_in(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError('Only confirmed bookings can be checked in.')
            rec.state = 'checked_in'
            rec.room_id.state = 'occupied'
        return True

    def action_check_out(self):
        for rec in self:
            if rec.state != 'checked_in':
                raise UserError('Only checked-in bookings can be checked out.')
            rec.state = 'checked_out'
            rec.room_id.state = 'available'
        return True

    def action_cancel(self):
        for rec in self:
            if rec.state == 'checked_in':
                raise UserError('Check out the guest before cancelling the booking.')
            if rec.state in ('confirmed', 'draft'):
                rec.room_id.state = 'available'
            rec.state = 'cancelled'
        return True
