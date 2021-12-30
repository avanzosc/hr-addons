# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import pytz


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    session_schedule = fields.Char(
        string='Schedule', compute='_compute_session_schedule', store=True)

    @api.depends("unit_amount", "event_track_id", "event_track_id.date")
    def _compute_session_schedule(self):
        for line in self:
            schedule = ""
            if (line.event_track_id and line.event_track_id.date and
                    line.unit_amount):
                timezone = pytz.timezone(
                    line.event_track_id.event_id.date_tz or 'UTC')
                track_date =  line.event_track_id.date.replace(
                    tzinfo=pytz.timezone('UTC')).astimezone(timezone)
                schedule = "{}:{}:{}".format(
                    str(track_date.hour).zfill(2),
                    str(track_date.minute).zfill(2),
                    str(track_date.second).zfill(2))
                new_date = track_date + relativedelta(
                    hours=+line.unit_amount)
                schedule = "{} - {}:{}:{}".format(
                    schedule,
                    str(new_date.hour).zfill(2),
                    str(new_date.minute).zfill(2),
                    str(new_date.second).zfill(2))
            line.session_schedule = schedule
