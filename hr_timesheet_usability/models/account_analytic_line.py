# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    # sale_team_id = fields.Many2one(
    #     comodel_name='crm.team', string='Sale team',
    #     related='move_id.invoice_id.team_id')  # sale module required
