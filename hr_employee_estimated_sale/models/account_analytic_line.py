from odoo import models, fields, api

class AnalyticLine(models.Model):
    _inherit='account.analytic.line'

    estimated_sale_amount=fields.Monetary(string='Importe estimado venta',
                                       compute='_compute_estimated_sale_amount',currency_field='currency_id',
                                       store=True)
    
    @api.depends('unit_amount','employee_id.estimated_sale_price')

    def _compute_estimated_sale_amount(self):
        for line in self:
            price= line.employee_id.estimated_sale_price or 0.0
            qty=line.unit_amount or 0.0
            line.estimated_sale_amount= price * qty
