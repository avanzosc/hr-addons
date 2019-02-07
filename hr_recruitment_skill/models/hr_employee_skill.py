# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class EmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    applicant_id = fields.Many2one(
        comodel_name='hr.applicant', string="Employee")

    _sql_constraints = [
        ('hr_applicant_skill_uniq', 'unique(applicant_id, skill_id)',
         "This employee already has that skill!"),
    ]
