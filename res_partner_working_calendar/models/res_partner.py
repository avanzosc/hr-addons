# -*- coding: utf-8 -*-
# Copyright 2018 Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'


    working_calendar_ids = fields.Many2one(comodel_name="resource.calendar",
                                           string="Working calendar")
