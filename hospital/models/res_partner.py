from odoo import models, fields, api,_

class ResPartner(models.Model):
    _inherit = 'res.partner'


    # name=fields.Char('Nmae')



    # @api.onchange('app_ment')
    # def onchange_is_customer(self):
    #     for rec in self:
    #         # print(rec.is_customer, '.....................')
    #         return {'domain': {'app_ment': [('category_id', '=', rec.app_ment)]}}
    #
    #
    app_ment = fields.Char(string='ref_order', required=True, copy=False, readonly=True, index=False,
                           default=lambda self: _('New'))
    #
    #
    #
    # @api.model
    # def create(self, vals):
    #     stu=self.env['res.partner'].search([('category_id','=','Vendor')])
    #     if vals.get('app_ment', _('New')) == _('New'):
    #         vals['app_ment'] = self.env['ir.sequence'].next_by_code('res.partner.sequence') or _('New')
    #     result = super(ResPartner, self).create(vals)
    #     print(result,"_____________________________")
    #     return result







