# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models

ATTENDANCE_FIELDS = ("employee_id", "check_in", "check_out")


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    @api.model
    def _notify_attendance_user_menu_status(self, employees):
        """Send the new attendance status to the users of the employees, so
        that the indicator of their user menu is refreshed."""
        bus = self.env["bus.bus"]
        for employee in employees.sudo().exists().filtered("user_id"):
            bus._sendone(
                employee.user_id.partner_id,
                "hr_attendance_user_menu_status/update",
                {
                    "employee_id": employee.id,
                    "attendance_state": employee.attendance_state,
                },
            )

    @api.model_create_multi
    def create(self, vals_list):
        attendances = super().create(vals_list)
        self._notify_attendance_user_menu_status(attendances.employee_id)
        return attendances

    def write(self, vals):
        employees = self.employee_id
        result = super().write(vals)
        if any(field in vals for field in ATTENDANCE_FIELDS):
            self._notify_attendance_user_menu_status(employees | self.employee_id)
        return result

    def unlink(self):
        employees = self.employee_id
        result = super().unlink()
        self._notify_attendance_user_menu_status(employees)
        return result
