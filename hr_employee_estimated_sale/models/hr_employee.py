from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    estimated_sale_price = fields.Monetary(
        string='Precio estimado venta',
        currency_field='currency_id'
    )