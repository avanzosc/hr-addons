# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .._common import _catch_employees_dates_to_treat, _get_local_date


class HrLeave(models.Model):
    _inherit = "hr.leave"

    date_from_without_hour = fields.Date(
        string="Start Date Without Hour", copy=False, index=True
    )
    date_to_without_hour = fields.Date(
        string="End Date Without Hour", copy=False, index=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        for vals in vals_list:
            if "date_from" in vals:
                vals["date_from_without_hour"] = _get_local_date(
                    vals.get("date_from"), self.env.user.tz
                )
            if "date_to" in vals:
                vals["date_to_without_hour"] = _get_local_date(
                    vals.get("date_to"), self.env.user.tz
                )
        leaves = super().create(vals_list)
        employees_dates = leaves._catch_employees_check_in_out_dates([])
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return leaves

    def write(self, vals):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        if "date_from" in vals:
            vals["date_from_without_hour"] = _get_local_date(
                vals.get("date_from"), self.env.user.tz
            )
        if "date_to" in vals:
            vals["date_to_without_hour"] = _get_local_date(
                vals.get("date_to"), self.env.user.tz
            )
        employees_dates = self._catch_employees_check_in_out_dates([])
        result = super().write(vals)
        if (
            "date_from_without_hour" in vals
            or "date_to_without_hour" in vals
            or "state" in vals
        ):
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
        for leave in self.filtered(
            lambda x: x.date_from_without_hour and x.date_to_without_hour
        ):
            employees_dates = _catch_employees_dates_to_treat(
                employees_dates,
                leave.employee_id,
                leave.date_from_without_hour,
                leave.date_to_without_hour,
            )
        return employees_dates

    def _put_dates_without_hour(self):
        companies = self.env["res.company"].search([])
        for company in companies:
            leaves = self.search([("employee_company_id", "=", company.id)])
            for leave in leaves:
                vals = {}
                if leave.date_from:
                    vals["date_from_without_hour"] = _get_local_date(
                        leave.date_from, self.env.user.tz
                    )
                if leave.date_to:
                    vals["date_to_without_hour"] = _get_local_date(
                        leave.date_to, self.env.user.tz
                    )
                if vals:
                    leave.write(vals)
