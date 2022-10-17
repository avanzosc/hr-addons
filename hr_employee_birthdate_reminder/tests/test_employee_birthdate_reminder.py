# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestEmployeeBirthdateCommon
from odoo.tests import common
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestEmployeeBirthdate(TestEmployeeBirthdateCommon):

    def test_today_birthdate(self):
        bday_employees = self.employee_obj.search([
            ("birthday_today", "=", self.today),
        ])
        self.assertTrue(self.bday_today.birthday_today)
        self.assertIn(self.bday_today, bday_employees)

    def test_next_week_birthdays(self):
        employees = self.employee_obj.next_week_birthday()
        birthday_dates = employees.mapped("birthday")
        self.assertTrue(len(employees) >= 7)
        min_date = min(birthday_dates)
        self.assertEquals(min_date, self.today + relativedelta(days=1))
        max_date = max(birthday_dates)
        self.assertEquals(max_date, self.today + relativedelta(days=7))
