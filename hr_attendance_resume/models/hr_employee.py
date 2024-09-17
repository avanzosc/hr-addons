# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_resume_ids = fields.One2many(
        comodel_name='hr.attendance.resume',
        inverse_name='employee_id', string='Imputations resumes')
    count_attendances_resumes = fields.Integer(
        string='Attendances resume', store=True,
        compute='_compute_count_attendances_resumes')

    @api.multi
    @api.depends('attendance_resume_ids')
    def _compute_count_attendances_resumes(self):
        for employee in self:
            employee.count_attendances_resumes = (
                len(employee.attendance_resume_ids))

    def _get_employee_calendar(self, date):
        calendar = self.resource_calendar_id
        if self.calendar_ids:
            esp_calendar = self.calendar_ids.filtered(
                lambda c: (not c.date_start or
                           (c.date_start and c.date_start <= date)) and
                (not c.date_end or (c.date_end and c.date_end >= date)))
            if esp_calendar and len(esp_calendar) == 1:
                calendar = esp_calendar.calendar_id
        return calendar

    def _regenerate_calendar(self):
        self.ensure_one()
        return True

    @api.multi
    def button_show_attendance_resumes(self):
        self.ensure_one()
        self = self.with_context(
            search_default_employee_id=self.id, default_employee_id=self.id)
        action = self.env.ref(
            'hr_attendance_resume.action_hr_attendance_resume')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update(
            {'search_default_employee_id': self.id,
             'default_employee_id': self.id})
        domain = expression.AND([
            [('employee_id', '=', self.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
