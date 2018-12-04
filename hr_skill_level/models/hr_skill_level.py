# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class Hr_Skill_level(models.Model):
    _inherit = 'hr.skill'

    level = fields.Selection(
        selection=[('1', '1'),
                   ('2', '2'),
                   ('3', '3')], string='Level')
