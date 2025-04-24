# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrAttendanceLeave(models.Model):
    _inherit = "hr.attendance.leave"

    rest_hours = fields.Float(default=0.0, copy=False)

    def _initialize_vals(self, employee, work_date):
        contract, vals = super()._initialize_vals(employee, work_date)
        rest_hours = self._catch_rest_hours_on_work_date(employee, work_date)
        vals["rest_hours"] = rest_hours
        if rest_hours > 0.25:
            vals["worked_hours"] = vals.get("worked_hours") + 0.25
        else:
            vals["worked_hours"] = vals.get("worked_hours") + rest_hours
        return contract, vals

    def _catch_worked_hours_on_work_date(self, employee, work_date):
        worked_attendances = self.env["hr.attendance"]
        super()._catch_worked_hours_on_work_date(employee, work_date)
        attendances = employee.attendance_ids.filtered(
            lambda x: x.check_in_without_hour == work_date and x.check_out_without_hour
        )
        if not attendances:
            return 0
        for attendance in attendances:
            if attendance.attendance_reason_ids and not any(
                [x.is_rest for x in attendance.attendance_reason_ids]
            ):
                worked_attendances += attendance
        if not worked_attendances:
            return 0
        return sum(worked_attendances.mapped("worked_hours"))

    def _catch_rest_hours_on_work_date(self, employee, work_date):
        rest_attendances = self.env["hr.attendance"]
        attendances = employee.attendance_ids.filtered(
            lambda x: x.check_in_without_hour == work_date and x.check_out_without_hour
        )
        if not attendances:
            return 0
        for attendance in attendances:
            if attendance.attendance_reason_ids and any(
                [x.is_rest for x in attendance.attendance_reason_ids]
            ):
                rest_attendances += attendance
        if not rest_attendances:
            return 0
        return sum(rest_attendances.mapped("worked_hours"))

    def _get_leave(self, contract, work_date, vals):
        vals = super()._get_leave(contract, work_date, vals)
        if vals.get("rest_hours") > 0.25:
            diff = vals.get("rest_hours") - 0.25
            vals["non_remunerated_hours"] = vals.get("non_remunerated_hours") + diff
        return vals
