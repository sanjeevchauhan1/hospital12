from odoo import models, fields, api

class CreateAppointment(models.TransientModel):
    _name='create.appointment'

    @api.depends('name')
    def _add(self):
        prd_ids = self.env['doctor.patient'].browse(self._context.get('active_ids'))
        for res in prd_ids:
            vals={
                'name':prd_ids.name,
            }
        return prd_ids.name
    #
    # @api.depends('doctor_gender')
    # def _add_gender(self):
    #     prd_ids = self.env['doctor.patient'].browse(self._context.get('active_ids'))
    #     for res in prd_ids:
    #         vals = {
    #             'doctor_gender': prd_ids.doctor_gender,
    #
    #         }
    #     return prd_ids.doctor_gender

    name = fields.Char(string='Patient')

    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Doctor Gender")


    def update_record(self):
        active_id = self._context.get('active_id')
        record_to_update = self.env['doctor.patient'].browse(active_id)
        if record_to_update.exists():
            vals = {
                'name': self.name,
                'doctor_gender': self.doctor_gender,
            }
            record_to_update.write(vals)






