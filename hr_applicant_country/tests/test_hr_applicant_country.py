# -*- coding: utf-8 -*-
# (Copyright) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHrApplicantCountry(common.TransactionCase):

    def setUp(self):
        super(TestHrApplicantCountry, self).setUp()
        self.country = self.env['res.country'].create(
            {'name': 'Country for test hr applicant country'})
        self.partner = self.env['res.partner'].create(
            {'name': 'Partner for test hr applicant country',
             'country_id': self.country.id,
             'nationality_id': self.country.id,
             'birthdate_date': '1969-01-01'})
        self.application = self.env['hr.applicant'].create(
            {'name': 'Applicant for test hr applicant country',
             'partner_id': self.partner.id})

    def test_hr_applicant_country(self):
        res = self.application.onchange_partner_id(self.partner.id)
        values = res.get('value')
        country_id = values.get('contact_country_id')
        self.assertEqual(
            country_id, self.country.id, 'Bad country for application contact')
        self.assertEqual(
            values.get('nationality_id'), self.country.id,
            'Bad nationality for application contact')
        self.assertEqual(
            values.get('birthdate_date'), '1969-01-01',
            'Bad birthdate for application contact')
