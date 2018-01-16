# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('user_id')
    def _onchange_user(self):
        result = super(HrEmployee, self)._onchange_user()
        if self.user_id and self.user_id.partner_id:
            self.address_home_id = self.user_id.partner_id.id
        return result

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)
        if employee.address_home_id:
            employee.address_home_id.employee_id = employee.id
        return employee

    @api.multi
    def write(self, vals):
        result = super(HrEmployee, self).write(vals)
        if vals.get('address_home_id', False):
            for employee in self:
                employee.address_home_id.employee_id = employee.id
        return result
