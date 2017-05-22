# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def _find_employee_for_user(self):
        employee_obj = self.env['hr.employee']
        cond = [('address_home_id', '=', self.partner_id.id)]
        employee = employee_obj.search(cond, limit=1)
        if not employee:
            raise exceptions.Warning(
                _("Employee not found for user: '%s'.") % self.name)
        return employee
