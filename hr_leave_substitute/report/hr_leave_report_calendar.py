from odoo import _, api, models


class HrLeaveReportCalendarInherited(models.Model):
    _inherit = "hr.leave.report.calendar"

    @api.depends("employee_id.name", "leave_id")
    def _compute_name(self):
        result = super()._compute_name()

        for leave in self:
            substitute = leave.leave_id.substitute_id
            if substitute:
                leave.name += _(", Substitute: %(substitute)s") % {
                    "substitute": substitute.name,
                }

        return result
