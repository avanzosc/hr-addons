# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    year_tutor_ids = fields.One2many(
        comodel_name='hr.employee.supervised.year',
        inverse_name='student_id', string='Tutors per year')
    current_year_tutor_ids = fields.Many2many(
        comodel_name="hr.employee",
        compute="_compute_current_year_tutor_ids",
        string="Current Tutors",
        compute_sudo=True)
    allowed_user_ids = fields.Many2many(
        comodel_name='res.users', relation='rel_res_partner_users',
        column1='partner_id', column2='user_id', string='Allowed users',
        copy=False, compute='_compute_allowed_user_ids', store=True,
        compute_sudo=True)

    @api.depends("year_tutor_ids")
    def _compute_current_year_tutor_ids(self):
        for partner in self:
            tutors = partner.sudo().year_tutor_ids.filtered(
                lambda t: t.school_year_id.current)
            partner.current_year_tutor_ids = tutors.mapped("teacher_id")

    @api.depends('year_tutor_ids', 'year_tutor_ids.user_id')
    def _compute_allowed_user_ids(self):
        for partner in self:
            partner.allowed_user_ids = [(6, 0, [])]
            users = partner.mapped('year_tutor_ids.user_id')
            if users:
                partner.allowed_user_ids = [(6, 0, users.ids)]
