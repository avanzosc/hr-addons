# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    sale_order_id = fields.Many2one(
        string='Sale Order', comodel_name='sale.order',
        related='task_id.sale_order_id', store=True)
    lot_id = fields.Many2one(
        string='Lot/Serial Number', comodel_name='stock.production.lot',
        related='task_id.lot_id', store=True)
