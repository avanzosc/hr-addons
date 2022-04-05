# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    expense_id = fields.Many2one(
        string='Expense', comodel_name='hr.expense')

    @api.model
    def create(self, values):
        line = super(AccountAnalyticLine, self).create(values)
        if line.product_id and line.product_id.can_be_expensed:
            line.create_hr_expense_from_analytic_line()
        return line

    def unlink(self):
        for line in self.filtered(lambda x: x.expense_id):
            line.expense_id.unlink()
        return super(AccountAnalyticLine, self).unlink()

    def create_hr_expense_from_analytic_line(self):
        expense_obj = self.env['hr.expense']
        if self.expense_id:
            self.expense_id.unlink()
        expense_vals = self.catch_values_for_create_expense()
        expense = expense_obj.create(expense_vals)
        self.expense_id = expense.id

    def catch_values_for_create_expense(self):
        cond = [('partner_id', '=', self.partner_id.id)]
        user = self.env['res.users'].search(cond, limit=1)
        cond = [('user_id', '=', user.id)]
        employee = self.env['hr.employee'].search(cond, limit=1)
        vals = {'name': self.name,
                'date': self.date,
                'quantity': 1,
                'unit_amount': self.amount}
        if self.product_id:
            vals['product_id'] = self.product_id.id
        if employee:
            vals['employee_id'] = employee.id
        return vals
