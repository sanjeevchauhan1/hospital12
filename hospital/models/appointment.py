from odoo import fields, models, api, _
import datetime
from odoo.exceptions import UserError

class AppointmentPatient(models.Model):
    _name='appointment.patient'
    _rec_name='Patient_Name'


    app_ment = fields.Char(string='ref_order', required=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))

    choice = fields.Boolean(string='Check')
    Patient_Name = fields.Char(string='Patient_Name')
    doctor_id = fields.Many2one('doctor.patient', string='Doctor')
    doctor_ids = fields.Many2many('doctor.patient', string='Doctor_ids')
    dob = fields.Date(string='Dob')
    Gender = fields.Selection([('Male','Male'),('female','female')])
    phone_no = fields.Char(string='Phone_No')

    appointment_lines = fields.One2many('hospital.appointment.lines','appointment_id',string='appointment_lines')
    Already_register = fields.Selection([('New','New'),('Exists','Exists')],string="Already_Register")
    purpose = fields.Char(string='Purpose')
    address = fields.Char(string='Address')
    problem = fields.Selection([('Heart','Heart'),('Fever','Fever'),('Dental','Dental')])
    # age = fields.Integer(string='Age')
    age = fields.Integer(string='Age',compute='_get_age_from_stu')
    remarks = fields.Text(string='Remarks')
    remarks2 = fields.Text(string='Remarks2')





    #dob change
    @api.depends('dob')
    def _get_age_from_stu(self):
        today_date=datetime.date.today()
        for stu in self:
            if stu.dob:
                dob=fields.Datetime.to_datetime(stu.dob).date()
                Age=str(int((today_date-dob).days/365))
                stu.age=Age
            else:
                stu.age=0


    @api.depends('age')
    def set_age_group(self):
        for rec in self:
            if rec.age <=5:
                rec.age_group ='bi'
            elif rec.age <=18:
                rec.age_group ='chi'
            else:
                rec.age_group ='gen'


    age_group = fields.Selection([('bi','baby'),('chi','child'),('gen','General')],string='Age group', compute='set_age_group')



    @api.model
    def create(self,vals):
        if vals.get('app_ment', _('New')) == _('New'):
            vals['app_ment'] = self.env['ir.sequence'].next_by_code('appointment.patient.sequence') or _('New')
        result = super(AppointmentPatient, self).create(vals)
        return result

    @api.multi
    def open_patient_appointments(self):
        return{
            'name': _('Appointment'),
            'domain':[],
            'view_type': 'form',
            'res_model': 'doctor.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    @api.model
    def create(self,vals):

        vals['remarks']='created appoinment'
        res = super(AppointmentPatient, self).create(vals)
        return res


    @api.multi
    def write(self,vals):
        vals['remarks'] = 'record edited'
        res = super(AppointmentPatient, self).write(vals)
        return res





    #unlink condition
    @api.depends('age')
    def unlink(self):
        for rec in self:
            if rec.age < 25:
               raise UserError("You can not delete this record")
        return super(AppointmentPatient, self).unlink()















class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description ='appointment lines'
    # product_id = fields.Many2one('doctor.patient',string='string')
    # product_qty = fields.Integer(string='quantity')
    appointment_id = fields.Many2one('appointment.patient',string='appointment id')
    medicine = fields.Many2one('store.medicin', string='medicine')
    timing = fields.Datetime(string='timing')
    next_appointment = fields.Date(string='next_appointment')