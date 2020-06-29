# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from .common import TestHrSchoolCommon
from odoo import _
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestHrSchool(TestHrSchoolCommon):

    def test_hr_school(self):
        tutored = self.tutored_model.create(self.tutored_vals)
        self.assertEqual(self.teacher.count_tutored_students, 1)
        res = self.teacher.button_show_tutored_students()
        self.assertIn(('teacher_id', '=', self.teacher.id),
                      res.get('domain'))
        self.assertIn(self.teacher.user_id, self.student.allowed_user_ids)
        lit = _(u"Academic year: {}, teacher: {}, student: {}").format(
            tutored.school_year_id.name, tutored.teacher_id.name,
            tutored.student_id.name)
        self.assertIn(lit, tutored.display_name)

    def test_hr_school_wizard(self):
        wiz_vals = {'school_year_id': self.academic_year.id,
                    'teacher_id': self.teacher.id}
        wiz = self.wiz_model.create(wiz_vals)
        wiz.with_context(
            active_ids=self.student.ids).button_create_relationship()
        self.assertEqual(self.teacher.count_tutored_students, 1)
