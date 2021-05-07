# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet.sheet'

    @api.multi
    def _get_timesheet_sheet_lines_domain(self):
        self.ensure_one()
        domain = super(
            HrTimesheetSheet, self)._get_timesheet_sheet_lines_domain()
        domain.append(('move_id', '=', False))
        return domain
