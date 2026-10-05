from odoo import fields, models


class Guest(models.Model):
    _name = 'thimo.guest'
    _description = 'Guest'
    _order = 'name'

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    id_number = fields.Char(string='ID / Passport')
    notes = fields.Text()
    active = fields.Boolean(default=True)
