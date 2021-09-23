# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventEvent(models.Model):
    _inherit = 'event.event'

    def _catch_sale_lines_for_event_displacement_product(self):
        sale_lines = super(
            EventEvent,
            self)._catch_sale_lines_for_event_displacement_product()
        sales = self.sale_order_lines_ids.mapped('order_id')
        for sale in sales:
            for line in sale.order_line.filtered(
                    lambda x: x.product_id.can_be_expensed):
                if line not in sale_lines:
                    sale_lines += line
        return sale_lines
