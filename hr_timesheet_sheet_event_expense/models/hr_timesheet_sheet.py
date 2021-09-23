# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet.sheet'

    def _get_timesheet_sheet_lines_domain(self):
        self.ensure_one()
        cond = super(
            HrTimesheetSheet, self)._get_timesheet_sheet_lines_domain()
        cond.append('|')
        cond.append(('product_id', '=', False))
        cond.append(('product_id.can_be_expensed', '=', False))
        return cond
