# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def create_condition_to_search_hr_expense(self):
        cond, employee = super(
            AccountAnalyticLine, self).create_condition_to_search_hr_expense()
        if ('default_track_id' in self.env.context and
                self.env.context.get('default_track_id', False)):
            cond.append(('track_id', '=',
                         self.env.context.get('default_track_id').id))
        return cond, employee

    def catch_values_for_create_expense(self):
        vals = super(
            AccountAnalyticLine,
            self).catch_values_for_create_expense()
        if ('default_track_id' in self.env.context and
                self.env.context.get('default_track_id', False)):
            vals['track_id'] = self.env.context.get('default_track_id').id
        return vals
