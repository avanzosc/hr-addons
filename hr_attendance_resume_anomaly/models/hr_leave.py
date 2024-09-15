# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, exceptions, _


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.multi
    def action_approve(self):
        anomaly_with_leave = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_with_leave')
        result = super(HrLeave, self).action_approve()
        if 'from_resume' not in self.env.context:
            for leave in self.filtered(
                    lambda c: c.leave_type_request_unit != 'hour'):
                cond = [('employee_id', '=', leave.employee_id.id),
                        ('imputation_date', '>=', leave.request_date_from),
                        ('imputation_date', '<=', leave.request_date_to)]
                attendances = self.env['hr.attendance'].search(cond)
                if attendances:
                    attendances.write({'treated': False})
                    attendances._impute_in_attendance_resume()
        else:
            cond = [('employee_id', '=',
                     self.env.context.get('default_employee_id')),
                    ('date', '=', self.env.context.get('request_date'))]
            resume = self.env['hr.attendance.resume'].search(cond, limit=1)
            for leave in self.filtered(
                    lambda c: c.leave_type_request_unit != 'hour'):
                if leave.request_date_from != leave.request_date_to:
                    raise exceptions.Warning(
                        _('You cannot approve an attendance from resume with '
                          'different days.'))
                anomalies = resume.attendance_anomaly_ids
                if anomaly_with_leave not in anomalies:
                    anomalies += anomaly_with_leave
                    resume.attendance_anomaly_ids = [(6, 0, anomalies.ids)]
        return result

    @api.multi
    def action_refuse(self):
        result = super(HrLeave, self).action_refuse()
        for leave in self.filtered(
                lambda c: c.leave_type_request_unit != 'hour'):
            cond = [('employee_id', '=', leave.employee_id.id),
                    ('imputation_date', '>=', leave.request_date_from),
                    ('imputation_date', '<=', leave.request_date_to)]
            attendances = self.env['hr.attendance'].search(cond)
            if attendances:
                attendances.write({'treated': False})
                attendances._impute_in_attendance_resume()
        return result
