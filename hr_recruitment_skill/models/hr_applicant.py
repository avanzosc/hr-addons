# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class Employee(models.Model):
    _inherit = 'hr.applicant'

    applicant_skill_ids = fields.One2many(
        comodel_name='hr.applicant.skill', inverse_name='applicant_id',
        string="Applicant Skill")
    applicant_eskill_ids = fields.One2many(
        comodel_name='hr.employee.skill', inverse_name='applicant_id',
        string="Applicant Skill")
