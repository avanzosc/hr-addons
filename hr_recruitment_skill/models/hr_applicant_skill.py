# Copyright 2013 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EmployeeSkill(models.Model):
    _name = 'hr.applicant.skill'

    @api.model
    def _get_selection_picking_policy(self):
        return self.env['hr.employee.skill'].fields_get(
            allfields=['level'])['level']['selection']

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', string="Applicant")
    skill_id = fields.Many2one(comodel_name='hr.skill', string="Skill")
    level = fields.Selection(
        selection=_get_selection_picking_policy, string='Level')

    _sql_constraints = [
        ('hr_applicant_skill_uniq', 'unique(applicant_id, skill_id)',
         "This applicant already has that skill!"),
    ]

