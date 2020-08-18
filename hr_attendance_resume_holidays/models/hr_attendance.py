# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from .._common import _catch_dayofweek


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def _impute_employee_attendances_day(self):
        resume = super(HrAttendance, self)._impute_employee_attendances_day()
        cond = [('employee_id', '=', resume.employee_id.id),
                ('request_date_from', '<=', resume.date),
                ('request_date_to', '>=', resume.date),
                ('state', '=', 'validate')]
        leave = self.env['hr.leave'].search(cond, limit=1)
        if leave:
            vals = {'leave_id': leave.id}
            resume.write(vals)
        return resume

    def _impute_employee_attendances(self):
        resume_obj = self.env['hr.attendance.resume']
        result = super(HrAttendance, self)._impute_employee_attendances()
        if not self:
            return result
        with_imputation_date = self.filtered(
                lambda x: x.imputation_date)
        if not with_imputation_date:
            return result
        min_fec = min(with_imputation_date, key=lambda x: x.imputation_date)
        date_from = min_fec.imputation_date
        max_fec = max(with_imputation_date, key=lambda x: x.imputation_date)
        date_to = max_fec.imputation_date
        employee = min_fec.employee_id
        cond = [('employee_id', '=', employee.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('created_from_holidays', '=', True)]
        resumes = resume_obj.search(cond)
        if resumes:
            resumes.unlink()
        while date_from <= date_to:
            cond = [('employee_id', '=', employee.id),
                    ('date', '=', date_from)]
            resume = resume_obj.search(cond, limit=1)
            if not resume:
                leave = self._search_no_imputed_holidays(employee, date_from)
                if leave:
                    self._create_resume_from_no_imputed_holidays(
                        leave, employee, date_from)
            date_from = (date_from + relativedelta(days=1))
        return result

    def _search_no_imputed_holidays(self, employee, date):
        cond = [('employee_id', '=', employee.id),
                ('request_date_from', '<=', date),
                ('request_date_to', '>=', date),
                ('state', '=', 'validate')]
        leave = self.env['hr.leave'].search(cond, limit=1)
        return leave

    def _create_resume_from_no_imputed_holidays(self, leave, employee, date):
        calendar = employee._get_employee_calendar(date=date)
        work_time, hour_from, hour_to = employee._get_day_info(
            calendar, date)
        if work_time == 0.0:
            return False
        vals = {'employee_id': employee.id,
                'date': date,
                'leave_id': leave.id,
                'created_from_holidays': True,
                'theoretical_time': work_time,
                'day_week_literal': _catch_dayofweek(date)}
        return self.env['hr.attendance.resume'].create(vals)


class HrAttendanceResume(models.Model):
    _inherit = 'hr.attendance.resume'

    leave_id = fields.Many2one(
        string='Leave', comodel_name='hr.leave')
    holiday_status_id = fields.Many2one(
        string='Leave type', comodel_name='hr.leave.type',
        related='leave_id.holiday_status_id', store=True)
    theoretical_time_final = fields.Float(
        string='Theoretical time', compute='_compute_theoretical_time_final',
        store=True)
    holiday_hours = fields.Float(
        string='Holiday hours', compute='_compute_theoretical_time_final',
        store=True)
    created_from_holidays = fields.Boolean(
        string='Created from holidays', default=False)

    @api.depends('theoretical_time', 'leave_id')
    def _compute_theoretical_time_final(self):
        for record in self:
            record.theoretical_time_final = record.theoretical_time
            record.holiday_hours = 0
            if record.leave_id:
                if (round(record.theoretical_time, 2) ==
                        round(record.leave_id.hours_per_day, 2)):
                    record.theoretical_time_final = 0.0
                else:
                    record.theoretical_time_final = (
                        record.theoretical_time -
                        record.leave_id.hours_per_day)
                if record.theoretical_time:
                    record.holiday_hours = record.leave_id.hours_per_day
                else:
                    record.holiday_hours = record.theoretical_time

    @api.depends('theoretical_time_final', 'presence_time', 'bonus_hours',
                 'rest_exceeded')
    def _compute_imputable_diference(self):
        for record in self:
            record.imputable_time = (
                record.presence_time + record.bonus_hours -
                record.rest_exceeded)
            difference_hours = (
                record.imputable_time - record.theoretical_time_final)
            if difference_hours != 0:
                record.difference_hours = difference_hours
                record.difference_minutes = round(difference_hours * 60)
