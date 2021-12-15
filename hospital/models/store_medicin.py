from odoo import models, fields, api, _


class StoreMedicin(models.Model):
    _name='store.medicin'

    name = fields.Char(string='Sequence_ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('new'))
    img = fields.Binary(string="Image")


    medicin_name = fields.Char(string='Medicin_Name')
    price = fields.Float(string='Price')
    stationery_line = fields.One2many('medicin.lines','medicin_id',string='Stationery_Line')
    xls_file = fields.Binary('File')

    # @api.multi
    # def import_xls(self):
    #     wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
    #     for sheet in wb.sheets():
    #         for row in range(sheet.nrows):
    #             item = self.env['store.medicin'].search([('book_name', '=', sheet.cell(row, 0).value)])
    #             print('item=', item)
    #             self.stationery_line = [
    #                 # (0, 0, {'item_name': item.book_name}), # Here you'll get both fields in different row.
    #                 # (0, 1, {'item_no': item.price})
    #                 {'item_name': item.book_name, 'item_no': item.price}  # Here you'll get both fields in same row.
    #             ]
    @api.model
    def create(self, vals):
        if vals.get('name',_('new')==_('new')):
            vals['name']=self.env['ir.sequence'].next_by_code('store.medicin.sequence') or ('new')
        result=super(StoreMedicin,self).create(vals)
        return result






class MedicinLines(models.Model):
    _name ='medicin.lines'

    item_name = fields.Char(string='Item_Name')
    item_no = fields.Char(string='item_no')
    medicin_id = fields.Many2one('store.medicin',string='Medicin')


