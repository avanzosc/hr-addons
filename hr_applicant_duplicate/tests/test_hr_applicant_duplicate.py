# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestHrApplicantDuplicate(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestHrApplicantDuplicate, cls).setUpClass()
        applicant_obj = cls.env['hr.applicant']
        cls.applicant1 = applicant_obj.create({
            'name': 'aaaa',
            'partner_mobile': '11111',
            'partner_phone': '22222',
            'active': True,
        })
        cls.applicant2 = applicant_obj.create({
            'name': 'bbbb',
            'email_from': 'bbbb@gmail.com',
            'active': False,
        })

    def test_hr_applicant_duplicate(self):
        with self.assertRaises(ValidationError):
            self.applicant1.email_from = self.applicant2.email_from
        with self.assertRaises(ValidationError):
            self.applicant2.partner_mobile = self.applicant1.partner_mobile
        with self.assertRaises(ValidationError):
            self.applicant2.partner_phone = self.applicant1.partner_phone
