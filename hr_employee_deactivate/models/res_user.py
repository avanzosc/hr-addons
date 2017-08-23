# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def write(self, values):
        employee_obj = self.env['hr.employee']
        res = super(ResUsers, self).write(values)
        if ('active' in values and not
                self.env.context.get('update_active_from_employee', False)):
            for user in self:
                cond = [('user_id', '=', user.id),
                        '|', ('active', '=', False),
                        ('active', '=', True)]
                employee = employee_obj.search(cond, limit=1)
                if employee:
                    employee.with_context(update_active_from_user=True).write(
                        {'active': values.get('active')})
        return res
