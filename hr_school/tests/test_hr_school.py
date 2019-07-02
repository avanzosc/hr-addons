# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestHrSchool(TransactionCase):

    def setUp(self):
        super(TestHrSchool, self).setUp()
        year_vals = {'name': '2019aaaaa',
                     'date_start': '2019-01-01',
                     'date_end': '2019-12-31'}
        self.year = self.env['education.academic_year'].create(year_vals)
        self.employee = self.env.ref('hr.employee_al')
        self.employee.user_id = 1
        self.student = self.env.ref('base.res_partner_address_2')
        tutored_vals = {'school_year_id': self.year.id,
                        'teacher_id': self.employee.id,
                        'student_id': self.student.id}
        self.tutored = self.env['hr.employee.supervised.year'].create(
            tutored_vals)

    def test_hr_scholl(self):
        self.assertEqual(self.employee.count_tutored_students, 1)
        res = self.employee.button_show_tutored_students()
        domain = [('teacher_id', '=', [self.employee.id])]
        self.assertEqual(res.get('domain'), domain)
        self.assertEqual(self.student.allowed_user_ids, self.employee.user_id)
        res = self.tutored.name_get()[0]
        lit = u"Academic year: {}, teacher: {}, student: {}".format(
            self.tutored.school_year_id.name, self.tutored.teacher_id.name,
            self.tutored.student_id.name)
        self.assertIn(lit, str(res))
