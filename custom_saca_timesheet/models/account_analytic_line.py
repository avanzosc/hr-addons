# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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
        default = False)

    def write(self, values):
        result = super(AccountAnalyticLine, self).write(values)
        chofer = self.env["account.analytic.line"].search(
            [("saca_line_id", "=", self.saca_line_id.id),
             ("name", "ilike", "Chofer")], limit=1)
        matanza = self.env["account.analytic.line"].search(
            [("saca_line_id", "=", self.saca_line_id.id),
             ("name", "ilike", "Matanza")], limit=1)
        espera = self.env["account.analytic.line"].search(
            [("saca_line_id", "=", self.saca_line_id.id),
             ("name", "ilike", "Espera")], limit=1)
        if ("time_start" in values and self.id == matanza.id) or (
            "time_stop" in values and self.id == chofer.id) and (
                chofer.time_stop) and matanza.time_start and espera:
            espera.write({
                "time_start": chofer.time_stop,
                "time_stop": matanza.time_start,
                "unit_amount": matanza.time_start - chofer.time_stop})
        return result
