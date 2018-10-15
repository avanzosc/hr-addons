# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    days_per_month_worked = fields.Float(
        string='Days per month worked', digits=(2, 1))
