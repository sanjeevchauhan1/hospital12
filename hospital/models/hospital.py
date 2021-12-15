from odoo import models, fields, api, _

class HospitalPatient(models.Model):  # Always use class name in Camelcase.
    _name = 'hospital.patient'  # Object name should be in single quotes.





    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    patient_name = fields.Char(string='Patient Name')
    doc_name = fields.Many2one('doctor.patient',string='Doctor Name')
    patient_dob = fields.Date(string='Date of Birth')
    patient_age = fields.Integer(string='Age')
    patient_email = fields.Char(string='E-mail ID')
    mobile_no = fields.Char(string='Mobile')
    gender = fields.Selection([('male', 'Male'),
                                       ('female', 'Female'),
                                       ('others', 'Others')
                                       ], string='Gender')
    appoint_date = fields.Date(string='appoint_date')
    start = fields.Date(string='start')
    end = fields.Date(string='end')

    @api.onchange('is_customer')
    def onchange_is_customer(self):
        for rec in self:
            print(rec.is_customer, '.....................')
            return {'domain': {'partner_id': [('category_id', '=', rec.is_customer)]}}

    # brand_id = fields.Char(string="Brands", required=True)

    is_customer = fields.Selection([('Customers', 'Customers'), ('Vendor', 'Vendor'), ('other', 'other')])
    partner_id = fields.Many2one('res.partner', string="Partner id")

    @api.model
    def create(self,vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result= super(HospitalPatient,self).create(vals)
        return result


    # def action_conform(self):
    #     for rec in self:
    #         patients=self.env['hospital.patient'].search([])
    #         print('pateinrsssssss',patients)











    # Sale Order Inherit
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')
    doctor_name = fields.Char(string='Doctor Name')
    reference_name = fields.Char(string='Reference Name')
    age = fields.Integer(string='Age')



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    owner_name = fields.Char(string='Owner name')
    mobile_no = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    # age = fields.Integer(string='Age')





