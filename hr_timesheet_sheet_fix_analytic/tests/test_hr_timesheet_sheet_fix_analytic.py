# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo import fields


@common.at_install(False)
@common.post_install(True)
class TestHrTimesheetSheetFixAnalytic(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHrTimesheetSheetFixAnalytic, cls).setUpClass()
        cls.analytic_line_obj = cls.env['account.analytic.line']
        cls.partner = cls.env.ref("base.partner_admin")
        cond = [('partner_id', '=', cls.partner.id)]
        cls.user = cls.env['res.users'].search(cond)
        cond = [('user_id', '=', cls.user.id)]
        cls.employee = cls.env['hr.employee'].search(cond)
        vals = {'employee_id': cls.employee.id,
                'date_start': fields.Date.today(),
                'date_end': fields.Date.today()}
        cls.sheet = cls.env['hr_timesheet.sheet'].create(vals)
        cond = [('move_id', '=', False)]
        cls.analytic_line = cls.analytic_line_obj.search(cond, limit=1)
        cls.analytic_line.write({
            'date': fields.Date.today(),
            'sheet_id': cls.sheet.id})
        cls.journal = cls.env['account.journal'].search([], limit=1)
        cls.account = cls.env['account.account'].search([], limit=1)
        vals = {'date': fields.Date.today(),
                'ref': 'aaaaaaaa',
                'journal_id': cls.journal.id}
        line_vals = {'account_id': cls.account.id}
        vals['line_ids'] = [(0, 0, line_vals)]
        cls.account_move = cls.env['account.move'].create(vals)

    def test_hr_timesheet_sheet_fix_analytic(self):
        cond = self.sheet._get_timesheet_sheet_lines_domain()
        lines = self.analytic_line_obj.search(cond)
        self.assertEquals(len(lines), 1)
        self.analytic_line.move_id = self.account_move.line_ids[0].id
        cond = self.sheet._get_timesheet_sheet_lines_domain()
        lines = self.analytic_line_obj.search(cond)
        self.assertEquals(len(lines), 0)
