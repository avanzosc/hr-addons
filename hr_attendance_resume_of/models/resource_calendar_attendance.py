# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    work_time_of = fields.Float(
        string='Work time of', compute='_compute_work_time_of', store=True)

    @api.depends('real_hour_from', 'real_hour_to')
    def _compute_work_time_of(self):
        for record in self:
            hours = record.real_hour_to - record.real_hour_from
            if record.real_hour_to == 23.9833333333333:
                hours += 0.0166666666666667
            record.work_time_of = hours
