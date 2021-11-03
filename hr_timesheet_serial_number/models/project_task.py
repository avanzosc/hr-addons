# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    lot_id = fields.Many2one(
        string='Lot/Serial Number', comodel_name='stock.production.lot',
        related='sale_line_id.lot_id', store=True)
    sale_order_id = fields.Many2one(
        string='Sale Order', comodel_name='sale.order',
        related='sale_line_id.order_id', store=True)
