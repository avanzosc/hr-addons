# -*- coding: utf-8 -*-
# © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields, exceptions


class TestCalendarHolidayProjectTimesheet(common.TransactionCase):

    def setUp(self):
        super(TestCalendarHolidayProjectTimesheet, self).setUp()
        self.contract_model = self.env['hr.contract']
        self.calendar_model = self.env['res.partner.calendar']
        self.calendar_day_model = self.env['res.partner.calendar.day']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.line_model = self.env['account.analytic.line']
        self.today = fields.Date.from_string(fields.Date.today())
        self.partner = self.env['res.partner'].create({
            'name': 'Partner',
        })
        self.user = self.env['res.users'].create({
            'partner_id': self.partner.id,
            'login': 'user',
            'password': 'pass',
        })
        employee_model = self.env['hr.employee']
        employee_vals = {
            'name': 'Test Employee',
            'user_id': self.user.id,
        }
        employee_vals.update(
            employee_model.onchange_user(
                user_id=employee_vals['user_id'])['value'])
        self.employee = employee_model.create(employee_vals)
        contract_vals = {
            'name': 'Test Employee Contract',
            'date_start': self.today.replace(month=1, day=1),
            'date_end': self.today.replace(
                year=self.today.year+1, month=12, day=31),
            'employee_id': self.employee.id,
            'wage': 500,
            'working_hours': self.ref('resource.timesheet_group1')}
        self.contract = self.contract_model.create(contract_vals)
        project_vals = {'name': 'test project',
                        'use_tasks': True,
                        'tasks': [(0, 0, {'name': 'test task'})]}
        self.project = self.env['project.project'].create(project_vals)
        account_vals = {'name': 'test analytic account',
                        'type': 'normal'}
        self.analytic_account = self.env['account.analytic.account'].create(
            account_vals)
        account_vals = {'code': 'test',
                        'name': 'test',
                        'type': 'other',
                        'user_type': 1}
        self.account = self.env['account.account'].create(account_vals)

    def test_calendar_holiday_project_task(self):
        cond = [('partner', '=', self.contract.partner.id),
                ('year', '=', self.today.year)]
        calendar = self.calendar_model.search(cond)
        self.assertEquals(len(calendar), 0)
        wiz = self.wiz_model.with_context(
            active_id=self.contract.id).create({})
        self.assertEquals(
            wiz.year, fields.Date.from_string(self.contract.date_start).year)
        wiz.button_calculate_workables_and_festives()
        cond = [('partner', '=', self.contract.partner.id),
                ('date', '=', self.today.replace(month=6, day=30))]
        day = self.calendar_day_model.search(cond, limit=1)
        day.unlink()
        line_vals = {
            'name': 'Test analytic line',
            'date': self.today.replace(month=6, day=30),
            'account_id': self.analytic_account.id,
            'user_id': self.employee.user_id.id,
            'unit_amount': 33,
            'product_uom_id': self.env.ref('product.product_uom_hour').id,
            'general_account_id': self.account.id}
        with self.assertRaises(exceptions.Warning):
            self.line_model.create(line_vals)
        wiz.button_calculate_workables_and_festives()
        self.employee.address_home_id = False
        with self.assertRaises(exceptions.Warning):
            self.line_model.create(line_vals)
        self.employee.address_home_id = self.partner.id
        wiz.button_calculate_workables_and_festives()
        self.line_model.create(line_vals)
        cond = [('partner', '=', self.contract.partner.id),
                ('date', '=', self.today.replace(month=6, day=30))]
        day = self.calendar_day_model.search(cond, limit=1)
        self.assertEquals(
            len(day), 1, 'Calendar day with imputation not found')
        self.assertEquals(
            day.account_analytic_line_real_hours, 99.00,
            'Bad analytic imputation')
        wiz.button_calculate_workables_and_festives()
        cond = [('partner', '=', self.contract.partner.id),
                ('date', '=', self.today.replace(month=6, day=30))]
        day = self.calendar_day_model.search(cond, limit=1)
        self.assertEquals(
            len(day), 1, 'Calendar day with imputation not found(2)')
        self.assertEquals(
            day.account_analytic_line_real_hours, 99.00,
            'Bad analytic imputation(2)')
