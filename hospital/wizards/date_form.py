from odoo import models, fields, api

class DateForm(models.TransientModel):
    _name='date.form'

    date_from=fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")







