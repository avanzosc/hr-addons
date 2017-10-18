# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields, exceptions


class TestCalendarHoliday(common.TransactionCase):

    def setUp(self):
        super(TestCalendarHoliday, self).setUp()
        self.holiday_model = self.env['calendar.holiday']
        self.contract_model = self.env['hr.contract']
        self.calendar_model = self.env['res.partner.calendar']
        self.calendar_day_model = self.env['res.partner.calendar.day']
        self.wiz_model = self.env['wiz.calculate.workable.festive']
        self.holidays_model = self.env['hr.holidays']
        self.today = fields.Date.from_string(fields.Date.today())
        self.partner = self.env['res.partner'].create({
            'name': 'Partner',
        })
        self.partner2 = self.env['res.partner'].create({
            'name': 'Partner 2',
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
        calendar_line_vals = {
            'date': self.today.replace(month=1, day=6),
            'absence_type': self.ref('hr_holidays.holiday_status_comp'),
        }
        calendar_vals = {
            'name': 'Holidays calendar',
            'lines': [(0, 0, calendar_line_vals)],
        }
        self.calendar_holiday = self.holiday_model.create(calendar_vals)
        contract_vals = {
            'name': 'Test Employee Contract',
            'date_start': self.today.replace(month=1, day=2),
            'date_end': self.today.replace(month=12, day=30),
            'employee_id': self.employee.id,
            'wage': 500,
            'working_hours': self.ref('resource.timesheet_group1'),
            'holiday_calendars': [(6, 0, [self.calendar_holiday.id])],
        }
        self.contract = self.contract_model.create(contract_vals)
        date_from = '{}-02-02 08:00:00'.format(self.today.year)
        date_to = '{}-02-05 18:00:00'.format(self.today.year)
        hr_holidays_vals = {'name': 'Employee holidays',
                            'holiday_type': 'employee',
                            'holiday_status_id':
                            self.ref('hr_holidays.holiday_status_comp'),
                            'employee_id': self.employee.id,
                            'date_from': date_from,
                            'date_to': date_to,
                            'number_of_days_temp': 4}
        self.hr_holidays = self.holidays_model.create(hr_holidays_vals)

    def test_calendar_holiday(self):
        self.contract.write({})
        cond = [('partner', '=', self.contract.partner.id),
                ('year', '=', self.today.year)]
        calendar = self.calendar_model.search(cond)
        self.assertEquals(len(calendar), 0)
        wiz = self.wiz_model.with_context(
            active_id=self.contract.id).create({'year': 2000})
        with self.assertRaises(exceptions.Warning):
            wiz.button_calculate_workables_and_festives()
        wiz.year = self.today.year+5
        with self.assertRaises(exceptions.Warning):
            wiz.button_calculate_workables_and_festives()
        wiz.year = 0
        self.wiz_model.with_context(
            active_id=self.contract.id).default_get([])
        wiz.year = self.today.year
        wiz.button_calculate_workables_and_festives()
        self.wiz_model.with_context(
            active_id=self.contract.id).default_get([])
        self.assertEquals(
            wiz.year, fields.Date.from_string(self.contract.date_start).year)
        calendar = self.calendar_model.search(cond)
        self.assertNotEquals(len(calendar), 0)
        with self.assertRaises(exceptions.Warning):
            self.partner2._generate_festives_in_calendar(self.today.year,
                                                         self.calendar_holiday)
        self.hr_holidays.signal_workflow('validate')
        date_from = '{}-01-01'.format(self.today.year)
        date_to = '{}-12-31'.format(self.today.year)
        cond = [('date', '>=', date_from),
                ('date', '<=', date_to),
                ('absence_type', '=',
                 self.ref('hr_holidays.holiday_status_comp')),
                ('partner', '=', self.employee.address_home_id.id)]
        days = self.calendar_day_model.search(cond)
        self.assertEquals(
            len(days), 5, 'Employee calendar holiday days not found(1)')
        wiz.button_calculate_workables_and_festives()
        days = self.calendar_day_model.search(cond)
        self.assertEquals(
            len(days), 5, 'Employee calendar holiday days not found(2)')
        self.hr_holidays.signal_workflow('refuse')
        days = self.calendar_day_model.search(cond)
        self.assertEquals(
            len(days), 1, 'Employee with holiday days')
        wiz2 = self.wiz_model.with_context(active_id=self.contract.id).create(
            {'year': fields.Date.from_string(self.contract.date_end).year})
        wiz2.button_calculate_workables_and_festives()
        date_from = str(fields.Datetime.from_string(
            fields.Datetime.now()).replace(month=1, day=1))
        vals = self.holidays_model.onchange_date_from(
            False, date_from, self.employee.id)
        date_to = str(fields.Datetime.from_string(
            fields.Datetime.now()).replace(month=1, day=7))
        date_from = str(fields.Datetime.from_string(
            fields.Datetime.now()).replace(month=1, day=1))
        vals = self.holidays_model.onchange_date_from(
            date_to, date_from, self.employee.id)
        days = int(vals['value'].get('number_of_days_temp'))
        self.assertEqual(days, 6, 'Absent days(1) badly calculated')
        vals = self.holidays_model.onchange_date_to(
            date_to, date_from, self.employee.id)
        days = int(vals['value'].get('number_of_days_temp'))
        self.assertEqual(days, 6, 'Absent days(2) badly calculated')
        vals = self.holidays_model.onchange_employee(
            self.employee.id, date_to, date_from)
        days = int(vals['value'].get('number_of_days_temp'))
        self.assertEqual(days, 6, 'Absent days(3) badly calculated')
        cond = [('calendar', '=', calendar.id),
                ('partner', '=', self.partner.id),
                ('date', '=', self.today.replace(month=1, day=6))]
        self.calendar_day_model.search(cond, limit=1). unlink()
        with self.assertRaises(exceptions.Warning):
            self.partner._generate_festives_in_calendar(self.today.year,
                                                        self.calendar_holiday)
        self.employee.address_home_id = False
        res = self.hr_holidays._remove_holidays(
            20, False, False, self.employee.id)
        self.assertEqual(res, 20, 'Bad days of employee without partner')

    def test_calendar_holiday_calendar_Scheduler(self):
        self.contract.write({
            'date_start': self.today.replace(
                year=self.today.year + 1, month=1, day=2),
            'date_end': self.today.replace(
                year=self.today.year + 1, month=12, day=30),
        })
        self.contract.automatic_process_generate_calendar()
        cond = [('partner', '=', self.contract.partner.id)]
        calendars = self.calendar_model.search(cond)
        self.assertEquals(
            len(calendars), 1, 'Calendar no generated for employee')
