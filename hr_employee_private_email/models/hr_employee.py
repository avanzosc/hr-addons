# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    private_email = fields.Char(related=False, readonly=False)
