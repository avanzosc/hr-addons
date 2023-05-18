# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged
from odoo import fields
from dateutil.relativedelta import relativedelta


@tagged("post_install", "-at_install")
class TestHrTimesheetSheetWithoutExpense(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestHrTimesheetSheetWithoutExpense, cls).setUpClass()
        vals = {'name': 'User hr timesheet sheet without expense',
                'login': 'hrtimesheetsheetwithoutexpense@avanzosc.es'}
        user = cls.env['res.users'].create(vals)
        vals = {'name': 'employee hr timesheet sheet without expense',
                'user_id': user.id}
        cls.employee = cls.env['hr.employee'].create(vals)
        vals = {
            'employee_id': cls.employee.id,
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + relativedelta(days=+30)}
        cls.timesheet = cls.env['hr_timesheet.sheet'].create(vals)

    def test_hr_timesheet_sheet_without_expense(self):
        my_cond = ", '|', ('product_id', '=', False), "
        "('product_id.can_be_expensed', '=', False)"
        cond = self.timesheet._get_timesheet_sheet_lines_domain()
        self.assertIn(my_cond, str(cond))
