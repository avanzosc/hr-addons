# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestHrEmployeeCatchPartner(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeCatchPartner, self).setUp()
        self.user = self.browse_ref('base.user_root')
        self.partner = self.browse_ref('base.res_partner_10')

    def test_hr_employee_catch_partner(self):
        employee_vals = {'name': 'employee name',
                         'address_home_id': self.user.partner_id.id}
        self.employee = self.env['hr.employee'].create(employee_vals)
        self.employee.user_id = self.user
        self.employee._onchange_user()
        self.assertEqual(
            self.employee.address_home_id, self.user.partner_id,
            'Employee without partner')
        self.employee.address_home_id = self.partner.id
        self.assertEqual(
            self.partner.employee_id, self.employee,
            'Bad modification for employee 1')
