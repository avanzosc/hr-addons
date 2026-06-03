
from odoo import http
from odoo.http import request, route
from odoo.addons.hr_attendance_reason.controllers.main import HrAttendance as BaseHrAttendance
import logging

_logger = logging.getLogger(__name__)

class HrAttendanceNoReasonsSystray(BaseHrAttendance):
    @route("/hr_attendance/attendance_user_data", type="json", auth="user")
    def user_attendance_data(self):
        _logger.info("✅ Entrando en override user_attendance_data " \
        "de hr_attendance_reason_custom")
        res = super().user_attendance_data()

        employee = request.env.user.employee_id
        if not employee:
            return res

        company = employee.company_id or request.env.company
        next_action = (
            "sign_out"
            if res.get("attendance_state") == "checked_in"
            else "sign_in"
        )

        Reason = request.env["hr.attendance.reason"].sudo()
        domain = [
            ("show_on_attendance_screen", "=", True),
            ("action_type", "=", next_action),
            ("company_id", "in", [False, company.id]),
        ]

        if not Reason.search_count(domain):
            res.update(
                {
                    "reasons": [],
                    "show_reason_on_attendance_screen": False,
                    "required_reason_on_attendance_screen": False,
                    "default_sign_in_reason_id": False,
                    "default_sign_out_reason_id": False,
                }
            )

        return res