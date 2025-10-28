# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
from datetime import datetime

from odoo import _, api, fields, models

from .._common import _catch_employees_dates_to_treat

_logger = logging.getLogger(__name__)


class HrContract(models.Model):
    _inherit = "hr.contract"

    @api.model_create_multi
    def create(self, vals_list):
        contracts = super().create(vals_list)
        contracts_to_treat = contracts.filtered(lambda x: x.state == "open")
        if contracts_to_treat:
            contracts_to_treat._treat_all_from_contract()
        return contracts

    def write(self, vals):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        employees_dates = []
        if "date_start" in vals or "date_end" in vals:
            self._date_start_date_end_change(employees_dates, vals)
        result = super().write(vals)
        if "state" in vals and vals.get("state", False):
            employees_dates = self._contract_state_changed(employees_dates)
        if employees_dates:
            hr_attendance_leave_obj._treat_employee_dates(employees_dates)
        return result

    def unlink(self):
        self._clean_hr_attendance_leave_info()
        return super().unlink()

    def _date_start_date_end_change(self, employees_dates, vals):
        contracts = self.filtered(lambda x: x.state in ("open", "close"))
        for contract in contracts:
            if "date_start" in vals:
                date_start, date_end = contract._catch_min_max_date(
                    contract.date_start, vals.get("date_start")
                )
                employees_dates = _catch_employees_dates_to_treat(
                    employees_dates, contract.employee_id, date_start, date_end
                )
            if "date_end" in vals and vals.get("date_end", False) and contract.date_end:
                date_start, date_end = contract._catch_min_max_date(
                    contract.date_end, vals.get("date_end")
                )
                employees_dates = _catch_employees_dates_to_treat(
                    employees_dates, contract.employee_id, date_start, date_end
                )
            if (
                "date_end" in vals
                and vals.get("date_end", False)
                and not contract.date_end
            ):
                contract._contract_finalized_delete_attendance_leaves(
                    vals.get("date_end")
                )
            if (
                "date_end" in vals
                and not vals.get("date_end", False)
                and contract.date_end
            ):
                employees_dates = contract._treat_employee_assistances(
                    employees_dates, contract.date_end, False
                )
                employees_dates = contract._treat_employee_absences(
                    employees_dates, contract.date_end, False
                )
                if contract.resource_calendar_id:
                    employees_dates = contract._treat_employee_festives(
                        employees_dates, contract.date_end, False
                    )
        return employees_dates

    def _catch_min_max_date(self, date1, date2):
        if isinstance(date1, str):
            date1 = datetime.strptime(date1, "%Y-%m-%d").date()
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, "%Y-%m-%d").date()
        min_date = date1 if date1 <= date2 else date2
        max_date = date1 if date1 > date2 else date2
        return min_date, max_date

    def _contract_state_changed(self, employees_dates):
        for contract in self:
            if contract.state == "open":
                employees_dates = contract._treat_all_from_contract()
            if contract.state in ("draf", "cancel"):
                contract._clean_hr_attendance_leave_info()
            if contract.state == "close":
                contract._contract_finalized_delete_attendance_leaves()
        return employees_dates

    def _contract_finalized_delete_attendance_leaves(self, date_to=None):
        if not date_to:
            date_to = (
                self.date_end if self.date_end else fields.Date.context_today(self)
            )
        if isinstance(date_to, str):
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        attendance_leaves = self.employee_id.attendance_leave_ids.filtered(
            lambda x: x.contract_id == self and x.work_day > date_to
        )
        if attendance_leaves:
            attendance_leaves.unlink()

    def _clean_hr_attendance_leave_info(self):
        for contract in self:
            attendance_leaves = contract.employee_id.attendance_leave_ids.filtered(
                lambda x, contract=contract: x.contract_id == contract
            )
            if attendance_leaves:
                attendance_leaves.unlink()

    def _treat_employee_assistances(self, employees_dates, date_start, date_end):
        cond = [
            ("employee_id", "=", self.employee_id.id),
            ("check_in_without_hour", ">=", date_start),
        ]
        if date_end:
            cond.append(("check_in_without_hour", "<=", date_end))
        attendances = self.env["hr.attendance"].search(cond)
        if attendances:
            employees_dates = attendances._catch_employees_check_in_out_dates(
                employees_dates
            )
        return employees_dates

    def _treat_employee_absences(self, employees_dates, date_start, date_end):
        cond = [
            ("employee_id", "=", self.employee_id.id),
            ("date_from_without_hour", ">=", date_start),
        ]
        if date_end:
            cond.append(("date_to_without_hour", "<=", date_end))
        leaves = self.env["hr.leave"].search(cond)
        if leaves:
            employees_dates = leaves._catch_employees_check_in_out_dates(
                employees_dates
            )
        return employees_dates

    def _treat_employee_festives(self, employees_dates, date_start, date_end):
        cond = [
            ("company_id", "=", self.company_id.id),
            ("calendar_id", "=", self.resource_calendar_id.id),
            ("date_from_without_hour", ">=", date_start),
            ("resource_id", "=", False),
        ]
        if date_end:
            cond.append(("date_to_without_hour", "<=", date_end))
        festives = self.env["resource.calendar.leaves"].search(cond)
        for festive in festives:
            employees_dates = _catch_employees_dates_to_treat(
                employees_dates,
                self.employee_id,
                festive.date_from_without_hour,
                festive.date_to_without_hour,
            )
        return employees_dates

    def _post_install_hr_leave_attendance(self):
        companies = self.env["res.company"].search([])

        for company in companies:
            contracts = self.search(
                [("company_id", "=", company.id), ("state", "in", ("open", "close"))]
            )
            if contracts:
                contracts._treat_all_from_contract()

    def _treat_all_from_contract(self):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        for contract in self:
            valid = True
            if contract.state == "close":
                valid = contract._check_contract_has_attendances_leaves()
            if valid:
                employees_dates = []
                date_end = (
                    contract.date_end
                    if contract.date_end
                    else fields.Date.context_today(self)
                )
                employees_dates = _catch_employees_dates_to_treat(
                    employees_dates, contract.employee_id, contract.date_start, date_end
                )
                if not contract.date_end:
                    employees_dates = contract._treat_employee_festives(
                        employees_dates, contract.date_start, False
                    )
                if employees_dates:
                    hr_attendance_leave_obj._treat_employee_dates(employees_dates)

    def _check_contract_has_attendances_leaves(self):
        employees_dates = []
        employees_dates = self._treat_employee_assistances(
            employees_dates, self.date_start, self.date_end
        )
        if employees_dates:
            return True
        employees_dates = self._treat_employee_absences(
            employees_dates, self.date_start, self.date_end
        )
        if employees_dates:
            return True
        return False

    def ir_cron_active_today_day_in_calendar(self):
        admin_user = self.env.ref("base.user_admin")
        self.with_user(admin_user)._continue_active_today_day_in_calendar()

    def _continue_active_today_day_in_calendar(self):
        hr_attendance_leave_obj = self.env["hr.attendance.leave"]
        today_day = fields.Date.context_today(self)
        companies = self.env["res.company"].search([])
        for company in companies:
            contracts = self.search(
                [
                    ("company_id", "=", company.id),
                    ("state", "=", "open"),
                    ("date_start", "<=", today_day),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">=", today_day),
                ]
            )
            for contract in contracts:
                try:
                    with self.env.cr.savepoint():
                        employees_dates = []
                        employees_dates = _catch_employees_dates_to_treat(
                            employees_dates, contract.employee_id, today_day, today_day
                        )
                        if employees_dates:
                            hr_attendance_leave_obj._treat_employee_dates(
                                employees_dates
                            )
                except Exception as e:
                    message = _(
                        "Error generating today day in hr_attendance_leave, "
                        "employee: %(employee)s, "
                        "contract: %(contract)s, "
                        "error: %(error)s."
                    ) % {
                        "employee": contract.employee_id.name,
                        "contract": contract.name,
                        "error": e,
                    }
                    _logger.exception(message)
