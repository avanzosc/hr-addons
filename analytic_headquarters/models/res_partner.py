# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    headquarters_id = fields.Many2one(comodel_name='res.headquarters',
                                      string='Headquarters')
