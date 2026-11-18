# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import pytz
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _get_attendance_user_menu_hours(self, employee):
        now = fields.Datetime.now()
        now_tz = pytz.utc.localize(now).astimezone(pytz.timezone(employee.tz))
        start_naive = (
            (now_tz + relativedelta(hour=0, minute=0, second=0, microsecond=0))
            .astimezone(pytz.utc)
            .replace(tzinfo=None)
        )
        attendances = self.env["hr.attendance"].search(
            [
                ("employee_id", "=", employee.id),
                ("check_in", "<=", now),
                "|",
                ("check_out", ">=", start_naive),
                ("check_out", "=", False),
            ],
            order="check_in asc",
        )
        hours_today = 0.0
        last_attendance_worked_hours = 0.0
        for attendance in attendances:
            last_attendance_worked_hours = (
                (attendance.check_out or now) - max(attendance.check_in, start_naive)
            ).total_seconds() / 3600.0
            hours_today += last_attendance_worked_hours
        return {
            "hours_today": round(hours_today, 2),
            "hours_previously_today": round(
                hours_today - last_attendance_worked_hours, 2
            ),
            "last_attendance_worked_hours": round(last_attendance_worked_hours, 2),
        }

    @api.model
    def get_attendance_user_menu_status(self):
        employee = self.env.user.employee_id.sudo()
        if not employee:
            return {}
        return {
            "employee_id": employee.id,
            "attendance_state": employee.attendance_state,
            "can_check_in_out": self.env.user.has_group(
                "hr_attendance.group_hr_attendance"
            ),
            "last_check_in": fields.Datetime.to_string(employee.last_check_in),
            **self._get_attendance_user_menu_hours(employee),
        }

    @api.model
    def attendance_user_menu_check_in_out(self):
        if not self.env.user.has_group("hr_attendance.group_hr_attendance"):
            raise AccessError(_("You are not allowed to check in or check out."))
        employee = self.env.user.employee_id
        if not employee:
            raise UserError(_("Your user is not linked to any employee."))
        employee.sudo()._attendance_action_change()
        return self.get_attendance_user_menu_status()
