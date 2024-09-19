# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools


class HRAttendanceReport(models.Model):
    _inherit = "hr.attendance.report"

    hours_to_work = fields.Float(readonly=True)
    leave_hours = fields.Float(readonly=True)
    worked_leave_hours = fields.Float(string="Worked leave hours", readonly=True)

    @api.model
    def _select(self):
        select = super()._select()
        my_select = """
                  (select sum(cal.hour_to - cal.hour_from)
                   from  resource_calendar_attendance cal,
                         resource_calendar reso,
                         hr_employee emp
                   where reso.id = cal.calendar_id
                     and emp.id = hra.employee_id
                     and emp.resource_calendar_id = reso.id
                     and (
                     (to_char(hra.check_in,'d') = '1' and cal.dayofweek = '6') or
                     (to_char(hra.check_in,'d') = '2' and cal.dayofweek = '0') or
                     (to_char(hra.check_in,'d') = '3' and cal.dayofweek = '1') or
                     (to_char(hra.check_in,'d') = '4' and cal.dayofweek = '2') or
                     (to_char(hra.check_in,'d') = '5' and cal.dayofweek = '3') or
                     (to_char(hra.check_in,'d') = '6' and cal.dayofweek = '4') or
                     (to_char(hra.check_in,'d') = '7' and cal.dayofweek = '5')
                     )
                  ) as hours_to_work, 0 as leave_hours, 0 as worked_leave_hours
                   """
        new_select = "{}, {}".format(select, my_select)
        return new_select

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """
            % (self._table, self._select(), self._from(), self._join(), self._union())
        )

    @api.model
    def _union(self):
        return """
            UNION SELECT
                cast(cast(hrl.id as varchar) || cast(hrl.employee_id as varchar) ||
                    EXTRACT(DAY FROM generate_series(request_date_from,
                    request_date_to, '1 day')) as integer) * -1 as id,
                hrl.department_id,
                hrl.employee_id,
                hrl.employee_company_id,
                generate_series(request_date_from, request_date_to, '1 day') as check_in,
                0 as worked_hours,
                0 as overtime_hours,
                0 as hours_to_work,
                (select (l.hours_duration / (1 + l.request_date_to - l.request_date_from))
                from hr_leave l
                where l.id = hrl.id
                  and l.holiday_status_id = (
                        select hr_leave_type.id
                        from   hr_leave_type
                        where  hr_leave_type.id = l.holiday_status_id
                          and  hr_leave_type.time_type = 'leave')
                ) as leave_hours,
                (select (l.hours_duration / (1 + l.request_date_to - l.request_date_from))
                from hr_leave l
                where l.id = hrl.id
                  and l.holiday_status_id = (
                        select hr_leave_type.id
                        from   hr_leave_type
                        where  hr_leave_type.id = l.holiday_status_id
                          and  hr_leave_type.time_type = 'other')
                ) as worked_leave_hours

            FROM hr_leave as hrl
            WHERE hrl.state = 'validate'
        """
