# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contacts_school_education.tests.common import \
    TestContactsSchoolEducationCommon


class TestHrSchoolCommon(TestContactsSchoolEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestHrSchoolCommon, cls).setUpClass()
        cls.wiz_model = cls.env["wiz.create.relationship.supervised.year"]
        cls.tutored_model = cls.env["hr.employee.supervised.year"]
        cls.tutored_vals = {
            "school_year_id": cls.academic_year.id,
            "teacher_id": cls.teacher.id,
            "student_id": cls.student.id,
        }
