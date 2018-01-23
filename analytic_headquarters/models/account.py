# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    headquarters_id = fields.Many2one(comodel_name='res.headquarters',
                                      string='Headquarters')

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        res = super(AccountInvoice,
                    self).finalize_invoice_move_lines(move_lines)
        for move in res:
            move[2].update(
                {'headquarters_id': (self.headquarters_id and
                                     self.headquarters_id.id or False)})
        return res

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        partner = self.env['res.partner'].browse(partner_id)
        res['value'].update(
            {'headquarters_id': (partner.headquarters_id and
                                 partner.headquarters_id.id or False)})
        return res


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    headquarters_id = fields.Many2one(comodel_name='res.headquarters',
                                      string='Headquarters')

    @api.model
    def _prepare_analytic_line(self, obj_line):
        res = super(AccountMoveLine, self)._prepare_analytic_line(obj_line)
        res['headquarters_id'] = (obj_line.headquarters_id and
                                  obj_line.headquarters_id.id or False)
        return res


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    headquarters_id = fields.Many2one(comodel_name='res.headquarters',
                                      string='Headquarters')

    @api.model
    def _prepare_cost_invoice(self, partner, company_id, currency_id,
                              analytic_lines):
        res = super(AccountAnalyticLine, self)._prepare_cost_invoice(
            partner, company_id, currency_id, analytic_lines)
        res['headquarters_id'] = (partner.headquarters_id and
                                  partner.headquarters_id.id or False)
        return res
