# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_day_info_of(self, calendar, date):
        days = calendar.mapped('attendance_ids').filtered(
            lambda x: x.dayofweek == str(date.weekday()))
        if not days:
            return 0.0, 0.0, 0.0
        if len(days) == 1:
            if days.hour_from != 0.0 and days.hour_to != 23.9833333333333:
                return days.work_time_of, days.real_hour_from, days.real_hour_to
            my_date = date
            if days.hour_from == 0.0:
                my_date += relativedelta(days=-1)
                days2 = calendar.mapped('attendance_ids').filtered(
                    lambda x: x.dayofweek == str(my_date.weekday()))
                if (days2 and days2.filtered(
                        lambda x: x.hour_to == 23.9833333333333)):
                    return 0.0, 0.0, 0.0
                else:
                    work_time = days2.work_time_of + days.work_time_of
                    return work_time, days2.real_hour_from, days.real_hour_to
            if days.hour_to == 23.9833333333333:
                return self._get_night_time_info_of(
                    days.work_time_of, days.real_hour_from, days.real_hour_to,
                    date, calendar)
        if not any(p.hour_to == 23.9833333333333 for p in days):
            min_hour = min(days, key=lambda x: x.hour_from)
            max_hour = max(days, key=lambda x: x.hour_to)
            hours = sum(days.mapped('work_time_of'))
            return hours, min_hour.real_hour_from, max_hour.real_hour_to
        day = days.filtered(lambda x: x.hour_to == 23.9833333333333)
        return self._get_night_time_info_of(
            day.work_time_of, day.real_hour_from, day.real_hour_to, date,
            calendar)

    def _get_night_time_info_of(self, work_time_of, real_hour_from,
                                real_hour_to, my_date, calendar):
        my_date += relativedelta(days=+1)
        days2 = calendar.mapped('attendance_ids').filtered(
            lambda x: x.dayofweek == str(my_date.weekday()))
        if days2:
            day2 = min(days2, key=lambda x: x.hour_from)
            if day2.hour_from == 0.0:
                work_time_of += day2.work_time_of
                return work_time_of, real_hour_from, day2.real_hour_to
        return work_time_of, real_hour_from, real_hour_to
