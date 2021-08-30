# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api
from datetime import datetime
import pytz
from datetime import timedelta


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.multi
    def action_button_end(self):
        self.ensure_one()
        for line in self:
            timezone = pytz.timezone(line._context.get('tz') or 'UTC')
            date_end = datetime.now()
            date_end = date_end.replace(tzinfo=pytz.timezone(
                'UTC')).astimezone(timezone)
            hours = int(date_end.strftime("%H"))
            minutes = int(date_end.strftime("%M"))
            start = line.time_start
            stop = hours + minutes/60
            start2 = timedelta(hours=start)
            stop2 = timedelta(hours=stop)
            if stop > start:
                unit_amount = (stop2 - start2).seconds / 3600
                vals = {'time_stop': round(stop, 14),
                        'unit_amount': unit_amount}
                line.write(vals)

    @api.onchange('time_start', 'time_stop')
    def onchange_hours_start_stop(self):
        self.time_stop = self.time_start if (
            self.time_start > 0 and self.time_stop == 0.0) else self.time_stop
        return super(AccountAnalyticLine, self).onchange_hours_start_stop()
