# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    track_id = fields.Many2one(
        string='Event track', comodel_name='event.track')
