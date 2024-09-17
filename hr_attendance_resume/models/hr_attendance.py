# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, exceptions, _
from dateutil.relativedelta import relativedelta
from .._common import _convert_to_local_date, _convert_to_utc_date
from .._common import _catch_dayofweek


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    treated = fields.Boolean(string='Treated', default=False)
    imputation_date = fields.Date(
        string='Imputation date', compute='_compute_imputation_date_hour',
        store=True)
    rest_time = fields.Float(
        string='Rest time', compute='_compute_imputation_date_hour',
        store=True)
    hour_gap = fields.Float(
        string='Hour gap', compute='_compute_imputation_date_hour',
        store=True)
    notes = fields.Text(string='Notes')
    attendance_resume_id = fields.Many2one(
        string='Hours imputations resume',
        comodel_name='hr.attendance.resume')
    check_in_without_hour = fields.Date(
        string='Check in without hour', store=True,
        compute='_compute_check_in_without_hour')

    @api.depends('check_in')
    def _compute_check_in_without_hour(self):
        for record in self.filtered(
                lambda c: c.employee_id.resource_calendar_id and c.check_in):
            date = _convert_to_local_date(
                record.check_in, record.employee_id.resource_calendar_id.tz)
            record.check_in_without_hour = date.date()

    @api.depends(
        'check_in', 'check_out', 'employee_id',
        'employee_id.resource_calendar_id',
        'employee_id.resource_calendar_id.attendance_ids',
        'employee_id.resource_calendar_id.attendance_ids.delay_hour_from',
        'employee_id.resource_calendar_id.attendance_ids.delay_hour_to',
        'employee_id.resource_calendar_id.attendance_ids.rest_time',
        'employee_id.resource_calendar_id.attendance_ids.night_shift',
        'employee_id.calendar_ids', 'employee_id.calendar_ids.date_start',
        'employee_id.calendar_ids.date_end',
        'employee_id.calendar_ids.calendar_id',
        'employee_id.resource_calendar_id.tz')
    def _compute_imputation_date_hour(self):
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
                if date >= fec_des and date <= fec_has:
                    record.imputation_date = imputation_date
                if (date >= fec_des and date <= fec_has and not
                        day.night_shift):
                    record.rest_time = sum(days.mapped('rest_time'))
                    record.hour_gap = sum(days.mapped('work_time'))
                    break
                if date >= fec_des and date <= fec_has and day.night_shift:
                    calendar2 = False
                    days2 = False
                    if day.hour_from == 0.0:
                        record.imputation_date = (
                            imputation_date + relativedelta(days=-1))
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
                        record.rest_time = (
                            day.rest_time if day.rest_time else
                            days2.rest_time)
                        record.hour_gap = day.work_time + days2.work_time
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
                        record.rest_time = (
                            day.rest_time if day.rest_time else
                            days2.rest_time)
                        record.hour_gap = day.work_time + days2.work_time
                    break

    @api.multi
    def unlink(self):
        for attendance in self:
            date = attendance.imputation_date
            resume = self._search_employee_attendance_resume(
                attendance.employee_id, date)
            if resume and resume.hr_leave_allocation_id:
                error = _(u'You cannot delete the hours imputations resume '
                          'with date {},  of the employee {}, because he has '
                          'assigned an allocation').format(
                              resume.date, resume.employee_id.name)
                raise exceptions.Warning(error)
        return super(HrAttendance, self).unlink()

    @api.multi
    def write(self, vals):
        if 'treated' in vals and not vals.get('treated', False):
            for attendance in self:
                date = attendance.imputation_date
                resume = self._search_employee_attendance_resume(
                    attendance.employee_id, date)
                if resume:
                    resume.unlink()
        return super(HrAttendance, self).write(vals)

    def _impute_in_attendance_resume(self):
        cond = [('id', 'in', self.mapped('employee_id').ids),
                ('resource_calendar_id', '!=', False)]
        employees = self.env['hr.employee'].search(cond)
        for employee in employees:
            emp_attendances = self.filtered(
                lambda c: c.employee_id.id == employee.id and
                c.check_out and not c.treated)
            emp_attendances._impute_employee_attendances()

    def _impute_employee_attendances(self):
        self._delete_employee_attendance_resumes()
        imputations = self.filtered(lambda c: c.imputation_date)
        dates = set(imputations.mapped('imputation_date'))
        for date in dates:
            if date:
                attendances = self.filtered(
                    lambda c: c.imputation_date == date)
                attendances._impute_employee_attendances_day()

    def _delete_employee_attendance_resumes(self):
        resume_obj = self.env['hr.attendance.resume']
        min_fec, max_fec = self._catch_employee_min_max_dates()
        cond = [('employee_id', '=', self[0].employee_id.id),
                ('date', '>=', min_fec),
                ('date', '<=', max_fec)]
        resumes = resume_obj.search(cond)
        if resumes:
            resumes.unlink()

    def _catch_employee_min_max_dates(self):
        with_calendar = self.filtered(lambda c: c.imputation_date)
        min_fec = False
        max_fec = False
        if with_calendar:
            min_fec = min(with_calendar, key=lambda x: x.imputation_date)
            min_fec = min_fec.imputation_date
            max_fec = max(with_calendar, key=lambda x: x.imputation_date)
            max_fec = max_fec.imputation_date
        without_calendar = self.filtered(lambda c: not c.imputation_date)
        if without_calendar:
            max_fec2 = max(
                without_calendar, key=lambda x: x.check_in_without_hour)
            if not max_fec or max_fec2.check_in_without_hour > max_fec:
                max_fec = max_fec2.check_in_without_hour
            min_fec2 = min(
                without_calendar, key=lambda x: x.check_in_without_hour)
            if not min_fec or min_fec2.check_in_without_hour < min_fec:
                min_fec = min_fec2.check_in_without_hour
        return min_fec, max_fec

    def _impute_employee_attendances_day(self):
        resume_obj = self.env['hr.attendance.resume']
        resume = resume_obj.create(self._catch_values_for_create_resume())
        self.update({'treated': True,
                     'attendance_resume_id': resume.id})
        return resume

    def _search_employee_attendance_resume(self, employee, date):
        cond = [('employee_id', '=', employee.id),
                ('date', '=', date)]
        return self.env['hr.attendance.resume'].search(cond, limit=1)

    def _catch_values_for_create_resume(self):
        min_fec = min(self, key=lambda x: x.check_in)
        max_fec = max(self, key=lambda x: x.check_in)
        date = (min_fec.imputation_date if min_fec.imputation_date else
                min_fec.check_in_without_hour)
        check_in = _convert_to_local_date(
            min_fec.check_in,
            min_fec.employee_id.resource_calendar_id.tz)
        check_out = _convert_to_local_date(
            max_fec.check_out,
            max_fec.employee_id.resource_calendar_id.tz)
        fout = fields.Datetime.from_string('{} {}:{}:00'.format(
            check_out.date(), check_out.hour, check_out.minute))
        fini = fields.Datetime.from_string('{} {}:{}:00'.format(
            check_in.date(), check_in.hour, check_in.minute))
        delta = fout - fini
        presence_time = delta.total_seconds() / 3600.0
        work_time = sum(self.mapped('worked_hours'))
        theoretical_time = min_fec.hour_gap
        calendar = min_fec.employee_id._get_employee_calendar(
            date=min_fec.check_in.date())
        bonus_hours = 0.0
        bonus_day = calendar.mapped('bonus_ids').filtered(
            lambda x: x.dayofweek == str(date.weekday()))
        if bonus_day:
            bonus_hours = (work_time * bonus_day.bonus_percentage) / 100
        rest_number = int(len(self))
        if rest_number >= 1:
            rest_number -= 1
        vals = {
            'employee_id': min_fec.employee_id.id,
            'date': date,
            'planned_rest': min_fec.rest_time,
            'presence_time': presence_time,
            'work_time': work_time,
            'bonus_hours': bonus_hours,
            'theoretical_time': theoretical_time,
            'rest_number': rest_number}
        date_to = (
            _convert_to_local_date(max_fec.check_out, calendar.tz)).date()
        date_dayofweek = _catch_dayofweek(date)
        date_to_dayofweek = _catch_dayofweek(date_to)
        day_week_literal = date_dayofweek
        if date_dayofweek != date_to_dayofweek:
            day_week_literal = u"{}-{}".format(
                day_week_literal, date_to_dayofweek)
        if bonus_day:
            day_week_literal = _(u'{} (Bonus {}%)').format(
                day_week_literal, bonus_day.bonus_percentage)
        vals['day_week_literal'] = day_week_literal
        markings = ''
        dates = sorted(set(self.mapped('check_in')))
        count = 0
        for date in dates:
            imputation = self.filtered(
                lambda x: x.check_in == date)
            check_in = (
                _convert_to_local_date(imputation.check_in, calendar.tz))
            check_out = (
                _convert_to_local_date(imputation.check_out, calendar.tz))
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
        vals['markings'] = markings
        return vals


class HrAttendanceResume(models.Model):
    _name = 'hr.attendance.resume'
    _description = "Hours imputations resume"

    employee_id = fields.Many2one(
        string='Employee', comodel_name='hr.employee')
    date = fields.Date(string='Date')
    day_week = fields.Char(
        string='Day week', compute='_compute_day_week', store=True)
    day_week_literal = fields.Char(string='Day week')
    markings = fields.Char(
        string='Markings (E=Entrance, O=Output)')
    planned_rest = fields.Float(string='Planned rest', default=0.0)
    presence_time = fields.Float(string='Presence time', default=0.0)
    rest_number = fields.Integer(
        string='Rest number', default=0)
    rest_time = fields.Float(
        string='Rest time', compute='_compute_rest_exceeded_time', store=True)
    rest_exceeded = fields.Float(
        string='Rest exceeded', store=True,
        compute='_compute_rest_exceeded_time')
    work_time = fields.Float(string='Work time', default=0.0)
    bonus_hours = fields.Float(string='Bonus hours', default=0.0)
    imputable_time = fields.Float(
        string='Imputable time', compute='_compute_imputable_diference',
        store=True)
    theoretical_time = fields.Float(string='Theoretical time', default=0.0)
    difference_hours = fields.Float(
        string='Difference hours', store=True,
        compute='_compute_imputable_diference')
    difference_minutes = fields.Integer(
        string='Difference minutes', store=True,
        compute='_compute_imputable_diference')
    hr_attendance_ids = fields.One2many(
        comodel_name='hr.attendance', inverse_name='attendance_resume_id',
        string='Attendances')

    @api.depends('date')
    def _compute_day_week(self):
        for record in self.filtered(lambda c: c.date):
            record.day_week = _catch_dayofweek(record.date)

    @api.depends('presence_time', 'work_time', 'planned_rest')
    def _compute_rest_exceeded_time(self):
        for record in self.filtered(lambda c: c.presence_time and c.work_time):
            record.rest_time = record.presence_time - record.work_time
            if ((record.rest_time - record.planned_rest) <= 0):
                record.rest_exceeded = 0
            else:
                record.rest_exceeded = record.rest_time - record.planned_rest

    @api.depends('theoretical_time', 'presence_time', 'bonus_hours',
                 'rest_exceeded', 'planned_rest')
    def _compute_imputable_diference(self):
        for record in self.filtered(lambda c: c.theoretical_time):
            record.imputable_time = (
                record.presence_time + record.bonus_hours -
                record.rest_exceeded)
            difference_hours = record.imputable_time - record.theoretical_time
            if difference_hours != 0:
                record.difference_hours = difference_hours
                record.difference_minutes = round(difference_hours * 60)
