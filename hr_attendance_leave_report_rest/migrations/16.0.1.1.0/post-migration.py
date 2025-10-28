import logging

from openupgradelib import openupgrade

from odoo import _

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    attendance_obj = env["hr.attendance.leave"]
    attendances = attendance_obj.search([])
    for attendance in attendances:
        try:
            attendance_obj._update_attendance_leave_info(
                attendance.employee_id, attendance.work_day
            )
        except Exception:
            _logger.error = _(
                "Error processing hr attendance leave for "
                "employee: %(employee_name)s, and date: "
                "%(leave_date)s."
            ) % {
                "employee_name": attendance.employee_id.name,
                "leave_date": attendance.work_day,
            }
