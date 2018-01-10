# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestHrEmployeeCatchPartner(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeCatchPartner, self).setUp()
        self.user = self.browse_ref('base.user_root')
        self.user2 = self.browse_ref('base.user_demo')

    def test_hr_employee_catch_partner(self):
        employee_vals = {'name': 'employee name',
                         'user_id':  self.user.id,
                         'address_home_id': self.user.partner_id.id}
        self.employee = self.env['hr.employee'].create(employee_vals)
        self.assertEqual(
            self.employee.address_home_id.employee_id.id, self.employee.id,
            'User without employee')
        self.employee.user_id = self.user2
        self.employee._onchange_user()
        self.assertEqual(
            self.employee.address_home_id, self.user2.partner_id,
            'Employee without partner')
        employee_vals = {'name': 'employee2 name',
                         'user_id':  self.user2.id,
                         'address_home_id': self.user2.partner_id.id}
        self.employee2 = self.env['hr.employee'].create(employee_vals)
        self.employee2.write({'address_home_id': self.user.partner_id.id})
        self.assertEqual(
            self.user2.partner_id.employee_id, self.employee,
            'Bad modification for employee 1')
        self.assertEqual(
            self.user.partner_id.employee_id, self.employee2,
            'Bad modification for employee 2')
        self.employee2.write({'address_home_id': False})
        self.assertEqual(
            len(self.user.partner_id.employee_id), 0,
            'Bad modification(2) for employee 2')
