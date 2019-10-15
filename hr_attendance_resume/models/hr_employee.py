# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_employee_calendar(self, date):
        calendar = self.resource_calendar_id
        if self.calendar_ids:
            calendars = self.calendar_ids.filtered(
                lambda c: (not c.date_start or (c.date_start and c.date_start <= date)) and
                (not c.date_end or (c.date_end and c.date_end > date)))
            if calendars and len(calendars) == 1:
                calendar = calendars.calendar_id
        return calendar

    def _get_day_work_time(self, calendar, date):
        days = calendar.mapped('attendance_ids').filtered(
            lambda x: x.dayofweek == str(date.weekday()))
        if not days:
            return 0.0
        if len(days) == 1:
            return days.work_time
        if not any(p.hour_to == 23.9833333333333 for p in days):
            return sum(days.mapped('work_time'))
        day = days.filtered(lambda x: x.hour_to == 23.9833333333333)
        work_time = day.work_time
        date += relativedelta(days=1)
        days2 = calendar.mapped('attendance_ids').filtered(
            lambda x: x.dayofweek == str(date.weekday()))
        if days2:
            day2 = min(days2, key=lambda x: x.hour_from)
            work_time += day2.work_time
        return work_time
