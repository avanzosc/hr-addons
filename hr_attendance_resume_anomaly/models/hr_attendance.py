# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from .._common import _catch_dayofweek
from dateutil.relativedelta import relativedelta


class HrAttendanceResumeAnomaly(models.Model):
    _name = 'hr.attendance.resume.anomaly'
    _description = 'Attendances resumes anomalies'

    name = fields.Char(string='Anomaly', required=True, translate=True)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def _impute_employee_attendances(self):
        result = super(HrAttendance, self)._impute_employee_attendances()
        without_calendar = self.filtered(lambda c: not c.imputation_date)
        if without_calendar:
            dates = set(without_calendar.mapped('check_in_without_hour'))
            for date in dates:
                attendances = without_calendar.filtered(
                    lambda c: c.check_in_without_hour == date)
                attendances._impute_employee_attendances_without_day(date)
        self.treat_without_signings_in_the_day()
        return result

    def treat_without_signings_in_the_day(self):
        festive_obj = self.env['hr.holidays.public.line']
        anomaly = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_no_'
            'attendance')
        resume_obj = self.env['hr.attendance.resume']
        min_check_in = min(self, key=lambda x: x.check_in)
        min_date = min_check_in.check_in_without_hour
        if (min_check_in.imputation_date and
                min_check_in.imputation_date < min_date):
            min_date = min_check_in.imputation_date
        max_check_in = max(self, key=lambda x: x.check_in)
        max_date = max_check_in.check_in_without_hour
        if (max_check_in.imputation_date and
                max_check_in.imputation_date < max_date):
            max_date = max_check_in.imputation_date
        while min_date <= max_date:
            country = min_check_in[0].employee_id.company_id.country_id
            cond = [('date', '=', min_date),
                    ('year_id.country_id', '=', country.id),
                    ('year_id.year', '=', min_date.year)]
            festive = festive_obj.search(cond, limit=1)
            if not festive:
                cond = [('employee_id', '=', min_check_in[0].employee_id.id),
                        ('date', '=', min_date)]
                resume = resume_obj.search(cond, limit=1)
                if not resume:
                    emp = min_check_in[0].employee_id
                    calendar = emp._get_employee_calendar(date=min_date)
                    work_time, hour_from, hour_to = emp._get_day_info(
                        calendar, min_date)
                    if work_time != 0.0:
                        vals = self._catch_values_for_anomaly(
                            min_check_in[0].employee_id, min_date, work_time,
                            anomaly, calendar)
                        resume = resume_obj.create(vals)
            min_date += relativedelta(days=1)

    def _catch_values_for_anomaly(self, employee, min_date, work_time,
                                  anomaly, calendar):
        vals = {
            'employee_id': employee.id,
            'date': min_date,
            'theoretical_time': work_time,
            'created_from_anomaly': True,
            'with_anomaly': True,
            'day_week_literal': _catch_dayofweek(min_date),
            'attendance_anomaly_ids': [(6, 0, anomaly.ids)]}
        return vals

    def _impute_employee_attendances_without_day(self, date):
        resume_obj = self.env['hr.attendance.resume']
        anomalies = self.env['hr.attendance.resume.anomaly']
        anomaly = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_without_'
            'calendar_day')
        anomaly_without_exit = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_without_'
            'exit')
        anomaly_very_often = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_very_'
            'often')
        anomalies += anomaly
        if any(p.entry_without_exit for p in self):
            anomalies += anomaly_without_exit
        if any(p.worked_hours < 0.0166666666666667 for p in self):
            anomalies += anomaly_very_often
        resume = resume_obj.create(self._catch_values_for_create_resume())
        if resume.imputable_time >= 6.0:
            resume._put_personalized_planned_rest()
        self.update({'treated': True,
                     'attendance_resume_id': resume.id})
        resume.attendance_anomaly_ids = [(6, 0, anomalies.ids)]

    def _impute_employee_attendances_day(self):
        festive_obj = self.env['hr.holidays.public.line']
        anomalies = self.env['hr.attendance.resume.anomaly']
        anomaly_with_leave = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_with_leave')
        anomaly_festive_worked = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_festive_'
            'worked')
        anomaly_without_exit = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_without_'
            'exit')
        anomaly_very_often = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_very_'
            'often')
        anomaly_percentage_day = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_entry_'
            'percentage_day')
        anomaly_negative_time = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_negative_time')
        resume = super(HrAttendance, self)._impute_employee_attendances_day()
        if resume.leave_id:
            anomalies += anomaly_with_leave
        country = resume.employee_id.company_id.country_id
        cond = [('date', '=', resume.date),
                ('year_id.country_id', '=', country.id),
                ('year_id.year', '=', resume.date.year)]
        festive = festive_obj.search(cond, limit=1)
        if festive:
            anomalies += anomaly_festive_worked
        if any(p.entry_without_exit for p in self):
            anomalies += anomaly_without_exit
        if any(p.worked_hours < 0.0166666666666667 for p in self):
            anomalies += anomaly_very_often
        if not resume.leave_id and resume.imputable_time:
            calendar = resume.employee_id._get_employee_calendar(
                date=resume.date)
            # alfredo2
            work_time = resume.theoretical_time
            error = False
            if calendar.percentage_excess_hours:
                hours = (work_time * calendar.percentage_excess_hours) / 100
                imputable_time = work_time + hours
                if resume.imputable_time >= imputable_time:
                    error = True
            if calendar.percentage_defect_hours:
                hours = (work_time * calendar.percentage_defect_hours) / 100
                imputable_time = work_time - hours
                if resume.imputable_time <= imputable_time:
                    error = True
            if error:
                anomalies += anomaly_percentage_day
        if resume.imputable_time < 0:
            anomalies += anomaly_negative_time
        if anomalies:
            resume.write({'with_anomaly': True,
                          'attendance_anomaly_ids': [(6, 0, anomalies.ids)]})
        return resume

    def _create_resume_from_no_imputed_holidays(self, leave, employee, date):
        anomaly = self.env.ref(
            'hr_attendance_resume_anomaly.hr_attendance_anomaly_with_approved_'
            'absence')
        resume = super(
            HrAttendance, self)._create_resume_from_no_imputed_holidays(
                leave, employee, date)
        if resume:
            vals = {'with_anomaly': True,
                    'attendance_anomaly_ids': [(6, 0, anomaly.ids)]}
            resume.write(vals)
            if resume.theoretical_time_final == 0.0:
                resume.write({'anomaly_resolved': True})
        return resume


class HrAttendanceResume(models.Model):
    _inherit = 'hr.attendance.resume'

    attendance_anomaly_ids = fields.Many2many(
        string='Anomalies', comodel_name='hr.attendance.resume.anomaly',
        relation='rel_attendance_resume_anomaly',
        column1='attendance_resume_id', store=True,
        column2='attendance_anomaly_id')
    created_from_anomaly = fields.Boolean(
        string='Created from anomaly', default=False)
    with_anomaly = fields.Boolean(
        string='With anomaly', default=False)
    anomaly_resolved = fields.Boolean(
        string='Anomaly resolved', default=False)

    @api.depends('theoretical_time', 'leave_id', 'attendance_anomaly_ids')
    def _compute_theoretical_time_final(self):
        return super(
            HrAttendanceResume, self)._compute_theoretical_time_final()

    def _put_personalized_planned_rest(self):
        self.planned_rest = 0.333333333333333
