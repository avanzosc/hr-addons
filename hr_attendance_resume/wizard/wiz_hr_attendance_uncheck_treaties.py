# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizHrAttendanceUncheckTreaties(models.TransientModel):
    _name = "wiz.hr.attendance.uncheck.treaties"
    _description = "Wizard for uncheck attendances treaties"

    @api.multi
    def button_uncheck(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        attendances = self.env['hr.attendance'].browse(active_ids)
        if attendances:
            attendances.write({'treated': False})
            self._delete_employees_resumes(attendances)
        return {'type': 'ir.actions.act_window_close'}

    def _delete_employees_resumes(self, attendances):
        cond = [('id', 'in', attendances.mapped('employee_id').ids),
                ('resource_calendar_id', '!=', False)]
        employees = self.env['hr.employee'].search(cond)
        for employee in employees:
            emp_attendances = attendances.filtered(
                lambda c: c.employee_id.id == employee.id and
                c.check_out and not c.treated)
            if emp_attendances:
                emp_attendances._delete_employee_attendance_resumes()
