# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def write(self, values):
        res = super(HrEmployee, self).write(values)
        if ('active' in values and not
                self.env.context.get('update_active_from_user', False)):
            for employee in self.filtered(lambda x: x.user_id):
                employee.user_id.with_context(
                    update_active_from_employee=True).write(
                    {'active': values.get('active')})
        return res
