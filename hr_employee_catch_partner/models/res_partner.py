# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee')
