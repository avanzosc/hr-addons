# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def automatic_congratulate_employee_birthday(self):
        today = fields.Date.from_string(fields.Date.today())
        cond = [('birthday', '!=', False)]
        employees = self.env['hr.employee'].search(cond).filtered(
            lambda c: fields.Date.from_string(c.birthday).day ==
            today.day and fields.Date.from_string(c.birthday).month ==
            today.month)
        for employee in employees:
            contract = employee.mapped('contract_ids').filtered(
                lambda l: not l.date_end or l.date_end >= fields.Date.today())
            if contract:
                contract.employee_id.send_email_for_congratule_birthday()

    @api.multi
    def send_email_for_congratule_birthday(self):
        template = self.env.ref(
            'hr_automatic_congratulate_birthday.email_for_congratulate_employe'
            'e_birthday', False)
        if template:
            mail = self.env['mail.compose.message'].with_context(
                default_composition_mode='mass_mail',
                default_template_id=template.id,
                default_use_template=True,
                default_partner_ids=[(6, 0, self.address_home_id.ids)],
                active_id=self.id,
                active_ids=self.ids,
                active_model='hr.employee',
                default_model='hr.employee',
                default_res_id=self.id,
                force_send=True
            ).create({'subject': template.subject,
                      'body': template.body_html})
            mail.send_mail()
