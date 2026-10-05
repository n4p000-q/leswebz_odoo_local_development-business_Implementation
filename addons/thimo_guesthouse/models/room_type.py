from odoo import fields, models


class RoomType(models.Model):
    _name = 'thimo.room.type'
    _description = 'Room Type'
    _order = 'name'

    name = fields.Char(required=True)
    description = fields.Text()
    capacity = fields.Integer(default=2)
