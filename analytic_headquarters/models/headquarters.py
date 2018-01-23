# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResHeadquarters(models.Model):

    _name = 'res.headquarters'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name', required=True)
