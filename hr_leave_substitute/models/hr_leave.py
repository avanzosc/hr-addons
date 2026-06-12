# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    substitute_id = fields.Many2one(
        string="Substitute", comodel_name="res.users", copy=False
    )

    @api.depends("employee_id", "holiday_status_id", "substitute_id")
    def _compute_display_name(self):
        result = super()._compute_display_name()
        for leave in self:
            if leave.substitute_id:
                display_name = _("%(display_name)s \n, substitute: %(substitute)s.") % {
                    "display_name": leave.display_name,
                    "substitute": leave.substitute_id.name,
                }
                leave.display_name = display_name
        return result
