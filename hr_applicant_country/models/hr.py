# -*- coding: utf-8 -*-
# (Copyright) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class HrJob(models.Model):
    _inherit = 'hr.job'

    destination_country_id = fields.Many2one(
        comodel_name='res.country', string='Destination country',
        related='address_id.country_id', store=True)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    destination_country_id = fields.Many2one(
        comodel_name='res.country', string='Destination country',
        related='job_id.destination_country_id', store=True)
    contact_country_id = fields.Many2one(
        comodel_name='res.country', string='Contact country')

    @api.multi
    def onchange_partner_id(self, partner_id):
        res = super(HrApplicant, self).onchange_partner_id(partner_id)
        res['value']['contact_country_id'] = False
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner.country_id:
                res['value']['contact_country_id'] = partner.country_id.id
        return res
