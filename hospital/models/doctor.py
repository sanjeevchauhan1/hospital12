import base64
from datetime import datetime
from io import BytesIO
import xlwt
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
class DoctorPatient(models.Model):
    _name='doctor.patient'
    _rec_name = 'name'

    datas_fname = fields.Char('File Name', size=256)

# reports excel card
    @api.multi
    def report_print(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet("sanjeev", cell_overwrite_ok=True)
        xlwt.add_palette_colour("custom_colour_or", 0x21)
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        filename = 'sanjeev Excel'
        # for style =====================================================================>
        style = xlwt.easyxf('font: bold 1, color red;align: horiz centre;')
        style1 = xlwt.easyxf('font: bold 1; align: horiz centre;')
        style_green_li = xlwt.easyxf('align: horiz centre; align: vert centre; font: colour black, bold True; '
                                     'borders: top_color black, bottom_color black, right_color black, left_color black,\
                                       left thin, right thin, top thin, bottom thin;\
                                     pattern: pattern solid, fore_color 0x11;')

        # all data sheet

        # Excel report

        patient_obj = self.env['doctor.patient'].search([])
        row = 2
        for rec in patient_obj:
            sheet.write(row, 0, rec.doc_seq, style1)
            sheet.write(row, 1, rec.name, style1)
            sheet.write(row, 2, rec.specilist, style1)
            sheet.write(row, 3, rec.qualified, style1)
            sheet.write(row, 5, rec.age, style1)
            sheet.write(row, 4, rec.doctor_gender, style1)
            row = row + 1
        # for line in self.patient_lines:
        #     print('patient_obj.patient_lines', patient_obj.patient_lines)
        #     sheet.write(row, 6, line.product_qty, style1)
        #     sheet.write(row, 7, line.product_qty, style1)
        #     row += 1
        fp = BytesIO()
        workbook.save(fp)
        out = base64.encodebytes(fp.getvalue())  # file name for download file
        view_report_status_id = self.env['view.xls.report'].create({'file_name': out, 'datas_fname': filename})
        return {
            'res_id': view_report_status_id.id,
            'name': 'GSTR-3b',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'view.xls.report',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }



        # DND
        xlwt.add_palette_colour("custom_colour_or", 0x21)
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        filename = 'test.xls'
        fp = BytesIO()
        wb.save(fp)
        out = base64.encodebytes(fp.getvalue())
        view_report_status_id = self.env['view.xls.report'].create({'file_name': out, 'datas_fname': filename})
        return {
            'res_id': view_report_status_id.id,
            'name': 'GSTR-3b',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'view.xls.report',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }




    doc_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))

    name = fields.Char(string='Name',required=True)
    doc_email = fields.Char(string="Doc_email")
    specilist = fields.Char(string='Specilist')
    qualified = fields.Char(string='Qualified')
    age = fields.Integer(string='age')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Doctor Gender")

    file_doc=fields.Binary(string="Report",attachment=True)






    @api.model
    def create(self, vals):
        if vals.get('doc_seq', _('New')) == _('New'):
            vals['doc_seq'] = self.env['ir.sequence'].next_by_code('doctor.patient.sequence') or _('New')
        result = super(DoctorPatient, self).create(vals)
        return result

    def action_send_card(self):
        print("sending mail__________________________________________")
        template_id = self.env.ref('hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

        # <!--attachment binary file-->

        ir_model_data = self.env['ir.model.data']
        ir_mail_server = self.env['ir.mail_server']
        mail_server_ids = ir_mail_server.sudo().search([], order='sequence', limit=1)
        mail = False
        if mail_server_ids:
            mail = mail_server_ids[0]
        template_id = ir_model_data.get_object_reference('hospital', 'patient_card_email_template')[1]
        if template_id:
            email_from = mail.smtp_user
            attachment = self.env['ir.attachment'].create({'name': 'filename.xlsx',
                                                           'datas_fname': 'filename.xlx',
                                                           'datas': self.file_doc})
            template = self.env['mail.template'].browse(template_id)
            template.attachment_ids = [(6, 0, [attachment.id])]
            template.send_mail(self.id, force_send=True, email_values={'email_from': email_from})

            # <!--end code-->



class view_xls_report(models.TransientModel):
    _name = 'view.xls.report'
    _rec_name = 'datas_fname'
    datas_fname = fields.Char('File Name', size=256)
    file_name = fields.Binary('Report')
