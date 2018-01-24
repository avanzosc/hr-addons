# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_analytic_entries_count(self):
        for employee in self.filtered(lambda x: x.account_analytic_id):
            cond = [('account_id', '=', employee.account_analytic_id.id)]
            employee.analytic_entries_count = len(
                self.env['account.analytic.line'].search(cond))

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic account')
    analytic_entries_count = fields.Integer(
        string='Analytic entries', compute='_compute_analytic_entries_count')

    def show_analytic_entries_from_employee(self):
        res = {}
        if self.account_analytic_id:
            cond = [('account_id', '=', self.account_analytic_id.id)]
            lines = self.env['account.analytic.line'].search(cond)
            res = {'view_mode': 'tree,form,graph,pivot',
                   'res_model': 'account.analytic.line',
                   'view_id': False,
                   'type': 'ir.actions.act_window',
                   'view_type': 'form',
                   'domain': [('id', 'in', lines.ids)]}
        return res
