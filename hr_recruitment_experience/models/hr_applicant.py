# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    academic_ids = fields.One2many(
        comodel_name='hr.academic', inverse_name='employee_id',
        string='Academic experiences', help="Academic experiences")
    certification_ids = fields.One2many('hr.certification',
                                        'employee_id',
                                        'Certifications',
                                        help="Certifications")
    experience_ids = fields.One2many('hr.experience',
                                     'employee_id',
                                     ' Professional Experiences',
                                     help='Professional Experiences')
