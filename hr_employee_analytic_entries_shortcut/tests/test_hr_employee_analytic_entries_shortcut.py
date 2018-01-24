# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestHrEmployeeAnalyticEntriesShortcut(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeAnalyticEntriesShortcut, self).setUp()
        self.account = self.env['account.analytic.account'].create({
            'name': 'Analytic account for employee'})
        self.employee = self.browse_ref('hr.employee_al')
        self.employee.account_analytic_id = self.account
        self.line = self.env['account.analytic.line'].create({
            'name': 'Analytic entrie for employee',
            'account_id': self.account.id})

    def test_hr_employee_analytic_entries_shortcut(self):
        self.assertEqual(
            self.employee.analytic_entries_count, 1,
            'BAD entries number for employee')
        result = self.employee.show_analytic_entries_from_employee()
        domain = "[('id', 'in', [{}])]".format(self.line.id)
        self.assertEqual(
            str(result.get('domain')), domain, 'BAD domain from employee')
