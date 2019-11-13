# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizHrAttendanceResume(models.TransientModel):
    _name = "wiz.hr.attendance.resume"
    _description = "Wizard to impute assistances resume"

    @api.multi
    def button_impute(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        attendances = self.env['hr.attendance'].browse(active_ids)
        if attendances:
            attendances = attendances.filtered(lambda c: not c.treated)
            if attendances:
                attendances._impute_in_attendance_resume()
        return {'type': 'ir.actions.act_window_close'}
