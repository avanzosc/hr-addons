# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    @api.depends('hour_from', 'hour_to')
    def _compute_work_time(self):
        for record in self:
            hours = record.hour_to - record.hour_from
            if record.hour_to == 23.9833333333333:
                hours += 0.0166666666666667
            record.work_time = hours

    work_time = fields.Float(
        string='Work time', compute='_compute_work_time', store=True)
