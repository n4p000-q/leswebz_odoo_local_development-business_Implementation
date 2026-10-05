from odoo import fields, models


class Rate(models.Model):
    _name = 'thimo.rate'
    _description = 'Room Rate'
    _order = 'room_type_id, date_from'

    name = fields.Char(required=True)
    room_type_id = fields.Many2one('thimo.room.type', required=True, ondelete='cascade')
    date_from = fields.Date(required=True)
    date_to = fields.Date()
    price = fields.Float(string='Price per Night', required=True)
