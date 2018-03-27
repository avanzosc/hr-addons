# -*- coding: utf-8 -*-
# (Copyright) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nationality_id = fields.Many2one(
        comodel_name='res.country', string='Nationality')
