# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models
from psycopg2.extensions import AsIs


class ResPartnerSupervisedEmployee(models.Model):
    _name = 'res.partner.supervised.employee'
    _inherit = 'education.group.report'
    _description = 'Tutored Report'
    _auto = False

    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Supervised Proffesor")

    _depends = {
        'education.group': [
            'center_id', 'course_id', 'group_type_id', 'academic_year_id',
            'student_ids',
        ],
    }

    # def _coalesce(self):
    #     return super(ResPartnerSupervisedEmployee, self)._coalesce()

    def _select(self):
        select_str = """
                , tutor.teacher_id AS employee_id
        """
        return super(ResPartnerSupervisedEmployee, self)._select() + select_str

    def _from(self):
        from_str = """
                LEFT JOIN hr_employee_supervised_year tutor
                ON tutor.student_id = stu.id
                AND tutor.school_year_id = grp.academic_year_id
        """
        return super(ResPartnerSupervisedEmployee, self)._from() + from_str

    def _group_by(self):
        group_by_str = """
                , tutor.teacher_id
        """
        return (super(ResPartnerSupervisedEmployee, self)._group_by() +
                group_by_str)

    @api.model_cr
    def init(self):
        # self._table = education_group_student_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()), AsIs(self._from()),
                AsIs(self._group_by()),))
