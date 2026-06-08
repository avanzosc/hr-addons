# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrAttendanceReason(models.Model):
    _inherit = "hr.attendance.reason"

    is_rest = fields.Boolean(default=False)
