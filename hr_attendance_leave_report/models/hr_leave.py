# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import float_round


class HrLeave(models.Model):
    _inherit = "hr.leave"

    hours_duration = fields.Float(
        string="Hours durations",
        store=True,
        copy=False,
        compute="_compute_hours_duration",
    )

    @api.depends("number_of_hours_display", "number_of_days_display")
    def _compute_hours_duration(self):
        for leave in self:
            hours = 0
            if leave.leave_type_request_unit == "hour":
                hours = float_round(leave.number_of_hours_display, precision_digits=2)
            leave.hours_duration = hours
