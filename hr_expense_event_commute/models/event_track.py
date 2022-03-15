# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    hr_expense_ids = fields.One2many(
        string='Expenses', comodel_name='hr.expense', inverse_name='track_id')
