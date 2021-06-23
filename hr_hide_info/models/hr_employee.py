# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    personal_private_email = fields.Char(string='Personal private email')
