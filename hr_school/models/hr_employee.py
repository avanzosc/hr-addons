# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    tutored_student_ids = fields.One2many(
        comodel_name='hr.employee.supervised.year',
        inverse_name='teacher_id', string='Tutored students per year')
    count_tutored_students = fields.Integer(
        string='# Tutored students', compute='_compute_count_tutored_students')

    def _compute_count_tutored_students(self):
        for employee in self:
            employee.count_tutored_students = (
                len(employee.tutored_student_ids))

    @api.multi
    def button_show_tutored_students(self):
        self.ensure_one()
        self = self.with_context(
            search_default_teacher_id=self.id, default_teacher_id=self.id)
        return {'name': _('Tutored students'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'hr.employee.supervised.year',
                'domain': [('id', 'in', self.tutored_student_ids.ids)],
                'context': self.env.context}


class HrEmployeeSupervisedYear(models.Model):
    _name = 'hr.employee.supervised.year'
    _description = 'Tutored by year'

    school_year_id = fields.Many2one(
        string='School year', comodel_name='education.academic_year',
        required=True)
    teacher_id = fields.Many2one(
        string='Teacher', comodel_name='hr.employee',
        required=True)
    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner',
        required=True)
    user_id = fields.Many2one(
        string='User', comodeel_name='res.users', store=True,
        related='teacher_id.user_id')

    @api.multi
    def name_get(self):
        result = []
        for year in self:
            name = _(
                u"Academic year: {}, teacher: {}, student: {}").format(
                    year.school_year_id.name, year.teacher_id.name,
                    year.student_id.name)
            result.append((year.id, name))
        return result
