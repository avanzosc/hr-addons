# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestHrEmployeeAssociatedPicking(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeAssociatedPicking, self).setUp()
        employee_model = self.env['hr.employee']
        self.user = self.browse_ref('base.user_root')
        employee_vals = {
            'name': 'employee name',
            'user_id': self.user.id,
            'address_home_id': self.user.partner_id.id
        }
        self.employee = employee_model.create(employee_vals)

    def test_hr_employee_associated_picking(self):
        self.assertEqual(
            self.employee.picking_count, 0, 'Employee with picking')
        result = self.employee.pickings_from_employee()
        self.assertEquals(
            result.get('type'), 'ir.actions.act_window')
        self.assertEquals(
            result.get('domain'),
            [('partner_id', '=', self.employee.address_home_id.id)])
