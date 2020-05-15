# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class WizCreateRelationshipSupervisedYear(models.TransientModel):
    _name = "wiz.create.relationship.supervised.year"
    _description = "Wizard for create relationship in supervised year"

    school_year_id = fields.Many2one(
        string='School year', comodel_name='education.academic_year',
        required=True)
    teacher_id = fields.Many2one(
        string='Teacher', comodel_name='hr.employee',
        required=True)

    @api.multi
    def button_create_relationship(self):
        year_obj = self.env['hr.employee.supervised.year']
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        partners = self.env['res.partner'].browse(active_ids)
        students = partners.filtered(
            lambda x: x.educational_category == 'student')
        for student in students:
            cond = [('school_year_id', '=', self.school_year_id.id),
                    ('teacher_id', '=', self.teacher_id.id),
                    ('student_id', '=', student.id)]
            year = year_obj.search(cond)
            if not year:
                vals = {'school_year_id': self.school_year_id.id,
                        'teacher_id': self.teacher_id.id,
                        'student_id': student.id}
                year_obj.create(vals)
        return {'type': 'ir.actions.act_window_close'}
