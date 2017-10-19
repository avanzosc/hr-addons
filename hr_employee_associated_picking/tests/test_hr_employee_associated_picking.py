# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHrEmployeeAssociatedPicking(common.TransactionCase):

    def setUp(self):
        super(TestHrEmployeeAssociatedPicking, self).setUp()
        employee_model = self.env['hr.employee']
        employee_vals = {
            'name': 'employee name',
            'user_id': self.ref('base.user_root'),
        }
        employee_vals.update(
            employee_model.onchange_user(
                user_id=employee_vals['user_id'])['value'])
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
