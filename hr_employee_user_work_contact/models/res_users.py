# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            employee = self.env["hr.employee"].browse(vals.get("create_employee_id"))
            contact = employee.work_contact_id
            if contact and not contact.user_ids and not vals.get("partner_id"):
                vals["partner_id"] = contact.id
        return super().create(vals_list)
