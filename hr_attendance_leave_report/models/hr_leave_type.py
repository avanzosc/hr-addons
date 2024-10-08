# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    def unlink(self):
        for leave_type in self:
            cond = [("holiday_status_id", "=", leave_type.id)]
            leave = self.env["hr.leave"].search(cond, limit=1)
            if leave:
                raise ValidationError(
                    _(
                        "Leave type: '%s', exists in any absence of a worker. "
                        "You can disable this one, and create a new one."
                    )
                    % leave_type.display_name
                )
        return super().unlink()
