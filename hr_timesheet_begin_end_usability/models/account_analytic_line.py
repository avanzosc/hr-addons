# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models
from datetime import timedelta
from odoo.tools.float_utils import float_compare


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    date_end = fields.Date(
        string="Date End",
        required=True,
        index=True,
        default=fields.Date.context_today)

    @api.constrains("time_start", "time_stop", "unit_amount")
    def _check_time_start_stop(self):
        for line in self:
            value_to_html = self.env["ir.qweb.field.float_time"].value_to_html
            start = timedelta(hours=line.time_start)
            stop = timedelta(hours=line.time_stop)
            hours = (stop - start).seconds / 3600
            if stop < start:
                line.date_end = line.date + timedelta(days=1)
                hours = (stop + timedelta(hours=24) - start).seconds / 3600
            rounding = self.env.ref("uom.product_uom_hour").rounding
            if hours and float_compare(
                hours, line.unit_amount, precision_rounding=rounding
            ):
                line.unit_amount = hours
                if hours and float_compare(
                    hours, line.unit_amount, precision_rounding=rounding
                ):
                    raise exceptions.ValidationError(
                        _(
                            "The duration (%s) must be equal to the difference "
                            "between the hours (%s)."
                            )
                        % (
                            value_to_html(line.unit_amount, None),
                            value_to_html(hours, None),
                            )
                        )
            # check if lines overlap
            if self.user_id:
                others = self.search(
                    [
                        ("id", "!=", line.id),
                        ("user_id", "=", line.user_id.id),
                        ("date", "=", line.date),
                        ("time_start", "<", line.time_stop),
                        ("time_stop", ">", line.time_start),
                    ]
                )
                if others:
                    message = _("Lines can't overlap:\n")
                    message += "\n".join(
                        [
                            "%s - %s"
                            % (
                                value_to_html(other.time_start, None),
                                value_to_html(other.time_stop, None),
                            )
                            for other in (line + others).sorted(lambda l: l.time_start)
                        ]
                    )
                    raise exceptions.ValidationError(message)

    @api.onchange("time_start", "time_stop")
    def onchange_hours_start_stop(self):
        result = super(AccountAnalyticLine, self).onchange_hours_start_stop()
        start = timedelta(hours=self.time_start)
        stop = timedelta(hours=self.time_stop)
        if stop < start:
            self.unit_amount = (
                stop + timedelta(hours=24) - start).seconds / 3600
        return result
