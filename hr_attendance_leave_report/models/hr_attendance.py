# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .._common import _catch_employees_dates_to_treat, _get_local_date


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_without_hour = fields.Date(copy=False, index=True)
    check_out_without_hour = fields.Date(copy=False, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        for vals in vals_list:
            if "check_in" in vals:
                vals["check_in_without_hour"] = _get_local_date(
                    vals.get("check_in"), self.env.user.tz
                )
            if "check_out" in vals:
                if vals.get("check_out", False):
                    vals["check_out_without_hour"] = _get_local_date(
                        vals.get("check_out"), self.env.user.tz
                    )
                else:
                    vals["check_out_without_hour"] = False
        attendances = super().create(vals_list)
        employees_dates = attendances._catch_employees_check_in_out_dates([])
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return attendances

    def write(self, vals):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        if "check_in" in vals:
            vals["check_in_without_hour"] = _get_local_date(
                vals.get("check_in"), self.env.user.tz
            )
        if "check_out" in vals:
            if vals.get("check_out", False):
                vals["check_out_without_hour"] = _get_local_date(
                    vals.get("check_out"), self.env.user.tz
                )
            else:
                vals["check_out_without_hour"] = False
        employees_dates = self._catch_employees_check_in_out_dates([])
        result = super().write(vals)
        if "check_in_without_hour" in vals or "check_in_without_hour" in vals:
            employees_dates = self._catch_employees_check_in_out_dates(employees_dates)
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return result

    def unlink(self):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        employees_dates = self._catch_employees_check_in_out_dates([])
        result = super().unlink()
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return result

    def _catch_employees_check_in_out_dates(self, employees_dates):
        for attendance in self.filtered(lambda x: x.check_in_without_hour):
            date_start = attendance.check_in_without_hour
            check_out = attendance.check_out_without_hour
            date_end = check_out if check_out else date_start
            employees_dates = _catch_employees_dates_to_treat(
                employees_dates, attendance.employee_id, date_start, date_end
            )
        return employees_dates

    def _put_dates_without_hour(self):
        attendances = self.search([])
        for attendance in attendances:
            vals = {}
            if attendance.check_in:
                vals["check_in_without_hour"] = _get_local_date(
                    attendance.check_in, self.env.user.tz
                )
            if attendance.check_out:
                vals["check_out_without_hour"] = _get_local_date(
                    attendance.check_out, self.env.user.tz
                )
            if vals:
                attendance.write(vals)
