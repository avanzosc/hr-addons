# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartnerCalendarDay(models.Model):
    _inherit = 'res.partner.calendar.day'

    @api.multi
    @api.depends('account_analytic_line_ids', 'account_analytic_line_ids.date',
                 'account_analytic_line_ids.unit_amount')
    def _compute_account_analytic_line_real_hours(self):
        for day in self:
            day.account_analytic_line_real_hours = sum(
                day.mapped('account_analytic_line_ids.unit_amount'))

    account_analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line',
        inverse_name='partner_calendar_day_id', string='Analytic lines')
    account_analytic_line_real_hours = fields.Float(
        string="Real hours from analytic_lines",
        compute='_compute_account_analytic_line_real_hours', store=True)
