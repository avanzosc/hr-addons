# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    product_categ_id = fields.Many2one(
        comodel_name='product.category', string='Product category',
        related='product_id.categ_id', store=True, readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('employee_id', False):
            vals = self._catch_employee_information(vals)
        return super(AccountAnalyticLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('employee_id', False):
            vals = self._catch_employee_information(vals)
        return super(AccountAnalyticLine, self).write(vals)

    def _catch_employee_information(self, vals):
        employee = self.env['hr.employee'].browse(vals.get('employee_id'))
        if employee.product_id:
            vals['product_id'] = employee.product_id.id
        return vals
