# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
from dateutil.relativedelta import relativedelta
import calendar


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def automatic_holidays_per_month_worked(self):
        expired_stage = self.env.ref(
            'hr_contract_stages.stage_contract3', False)
        cond = [('vacations_automatically', '=', True)]
        holiday_status = self.env['hr.holidays.status'].search(cond, limit=1)
        today = fields.Date.from_string(fields.Date.today())
        today -= relativedelta(months=1)
        lastday = calendar.monthrange(today.year, today.month)[1]
        first_day = today.replace(day=1)
        last_day = today.replace(day=lastday)
        cond = [('contract_stage_id', '!=', expired_stage.id),
                ('date_start', '<', fields.Date.to_string(last_day))]
        contracts = self.search(cond)
        for c in contracts:
            days = (
                c.employee_id.address_home_id.company_id.days_per_month_worked)
            start = (first_day if fields.Date.from_string(c.date_start) <
                     first_day else fields.Date.from_string(c.date_start))
            end = last_day
            if (c.date_end and fields.Date.from_string(c.date_end) >=
                first_day and fields.Date.from_string(c.date_end) <=
                    last_day):
                end = fields.Date.from_string(c.date_end)
            worked_days = int(end.day) - int(start.day) + 1
            d = days
            if worked_days != lastday:
                d = round((worked_days * days) / lastday, 1)
            vals = c._catch_contract_information_for_holidays(
                holiday_status, first_day, d)
            self.env['hr.holidays'].create(vals)

    @api.multi
    def _catch_contract_information_for_holidays(
            self, holiday_status, date, days):
        name = u"{}: {} {}".format(
            _('Holidays'), date.year, date.strftime("%B").lower().capitalize())
        vals = {'name': name,
                'holiday_status_id': holiday_status.id,
                'holiday_type': 'employee',
                'employee_id': self.employee_id.id,
                'number_of_days_temp': days,
                'type': 'add'}
        return vals


class HrHolidaysStatus(models.Model):
    _inherit = 'hr.holidays.status'

    vacations_automatically = fields.Boolean(
        string='To generate vacations automatically')
