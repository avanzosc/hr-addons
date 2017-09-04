# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHrEmployeeDeactivate(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeDeactivate, self).setUp()
        user_vals = {'name': 'Odoo user',
                     'login': 'odoouser@odoo.com'}
        self.user = self.env['res.users'].create(user_vals)
        employee_vals = {'name': 'Odoo employee',
                         'user_id': self.user.id}
        self.employee = self.env['hr.employee'].create(employee_vals)

    def test_hr_employee_deactivate(self):
        self.user.active = False
        self.assertEquals(self.employee.active, False,
                          'Employee is not deactive')
        self.user.active = True
        self.assertEquals(self.employee.active, True,
                          'Employee is not active')
        self.employee.active = False
        self.assertEquals(self.user.active, False,
                          'User is not deactive')
        self.employee.active = True
        self.assertEquals(self.user.active, True,
                          'User is not active')
