# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

from .._common import _catch_employees_dates_to_treat, _get_local_date


class ResourceCandelarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

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
        festives = super().create(vals_list)
        employees_dates = festives._catch_employees_contract_dates_to_treat([])
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return festives

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
        employees_dates = self._catch_employees_contract_dates_to_treat([])
        result = super().write(vals)
        if "date_from_without_hour" in vals or "date_to_without_hour" in vals:
            employees_dates = self._catch_employees_contract_dates_to_treat(
                employees_dates
            )
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return result

    def unlink(self):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        employees_dates = self._catch_employees_contract_dates_to_treat([])
        result = super().unlink()
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return result

    def _catch_employees_contract_dates_to_treat(self, employees_dates):
        for leave in self.filtered(
            lambda x: x.date_from_without_hour and x.date_to_without_hour
        ):
            date_from = leave.date_from_without_hour
            date_to = leave.date_to_without_hour
            if date_from and date_to:
                while date_from <= date_to:
                    cond = [
                        ("company_id", "=", leave.company_id.id),
                        ("date_start", "<=", date_from),
                        "|",
                        ("date_end", "=", False),
                        ("date_end", ">=", date_from),
                    ]
                    if leave.calendar_id:
                        cond.append(("resource_calendar_id", "=", leave.calendar_id.id))
                    contracts = self.env["hr.contract"].sudo().search(cond)
                    for contract in contracts:
                        employees_dates = _catch_employees_dates_to_treat(
                            employees_dates, contract.employee_id, date_from, date_from
                        )
                    date_from = date_from + relativedelta(days=1)
        return employees_dates

    def _put_dates_without_hour(self):
        companies = self.env["res.company"].search([])
        for company in companies:
            festives = self.search(
                [
                    ("company_id", "=", company.id),
                    ("calendar_id", "!=", False),
                    ("resource_id", "=", False),
                ]
            )
            for festive in festives:
                vals = {}
                if festive.date_from:
                    vals["date_from_without_hour"] = _get_local_date(
                        festive.date_from, self.env.user.tz
                    )
                if festive.date_to:
                    vals["date_to_without_hour"] = _get_local_date(
                        festive.date_to, self.env.user.tz
                    )
                if vals:
                    festive.write(vals)
