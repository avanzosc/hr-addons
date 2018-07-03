# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class HrContract(models.Model):
    _name = 'hr.contract'
    _inherit = ['hr.contract', 'mail.thread', 'ir.needaction_mixin']

    holiday_calendars = fields.Many2many(
        comodel_name='calendar.holiday', string='Holiday calendars')
    partner = fields.Many2one(
        comodel_name='res.partner', string='Contract employee',
        related='employee_id.address_home_id', store=True)
    calendar_days = fields.One2many(
        comodel_name='res.partner.calendar.day', inverse_name='contract',
        string='Employee calendar days')

    @api.model
    def create(self, vals):
        contract = super(HrContract, self).create(vals)
        if contract.partner:
            contract.message_subscribe(contract.partner.ids)
        return contract

    @api.multi
    def write(self, vals):
        result = super(HrContract, self).write(vals)
        for contract in self.filtered('partner'):
            contract.message_subscribe(contract.partner.ids)
        return result

    @api.multi
    def _generate_calendar_from_wizard(self, year):
        holidays_obj = self.env['hr.holidays']
        date_from = '{}-01-01'.format(year)
        for contract in self:
            contract.partner._generate_calendar(year)
            if (contract.working_hours and
                    contract.working_hours.attendance_ids):
                contract.partner._put_estimated_hours_in_calendar(year,
                                                                  contract)
            if contract.holiday_calendars:
                for calendar in contract.holiday_calendars:
                    contract.partner._generate_festives_in_calendar(year,
                                                                    calendar)
            cond = [('employee_id', '=', contract.employee_id.id),
                    ('type', '=', 'remove'),
                    ('date_to', '>=', date_from),
                    ('state', 'in', ('validate', 'validate1'))]
            for holiday in holidays_obj.search(cond):
                days = holiday._find_calendar_days_from_holidays()
                days.write(self._prepare_partner_day_information(
                    holiday.holiday_status_id.id))
            self._put_contract_in_employee_calendar_day(year)

    def _prepare_partner_day_information(self, absence_type):
        return {'absence_type': absence_type}

    def _put_contract_in_employee_calendar_day(self, year):
        day_obj = self.env['res.partner.calendar.day']
        date_from = '{}-01-01'.format(year)
        date_to = '{}-12-31'.format(year)
        cond = [('employee_id', '=', self.employee_id.id),
                '|', ('date_end', '=', False), ('date_end', '>=', date_from)]
        contracts = self.search(cond)
        for contract in contracts:
            cond = [('partner', '=', contract.partner.id),
                    ('date', '>=', max(date_from, contract.date_start)),
                    ('date', '<=', date_to if not contract.date_end else
                     min(date_to, contract.date_end))]
            days = day_obj.search(cond)
            days.write({'contract': contract.id})

    @api.multi
    def automatic_process_generate_calendar(self):
        contract_obj = self.env['hr.contract']
        date_begin = '{}-01-01'.format(fields.Date.from_string(
            fields.Date.today()).year)
        cond = ['|', ('date_end', '=', False),
                ('date_end', '>=', date_begin)]
        contracts = contract_obj.search(cond)
        for contract in contracts:
            contract._generate_calendar_from_wizard(
                fields.Date.from_string(fields.Date.today()).year)
