# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, exceptions, _


class WizHrAttendanceResumeAbsence(models.TransientModel):
    _inherit = "wiz.hr.attendance.resume.absence"

    @api.multi
    def button_generate(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        resumes = self.env['hr.attendance.resume'].browse(active_ids)
        if resumes:
            resumes = resumes.filtered(
                lambda c: not c.anomaly_resolved and c.attendance_anomaly_ids)
            if resumes:
                error = _(u"To close the absences, all anomalies must be in "
                          "a 'resolved' state.")
                raise exceptions.Warning(error)
        return super(WizHrAttendanceResumeAbsence, self).button_generate()
