# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizHrAttendanceResumeAbsence(models.TransientModel):
    _name = "wiz.hr.attendance.resume.absence"
    _description = "Wizard to impute absences from attendance resume"

    @api.multi
    def button_generate(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        resumes = self.env['hr.attendance.resume'].browse(active_ids)
        if resumes:
            resumes._generate_allocations()
        return {'type': 'ir.actions.act_window_close'}
