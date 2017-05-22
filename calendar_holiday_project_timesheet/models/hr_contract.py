# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def _generate_calendar_from_wizard(self, year):
        analytic_line_obj = self.env['account.analytic.line']
        day_obj = self.env['res.partner.calendar.day']
        super(HrContract, self)._generate_calendar_from_wizard(year)
        for contract in self:
            date_from = '{}-01-01'.format(year)
            date_to = '{}-12-31'.format(year)
            user_id = contract.employee_id.user_id
            cond = [('user_id', '=', user_id.id),
                    ('date', '>=', date_from),
                    ('date', '<=', date_to),
                    ('journal_id', '=',
                     user_id._find_employee_for_user().journal_id.id),
                    ('product_uom_id', '=',
                     self.env.ref('product.product_uom_hour').id)]
            for line in analytic_line_obj.search(cond):
                cond = [('partner', '=', contract.partner.id),
                        ('date', '=', line.date)]
                line.partner_calendar_day_id = day_obj.search(
                    cond, limit=1).id
