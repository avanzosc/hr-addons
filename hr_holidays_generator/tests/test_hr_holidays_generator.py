# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from dateutil.relativedelta import relativedelta
from openerp import fields


class TestHrHolidaysGenerator(common.TransactionCase):

    def setUp(self):
        super(TestHrHolidaysGenerator, self).setUp()
        self.status = self.browse_ref('hr_holidays.holiday_status_cl')
        self.status.vacations_automatically = True
        self.partner = self.env['res.partner'].create({
            'name': 'Partner for test hr automatic holidays',
            'email': 'automaticholidays@odoo.com'})
        self.employee = self.browse_ref('hr.employee_al')
        self.employee.write({'birthday': fields.Date.today(),
                             'address_home_id': self.partner.id})
        date_start = fields.Date.from_string(fields.Date.today())
        date_start -= relativedelta(months=1)
        date_end = date_start
        date_start = date_start.replace(day=10)
        date_end = date_end.replace(day=25)
        contract_vals = {'name': 'New contract for employee',
                         'employee_id': self.employee.id,
                         'wage': 1000,
                         'date_start': fields.Date.to_string(date_start),
                         'date_end': fields.Date.to_string(date_end)}
        self.contract = self.env['hr.contract'].create(contract_vals)
        self.env.user.company_id.days_per_month_worked = 2

    def test_hr_holidays_generator(self):
        self.env['hr.contract'].automatic_holidays_per_month_worked()
        cond = [('employee_id', '=', self.contract.employee_id.id),
                ('holiday_type', '=', 'employee'),
                ('type', '=', 'add')]
        holiday = self.env['hr.holidays'].search(cond, limit=1)
        self.assertEqual(
            holiday.number_of_days_temp, 1.1, 'Bad holidays generated')
