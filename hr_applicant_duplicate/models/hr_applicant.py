# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, _
from odoo.exceptions import ValidationError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.constrains('partner_mobile', 'partner_phone', 'email_from')
    def _check_applicant_duplicate(self):
        for applicant in self:
            if applicant.partner_mobile:
                cond = [('id', '!=', applicant.id), '|',
                        ('partner_mobile', 'ilike', applicant.partner_mobile),
                        ('partner_phone', 'ilike', applicant.partner_mobile),
                        '|', ('active', '=', True), ('active', '=', False)]
                employee = applicant.env['hr.applicant'].search(cond, limit=1)
                if employee and employee != applicant.id:
                    raise ValidationError(
                        _("Applicant mobile is duplicated."))
            if applicant.partner_phone:
                cond = [('id', '!=', applicant.id), '|',
                        ('partner_phone', 'ilike', applicant.partner_phone),
                        ('partner_mobile', 'ilike', applicant.partner_phone),
                        '|', ('active', '=', True), ('active', '=', False)]
                employee = applicant.env['hr.applicant'].search(cond, limit=1)
                if employee:
                    raise ValidationError(
                        _("Applicant phone is duplicated."))
            if applicant.email_from:
                cond = [('id', '!=', applicant.id),
                        ('email_from', '=ilike', applicant.email_from), '|',
                        ('active', '=', True), ('active', '=', False)]
                employee = applicant.env['hr.applicant'].search(cond, limit=1)
                if employee:
                    raise ValidationError(
                        _("Applicant email is duplicated."))
