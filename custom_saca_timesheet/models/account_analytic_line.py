# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import timedelta


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    order = "sequence"

    sequence = fields.Integer(string="Sequence")
    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line")
    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="saca_line_id.saca_id",
        store=True)
    classified = fields.Boolean(
        string="Classified",
        default=False)
    speed = fields.Float(
        string="Speed",
        compute="_compute_speed",
        store=True)

    @api.depends("saca_line_id", "saca_line_id.download_unit", "unit_amount")
    def _compute_speed(self):
        for line in self:
            speed = 0
            if line.saca_line_id and line.unit_amount != 0:
                speed = line.saca_line_id.download_unit / line.unit_amount
            line.speed = speed

    @api.onchange("time_start", "time_stop")
    def onchange_time_start(self):
        chofer = self.saca_line_id.timesheet_ids.filtered(
            lambda c: c.task_id.name == "Chofer")
        if self.time_stop > self.time_start:
            self.date_end = self.date
        if chofer and self.time_start < chofer.time_start:
            self.date = chofer.date + timedelta(days=1)
        if chofer and self.time_stop < chofer.time_start:
            self.date_end = chofer.date + timedelta(days=1)

    def write(self, values):
        result = super(AccountAnalyticLine, self).write(values)
        for line in self:
            chofer = self.env["account.analytic.line"].search(
                [("saca_line_id", "=", line.saca_line_id.id),
                 ("name", "=", u'{} {}'.format(
                     line.project_id.name, "Chofer"))], limit=1)
            matanza = line.env["account.analytic.line"].search(
                [("saca_line_id", "=", line.saca_line_id.id),
                 ("name", "=", u'{} {}'.format(
                     line.project_id.name, "Matanza"))], limit=1)
            espera = line.env["account.analytic.line"].search(
                [("saca_line_id", "=", line.saca_line_id.id),
                 ("name", "=", u'{} {}'.format(
                     line.project_id.name, "Espera"))], limit=1)
            if ("time_start" in values and line.id == matanza.id) or (
                "time_stop" in values and line.id == chofer.id) and (
                    chofer.time_stop) and matanza.time_start and espera:
                date_end = matanza.date
                amount = matanza.time_start - chofer.time_stop
                if matanza.time_start < chofer.time_stop:
                    amount = (timedelta(hours=matanza.time_start) + timedelta(
                        hours=24) - timedelta(hours=chofer.time_stop)
                    ).seconds / 3600
                espera.write({
                    "date": chofer.date_end,
                    "date_end": date_end,
                    "time_start": chofer.time_stop,
                    "time_stop": matanza.time_start,
                    "unit_amount": amount})
        return result
