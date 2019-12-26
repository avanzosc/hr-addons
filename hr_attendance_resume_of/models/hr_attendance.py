# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from .._common import _convert_to_local_date, _convert_to_utc_date


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    theoretical_time_of = fields.Float(
        string='Theoretical time of', compute='_compute_imputation_date_hour',
        store=True)

    @api.depends(
        'check_in', 'check_out', 'employee_id',
        'employee_id.resource_calendar_id',
        'employee_id.resource_calendar_id.attendance_ids',
        'employee_id.resource_calendar_id.attendance_ids.delay_hour_from',
        'employee_id.resource_calendar_id.attendance_ids.delay_hour_to',
        'employee_id.resource_calendar_id.attendance_ids.rest_time',
        'employee_id.resource_calendar_id.attendance_ids.night_shift',
        'employee_id.resource_calendar_id.attendance_ids.work_time_of',
        'employee_id.calendar_ids', 'employee_id.calendar_ids.date_start',
        'employee_id.calendar_ids.date_end',
        'employee_id.calendar_ids.calendar_id',
        'employee_id.resource_calendar_id.tz')
    def _compute_imputation_date_hour(self):
        result = super(HrAttendance, self)._compute_imputation_date_hour()
        for record in self.filtered(
                lambda c: c.employee_id.resource_calendar_id and c.check_out):
            date = _convert_to_local_date(
                record.check_in, record.employee_id.resource_calendar_id.tz)
            calendar = record.employee_id._get_employee_calendar(
                date=date.date())
            days = calendar.mapped('attendance_ids').filtered(
                lambda x: x.dayofweek == str(date.date().weekday()))
            imputation_date = date.date()
            if not days:
                imputation_date = (date.date() + relativedelta(days=-1))
                calendar2 = record.employee_id._get_employee_calendar(
                    date=imputation_date)
                days = calendar2.mapped('attendance_ids').filtered(
                    lambda x: x.dayofweek == str(imputation_date.weekday()))
            for day in days:
                fec_des = _convert_to_utc_date(
                     imputation_date, time=day.delay_hour_from, tz=u'UTC')
                hours = day.delay_hour_to
                my_date = fec_des.date()
                if hours > 24.0:
                    hours -= 24
                    my_date = (fec_des.date() + relativedelta(days=+1))
                fec_has = _convert_to_utc_date(
                    my_date, time=hours, tz=u'UTC')
                if (date >= fec_des and date <= fec_has and not
                        day.night_shift):
                    record.theoretical_time_of = sum(
                        days.mapped('work_time_of'))
                    break
                if date >= fec_des and date <= fec_has and day.night_shift:
                    calendar2 = False
                    days2 = False
                    if day.hour_from == 0.0 and day.rest_time == 0.0:
                        date2 = imputation_date + relativedelta(days=-1)
                        calendar2 = record.employee_id._get_employee_calendar(
                            date=date2)
                    if (day.hour_from == 0.0 and day.rest_time == 0.0 and
                            calendar2):
                        days2 = calendar2.mapped('attendance_ids').filtered(
                            lambda x: x.hour_to == 23.9833333333333 and
                            x.dayofweek == str(date2.weekday()))
                    if (day.hour_from == 0.0 and day.rest_time == 0.0 and
                            calendar2 and days2):
                        record.theoretical_time_of = (
                            day.work_time_of + days2.work_time_of)
                    if day.hour_to == 23.9833333333333:
                        date2 = imputation_date + relativedelta(days=+1)
                        calendar2 = record.employee_id._get_employee_calendar(
                            date=date2)
                    if day.hour_to == 23.9833333333333 and calendar2:
                        days2 = calendar2.mapped('attendance_ids').filtered(
                            lambda x: x.hour_from == 0 and
                            x.dayofweek == str(date2.weekday()))
                    if (day.hour_to == 23.9833333333333 and calendar2 and
                            days2):
                        record.theoretical_time_of = (
                            day.work_time_of + days2.work_time_of)
                    break
        return result

    def _catch_values_for_create_resume(self):
        vals = super(HrAttendance, self)._catch_values_for_create_resume()
        min_fec = min(self, key=lambda x: x.check_in)
        vals['theoretical_time_of'] = min_fec.theoretical_time_of
        return vals

    def _catch_values_for_anomaly(self, employee, min_date, work_time,
                                  anomaly, calendar):
        vals = super(
            HrAttendance, self)._catch_values_for_anomaly(
                employee, min_date, work_time, anomaly, calendar)
        work_time_of, real_hour_from, real_hour_to = employee._get_day_info_of(
            calendar, min_date)
        vals['theoretical_time_of'] = work_time_of
        return vals


class HrAttendanceResume(models.Model):
    _inherit = 'hr.attendance.resume'

    presence_time_of = fields.Float(
        string='Presence time of', compute='_compute_of_times', store=True)
    work_time_of = fields.Float(
        string='Work time of', compute='_compute_of_times', store=True)
    imputable_time_of = fields.Float(
        string='Imputable time of', compute='_compute_of_times', store=True)
    theoretical_time_of = fields.Float(
        string='Theoretical time of')
    markings_of = fields.Char(
        string='Markings of (E=Entrance, O=Output)', store=True,
        compute='_compute_markings_of')
    theoretical_time_final_of = fields.Float(
        string='Theoretical time', compute='_compute_theoretical_time_final',
        store=True)
    difference_hours_of = fields.Float(
        string='Difference hours', store=True,
        compute='_compute_imputable_diference_of')
    difference_minutes_of = fields.Integer(
        string='Difference minutes', store=True,
        compute='_compute_imputable_diference_of')

    @api.depends('theoretical_time', 'theoretical_time_of', 'leave_id',
                 'attendance_anomaly_ids')
    def _compute_theoretical_time_final(self):
        result = super(
            HrAttendanceResume, self)._compute_theoretical_time_final()
        for record in self:
            record.theoretical_time_final_of = record.theoretical_time_of
        return result

    @api.depends('presence_time', 'work_time', 'imputable_time',
                 'bonus_hours', 'theoretical_time', 'theoretical_time_of')
    def _compute_of_times(self):
        for record in self:
            emp = record.employee_id
            calendar = emp._get_employee_calendar(date=record.date)
            if calendar:
                # alfredo 2
                work_time_of = record.theoretical_time_of
                work_time = record.theoretical_time
                dif = work_time - work_time_of
                record.presence_time_of = (
                    0.0 if not record.presence_time else
                    record.presence_time - dif)
                record.work_time_of = (
                    0.0 if not record.work_time else record.work_time - dif)
                record.imputable_time_of = (
                    0.0 if not record.imputable_time else
                    record.imputable_time + record.bonus_hours - dif)

    @api.depends('imputable_time_of', 'theoretical_time_final_of')
    def _compute_imputable_diference_of(self):
        for record in self:
            difference_hours = (
                record.imputable_time_of - record.theoretical_time_final_of)
            if difference_hours != 0:
                record.difference_hours_of = difference_hours
                record.difference_minutes_of = round(difference_hours * 60)

    @api.depends('markings', 'hr_attendance_ids')
    def _compute_markings_of(self):
        for record in self:
            record.markings_of = record._calculate_markings_of()

    def _calculate_markings_of(self):
        employee = self.employee_id
        calendar = employee._get_employee_calendar(date=self.date)
        if not calendar:
            return self.markings
        # alfredo 2
        work_time_of = self.theoretical_time_of
        if work_time_of == 0.0:
            return self.markings
        work_time = self.theoretical_time
        if work_time_of == work_time:
            return self.markings
        dif = work_time - work_time_of
        hours = {}
        dates = sorted(set(self.hr_attendance_ids.mapped('check_in')))
        count = 0
        for my_date in dates:
            imputation = self.hr_attendance_ids.filtered(
                lambda x: x.check_in == my_date)
            count += 1
            key = str(count)
            if key not in hours:
                check_in = imputation.check_in
                if count == 1:
                    check_in += relativedelta(hours=float(dif / 2))
                check_out = imputation.check_out
                if count == len(dates):
                    check_out -= relativedelta(hours=float(dif / 2))
                vals = {'check_in': check_in,
                        'check_out': check_out}
                hours[key] = vals
        markings = ''
        count = 0
        for key in hours.keys():
            check_in = (
                _convert_to_local_date(
                    hours.get(key).get('check_in'), calendar.tz))
            check_out = (
                _convert_to_local_date(
                    hours.get(key).get('check_out'), calendar.tz))
            count += 1
            if count == 1:
                if not markings:
                    markings = _(u'{}:{}E{}:{}O').format(
                        str(check_in.hour).zfill(2),
                        str(check_in.minute).zfill(2),
                        str(check_out.hour).zfill(2),
                        str(check_out.minute).zfill(2))
                else:
                    markings = _(u'{}{}:{}E{}:{}O').format(
                        markings, str(check_in.hour).zfill(2),
                        str(check_in.minute).zfill(2),
                        str(check_out.hour).zfill(2),
                        str(check_out.minute).zfill(2))
            else:
                markings = _(u'{}/{}:{}E{}:{}O').format(
                    markings, str(check_in.hour).zfill(2),
                    str(check_in.minute).zfill(2),
                    str(check_out.hour).zfill(2),
                    str(check_out.minute).zfill(2))
                if count == 2:
                    markings += '\n'
                    count = 0
        return markings
