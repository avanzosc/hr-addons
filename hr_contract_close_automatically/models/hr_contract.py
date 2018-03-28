# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def automatic_close_expired_employee_contracts(self):
        expired_stage = self.env.ref(
            'hr_contract_stages.stage_contract3', False)
        date = fields.Date.to_string(fields.Date.from_string(
            fields.Date.today()) + relativedelta(days=-1))
        cond = [('date_end', '!=', False),
                ('date_end', '<=', date),
                ('contract_stage_id', '!=', expired_stage.id)]
        contracts = self.env['hr.contract'].search(cond)
        for contract in contracts:
            try:
                contract.contract_stage_id = expired_stage.id
            except Exception:
                pass
