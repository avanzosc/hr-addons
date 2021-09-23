# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    hr_expense_ids = fields.One2many(
        string='Expenses', comodel_name='hr.expense', inverse_name='track_id')

    def create_analytic_line_from_track(self, line, employee, vals):
        analytic_line = super(
            EventTrack,
            self).create_analytic_line_from_track(line, employee, vals)
        expense_obj = self.env['hr.expense']
        cond = [('date', '=', self.date.date()),
                ('employee_id', '=', employee.id),
                ('product_id', '=', line.product_id.id),
                ('sale_order_id', '=', line.sale_order_id.id),
                ('track_id', '=', self.id)]
        expense = expense_obj.search(cond)
        if expense:
            expense.unlink()
        expense_vals = self.catch_values_for_create_expense(
            line, employee)
        expense_obj.create(expense_vals)
        return analytic_line

    def catch_values_for_create_expense(self, product_line, employee):
        name = '{}: {}'.format(self.event_id.name, self.name)
        vals = {'name': name,
                'date': self.date.date(),
                'employee_id': employee.id,
                'product_id': product_line.product_id.id,
                'sale_order_id': product_line.sale_order_id.id,
                'track_id': self.id,
                'quantity': 1,
                'unit_amount': product_line.standard_price}
        return vals
