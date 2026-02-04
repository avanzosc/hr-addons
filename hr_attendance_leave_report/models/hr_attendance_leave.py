# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class HrAttendanceLeave(models.Model):
    _name = "hr.attendance.leave"
    _description = "Attendances And Absences"
    _rec_name = "day_type"
    _order = "work_day desc, display_name asc"

    work_day = fields.Date(copy=False, index=True)
    employee_id = fields.Many2one(
        string="Employee", comodel_name="hr.employee", copy=False, index=True
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        store=True,
        copy=False,
        related="employee_id.company_id",
    )
    user_id = fields.Many2one(
        string="Employee",
        comodel_name="res.users",
        store=True,
        copy=False,
        related="employee_id.user_id",
    )
    display_name = fields.Char(
        string="Employee", related="user_id.name", copy=False, store=True
    )
    contract_id = fields.Many2one(
        string="Contract", comodel_name="hr.contract", copy=False
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        related="contract_id.department_id",
        store=True,
        copy=False,
    )
    day_type = fields.Char(string="Day type", copy=False, translate=True)
    is_normal_day = fields.Boolean(default=False, copy=False)
    leave_type_id = fields.Many2one(
        string="Leave Type", comodel_name="hr.leave.type", copy=False
    )
    calendar_leave_id = fields.Many2one(
        string="Festive", comodel_name="resource.calendar.leaves", copy=False
    )
    hours_to_work = fields.Float(default=0.0, copy=False)
    worked_hours = fields.Float(string="Worked hours", default=0.0, copy=False)
    remunerated_hours = fields.Float(default=0.0, copy=False)
    non_remunerated_hours = fields.Float(default=0.0, copy=False)
    extra_hours = fields.Float(
        compute="_compute_attendance_leave_info",
        compute_sudo=True,
        string="Extra hours",
        copy=False,
        store=True,
    )

    @api.depends(
        "is_normal_day",
        "leave_type_id",
        "leave_type_id.name",
        "calendar_leave_id",
        "calendar_leave_id.name",
        "hours_to_work",
        "worked_hours",
        "remunerated_hours",
        "non_remunerated_hours",
    )
    def _compute_attendance_leave_info(self):
        for line in self:
            extra_hours = 0
            if not line.calendar_leave_id:
                if not line.leave_type_id or (
                    line.leave_type_id and line.leave_type_id.time_type != "other"
                ):
                    extra_hours = line._extra_hours_in_non_remurated_day()
            if line.calendar_leave_id or (
                line.leave_type_id and line.leave_type_id.time_type == "other"
            ):
                extra_hours = line._extra_hours_in_remurated_day()
            line.extra_hours = extra_hours

    def _extra_hours_in_non_remurated_day(self):
        extra_hours = 0
        if self.worked_hours == 0:
            extra_hours = self.hours_to_work * -1
        else:
            extra_hours = self.worked_hours - self.hours_to_work
        return extra_hours

    def _extra_hours_in_remurated_day(self):
        extra_hours = 0
        if self.worked_hours == 0:
            extra_hours = (self.hours_to_work - self.remunerated_hours) * -1
        else:
            worked_hours = self.worked_hours + self.remunerated_hours
            if worked_hours >= self.hours_to_work:
                extra_hours = worked_hours - self.hours_to_work
            else:
                extra_hours = (self.hours_to_work - worked_hours) * -1
        return extra_hours

    def _treat_employee_dates(self, employees_dates):
        for employee_date in employees_dates:
            for date_to_treat in employee_date.get("work_date"):
                self._update_attendance_leave_info(
                    employee=employee_date.get("employee"), work_date=date_to_treat
                )

    def _update_attendance_leave_info(self, employee, work_date):
        contract, vals = self._initialize_vals(employee, work_date)
        if contract:
            vals = self._get_festive(contract, work_date, vals)
        if contract and not vals.get("calendar_leave_id"):
            vals = self._get_leave(contract, work_date, vals)
        if (
            contract
            and not vals.get("leave_type_id")
            and not vals.get("calendar_leave_id") not in vals
        ):
            vals["is_normal_day"] = True
        attendance_leave = employee.sudo().attendance_leave_ids.filtered(
            lambda x: x.work_day == work_date and x.employee_id == employee
        )
        if not contract and attendance_leave:
            attendance_leave.unlink()
        if (
            contract
            and attendance_leave
            and vals.get("hours_to_work") == 0
            and vals.get("worked_hours") == 0
        ):
            attendance_leave.unlink()
        if (
            contract
            and attendance_leave
            and (vals.get("hours_to_work") != 0 or vals.get("worked_hours") != 0)
        ):
            attendance_leave.with_context(lang=self.env.user.lang).write(vals)
        if (
            contract
            and not attendance_leave
            and (vals.get("hours_to_work") != 0 or vals.get("worked_hours") != 0)
        ):
            vals["work_day"] = work_date
            vals["employee_id"] = employee.id
            attendance_leave.with_context(lang=self.env.user.lang).create(vals)

    def _initialize_vals(self, employee, work_date):
        hours_to_work, contract = self._catch_hours_of_work_schedule(
            employee, work_date
        )
        worked_hours = self._catch_worked_hours_on_work_date(employee, work_date)
        vals = {
            "contract_id": contract.id if contract else False,
            "hours_to_work": hours_to_work,
            "worked_hours": worked_hours,
            "extra_hours": worked_hours - hours_to_work,
            "calendar_leave_id": False,
            "leave_type_id": False,
            "remunerated_hours": 0.0,
            "non_remunerated_hours": 0.0,
            "day_type": _("Normal Day"),
        }
        return contract, vals

    def _catch_hours_of_work_schedule(self, employee, work_date):
        contract = employee.sudo().contract_ids.filtered(
            lambda x: x.company_id == employee.company_id
            and x.state in ("open", "close")
            and x.date_start <= work_date
            and (not x.date_end or x.date_end >= work_date)
        )
        if (
            not contract
            or not contract.resource_calendar_id
            or not contract.resource_calendar_id.attendance_ids
        ):
            return 0, False
        lines = contract.resource_calendar_id.attendance_ids.filtered(
            lambda x: x.dayofweek == str(work_date.weekday())
        )
        hours_to_work = 0
        for line in lines:
            hours_to_work += line.hour_to - line.hour_from
        return hours_to_work, contract

    def _catch_worked_hours_on_work_date(self, employee, work_date):
        attendances = employee.sudo().attendance_ids.filtered(
            lambda x: x.check_in_without_hour == work_date and x.check_out_without_hour
        )
        if not attendances:
            return 0
        return sum(attendances.mapped("worked_hours"))

    def _get_festive(self, contract, work_date, vals):
        if contract.resource_calendar_id:
            cond = [
                ("company_id", "=", contract.company_id.id),
                ("calendar_id", "=", contract.resource_calendar_id.id),
                ("resource_id", "=", False),
                ("date_from_without_hour", "<=", work_date),
                ("date_to_without_hour", ">=", work_date),
            ]
            festive = self.env["resource.calendar.leaves"].search(cond, limit=1)
            if not festive:
                cond = [
                    ("company_id", "=", contract.company_id.id),
                    ("calendar_id", "=", False),
                    ("resource_id", "=", False),
                    ("date_from_without_hour", "<=", work_date),
                    ("date_to_without_hour", ">=", work_date),
                ]
            festive = self.env["resource.calendar.leaves"].search(cond, limit=1)
            if festive:
                vals["calendar_leave_id"] = festive.id
                vals["day_type"] = festive.name
                vals["remunerated_hours"] = vals.get("hours_to_work")
        return vals

    def _get_leave(self, contract, work_date, vals):
        cond = [
            ("employee_company_id", "=", contract.company_id.id),
            ("employee_id", "=", contract.employee_id.id),
            ("date_from_without_hour", "<=", work_date),
            ("date_to_without_hour", ">=", work_date),
            ("state", "=", "validate"),
        ]
        leave = self.env["hr.leave"].search(cond, limit=1)
        if leave:
            hours = vals.get("hours_to_work")
            if leave.holiday_status_id.request_unit != "day":
                hours = leave.number_of_hours
            vals["leave_type_id"] = leave.holiday_status_id.id
            vals["day_type"] = leave.holiday_status_id.name
            if leave.holiday_status_id.time_type == "other":
                vals["remunerated_hours"] = hours
            if leave.holiday_status_id.time_type != "other":
                vals["non_remunerated_hours"] = hours
        return vals
