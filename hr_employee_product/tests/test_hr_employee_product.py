# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestHrEmployeeProduct(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeProduct, self).setUp()
        self.line_obj = self.env['account.analytic.line']
        self.employee = self.browse_ref('hr.employee_al')
        self.employee2 = self.browse_ref('hr.employee_mit')
        self.product = self.browse_ref('product.product_product_11c')
        self.product2 = self.browse_ref('product.service_order_01')
        self.employee.product_id = self.product
        self.employee2.product_id = self.product2
        self.account = self.env['account.analytic.account'].create({
            'name': 'Analytic account for employee'})

    def test_hr_employee_product(self):
        line_vals = {'employee_id': self.employee.id,
                     'name': self.employee.name,
                     'account_id': self.account.id,
                     'unit_amount': 2}
        line = self.line_obj.create(line_vals)
        self.assertEqual(
            line.product_id, self.employee.product_id,
            'Bad product in employee analytic line')
        line.employee_id = self.employee2
        self.assertEqual(
            line.product_id, self.employee2.product_id,
            'Bad product in employee analytic line(2)')
