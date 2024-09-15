# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class WizAttendanceResumePutResolved(models.TransientModel):
    _name = "wiz.attendance.resume.put.resolved"
    _description = "Wizard for put anomalies as resolved"

    @api.multi
    def button_resolved(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        resumes = self.env['hr.attendance.resume'].browse(active_ids)
        if resumes:
            resumes.write({'anomaly_resolved': True})
        return {'type': 'ir.actions.act_window_close'}
