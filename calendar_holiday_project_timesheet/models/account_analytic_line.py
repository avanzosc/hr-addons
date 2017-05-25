# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_calendar_day_id = fields.Many2one(
        comodel_name='res.partner.calendar.day',
        string='Employee calendar day')

    @api.model
    def create(self, values):
        line = super(AccountAnalyticLine, self).create(values)
        line._put_analytic_line_in_employee_calendar()
        return line

    @api.multi
    def write(self, values):
        result = super(AccountAnalyticLine, self).write(values)
        if not self.env.context.get('update_line_with_day', False):
            self._put_analytic_line_in_employee_calendar()
        return result

    @api.multi
    def _put_analytic_line_in_employee_calendar(self):
        day_obj = self.env['res.partner.calendar.day']
        lines = self.filtered(
            lambda x: x.partner_calendar_day_id and
            (not x.product_uom_id or not x.user_id or not x.journal_id or
             (x.product_uom_id and x.product_uom_id != self.env.ref(
                 'product.product_uom_hour')) or
             (x.journal_id and x.user_id and x.journal_id !=
              x.user_id._find_employee_for_user().journal_id)))
        lines2 = self.filtered(
            lambda x: not x.partner_calendar_day_id and
            x.product_uom_id and x.user_id and x.journal_id and
            x.product_uom_id == self.env.ref('product.product_uom_hour') and
            x.user_id._find_employee_for_user().journal_id == x.journal_id)
        for line in lines2:
            cond = [('partner', '=', line.user_id.partner_id.id),
                    ('date', '=', line.date)]
            day = day_obj.search(cond, limit=1)
            if not day:
                raise exceptions.Warning(
                    _("Calendar day not found for employee '%s'.") %
                    line.user_id.partner_id.name)
            line.with_context(update_line_with_day=True).write(
                {'partner_calendar_day_id': day.id})
        lines.with_context(update_line_with_day=True).write(
            {'partner_calendar_day_id': False})
