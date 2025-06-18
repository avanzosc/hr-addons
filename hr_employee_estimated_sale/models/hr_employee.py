from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    estimated_sale_price = fields.Monetary(
        string="Precio estimado venta", currency_field="currency_id"
    )
