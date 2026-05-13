# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    see_in_employee = fields.Boolean()
