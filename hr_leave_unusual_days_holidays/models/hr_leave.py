import logging
from datetime import timedelta

from odoo import api, models

_logger = logging.getLogger(__name__)


class HrLeave(models.Model):
    _inherit = "hr.leave"

    @api.model
    def get_unusual_days(self, date_from, date_to=None):
        context = self.env.context or {}
        employee_id = context.get("active_id")

        if not employee_id:
            return super().get_unusual_days(date_from, date_to)

        employee = self.env["hr.employee"].browse(employee_id)
        if not employee.exists():
            return super().get_unusual_days(date_from, date_to)

        self = self.with_context(employee_id=employee.id)
        unusual_days = super().get_unusual_days(date_from, date_to)

        calendar = employee.resource_calendar_id
        if not calendar:
            return unusual_days

        leaves = self.env["resource.calendar.leaves"].search(
            [("resource_id", "=", False), ("calendar_id", "=", calendar.id)]
        )

        for leave in leaves:
            dt_from = leave.date_from
            dt_to = leave.date_to

            if dt_from.date() == dt_to.date():
                date_str = dt_from.strftime("%Y-%m-%d")
                unusual_days[date_str] = True
            else:
                _logger.warning(
                    "Leave from %s to %s does not have the same date.",
                    dt_from,
                    dt_to,
                )
                current_day = dt_from.date()
                while current_day <= dt_to.date():
                    date_str = current_day.strftime("%Y-%m-%d")
                    unusual_days[date_str] = True
                    current_day += timedelta(days=1)

        return unusual_days
