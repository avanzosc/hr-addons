# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestAnalyticHeadquarters(common.TransactionCase):

    def setUp(self):
        super(TestAnalyticHeadquarters, self).setUp()
        self.analytic_acc_model = self.env['account.analytic.account']
        self.analytic_line_model = self.env['account.analytic.line']
        self.invoice_model = self.env['account.invoice']
        self.partner = self.env.ref('base.res_partner_2')
        self.headquarters_id = self.env['res.headquarters'].create(
            {'name': 'Test Headquarters'})
        self.partner.headquarters_id = self.headquarters_id
        pricelist = self.env.ref('product.list0')
        invoice_factor = self.env.ref(
            'hr_timesheet_invoice.timesheet_invoice_factor1')
        analytic_vals = {
            'name': 'Test Account #1',
            'partner_id': self.partner.id,
            'pricelist_id': pricelist.id,
            'to_invoice': invoice_factor.id,
            'state': 'open',
            }
        self.analytic_acc_1 = self.analytic_acc_model.create(analytic_vals)
        product = self.env.ref('product.product_product_2')
        line_vals = {
            'name': 'Analytic Invoicing Line #1',
            'account_id': self.analytic_acc_1.id,
            'general_account_id': self.ref('account.cash'),
            'to_invoice': invoice_factor.id,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'journal_id': self.ref('hr_timesheet.analytic_journal'),
            'user_id': self.ref('base.user_demo'),
            'amount': 100,
            'unit_amount': 20,
            }
        self.analytic_line_1 = self.analytic_line_model.create(line_vals)
        self.invoice_create_wiz = self.env['hr.timesheet.invoice.create'
                                           ].with_context(
            active_id=self.analytic_line_1.id,
            active_ids=[self.analytic_line_1.id],
            active_model='account.analytic.line'
            )

    def test_invoice_headquarters(self):
        wiz = self.invoice_create_wiz.create({})
        res = wiz.do_create()
        for rec in res['domain']:
            if rec[0] == 'id':
                for invoice_id in rec[2]:
                    invoice = self.invoice_model.browse(invoice_id)
                    self.assertEqual(invoice.headquarters_id,
                                     self.headquarters_id)
                    invoice.signal_workflow('invoice_open')
                    for line in invoice.move_id.line_id:
                        self.assertEqual(line.headquarters_id,
                                         self.headquarters_id)
                    for analytic_line in invoice.mapped(
                            'move_id.line_id.analytic_lines'):
                        self.assertEqual(analytic_line.headquarters_id,
                                         self.headquarters_id)

    def test_invoice_change_partner(self):
        partner2 = self.partner.copy()
        partner2.headquarters_id = False
        invoice_vals = {'partner_id': partner2.id,
                        'type': 'out_invoice',
                        'account_id': self.ref('account.cash'),
                        'journal_id': self.ref('account.expenses_journal')
                        }
        invoice = self.invoice_model.create(invoice_vals)
        self.assertNotEqual(invoice.headquarters_id, self.headquarters_id)
        invoice.partner_id = self.partner
        res = invoice.onchange_partner_id('out_invoice', self.partner.id)
        self.assertEqual(res['value'].get('headquarters_id'),
                         self.headquarters_id.id)
