# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
