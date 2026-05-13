# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def action_employee_account_moves(self):
        self.ensure_one()
        partner = self.user_id.partner_id
        return {
            "type": "ir.actions.act_window",
            "name": "Journal Items",
            "res_model": "account.move.line",
            "view_mode": "tree,form",
            "domain": [
                ("full_reconcile_id", "=", False),
                ("balance", "!=", 0),
                ("account_id.reconcile", "=", True),
                ("see_in_employee", "=", True),
                ("partner_id", "=", partner.id),
            ],
            "context": {"create": False},
        }
