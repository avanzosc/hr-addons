# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields


class TestHrAutomaticCongratulateBirthday(common.TransactionCase):

    def setUp(self):
        super(TestHrAutomaticCongratulateBirthday, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner for test hr automatic congratulate birthday',
            'email': 'emailfortest@odoo.com'})
        self.employee = self.browse_ref('hr.employee_al')
        self.employee.write({'birthday': fields.Date.today(),
                             'address_home_id': self.partner.id})
        contract_vals = {'name': 'New contract for employee',
                         'employee_id': self.employee.id,
                         'wage': 1000,
                         'date_start': '2018-01-01'}
        self.contract = self.env['hr.contract'].create(contract_vals)

    def test_hr_automatic_congratulate_birthday(self):
        self.env['hr.employee'].automatic_congratulate_employee_birthday()
        cond = [('body_html', 'ilike', '%<p>We wish you a very happy birthday'
                 ' and have a great day with yours.</p>%')]
        mail = self.env['mail.mail'].search(cond, limit=1)
        self.assertEqual(len(mail), 1)
