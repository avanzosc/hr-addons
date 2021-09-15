# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestHrEmployeeDepartureReason(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestHrEmployeeDepartureReason, cls).setUpClass()
        cls.wizard_obj = cls.env['hr.departure.wizard']
        cls.employee_obj = cls.env['hr.employee']
        cls.employee = cls.employee_obj.search([], limit=1)

    def test_hr_departure_wizard(self):
        wizard = self.wizard_obj.with_context(
            active_id=self.employee.id).create({})
        with self.assertRaises(ValidationError):
            wizard.action_register_departure()
