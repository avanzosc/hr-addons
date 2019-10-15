# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizHrAttendanceUncheckTreaties(models.TransientModel):
    _name = "wiz.hr.attendance.uncheck.treaties"
    _description = "Wizard for uncheck attendances treaties"

    @api.multi
    def button_uncheck(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        attendances = self.env['hr.attendance'].browse(active_ids)
        if attendances:
            attendances.write({'treated': False})
        return {'type': 'ir.actions.act_window_close'}
