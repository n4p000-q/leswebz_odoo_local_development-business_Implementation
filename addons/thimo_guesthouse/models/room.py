from odoo import fields, models


class Room(models.Model):
    _name = 'thimo.room'
    _description = 'Guest House Room'
    _order = 'name'

    name = fields.Char(string='Room Number', required=True)
    room_type_id = fields.Many2one('thimo.room.type', required=True, ondelete='restrict')
    floor = fields.Char()
    state = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ], default='available', required=True)
    notes = fields.Text()
