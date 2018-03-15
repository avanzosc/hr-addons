# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestHrContractCloseAutomatically(common.TransactionCase):

    def setUp(self):
        super(TestHrContractCloseAutomatically, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner for test hr contract cloese automatically'})
        self.employee = self.browse_ref('hr.employee_al')
        self.employee.address_home_id = self.partner.id
        date_end = fields.Date.to_string(fields.Date.from_string(
            fields.Date.today()) + relativedelta(days=-1))
        contract_vals = {'name': 'New contract for employee',
                         'employee_id': self.employee.id,
                         'wage': 1000,
                         'date_start': '2018-01-01',
                         'date_end': date_end}
        self.contract = self.env['hr.contract'].create(contract_vals)

    def test_hr_contract_close_automatically(self):
        expired_stage = self.env.ref('hr_contract_stages.stage_contract3')
        self.env['hr.contract'].automatic_close_expired_employee_contracts()
        self.assertEqual(
            self.contract.contract_stage_id, expired_stage,
            'Bad automatic contract close')
