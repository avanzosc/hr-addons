# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class HrPersonalEquipment(models.Model):
    _inherit = "hr.personal.equipment"

    company_id_employee = fields.Many2one(
        string="Employee Company", related="employee_id.company_id", readonly=True
    )

    company_ids_product = fields.Many2many(
        string="Product Companies", related="product_id.company_ids", readonly=True
    )
