from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale



class Hospital(http.Controller):

    # Sample Controller Created
    @http.route('/patient_webform', website=True,type="http",auth="public")
    def hospital_patient(self, **kw):
        # return "Thanks for watching"
        doctor_rec = request.env['doctor.patient'].sudo().search([])
        print('executed...........',doctor_rec)
        return request.render("hospital.create_patient",{'doc_name':doctor_rec})


    @http.route('/create/webpatient', website=True, type="http", auth="public")
    def create_webpatient(self, **kw):
        # return "Thanks for watching"
        print('executed...........',kw)
        request.env['hospital.patient'].sudo().create(kw)
        return request.render("hospital.patient_thanks", {})
