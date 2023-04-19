# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    timesheet_ids = fields.One2many(
        string="Timesheet",
        comodel_name="account.analytic.line",
        inverse_name="saca_line_id")

    def action_next_stage(self):
        super(SacaLine, self).action_next_stage()
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        project = self.env.ref("custom_saca_timesheet.project_saca")
        if self.stage_id == stage_descarga:
            if not self.purchase_order_line_ids:
                raise ValidationError(
                    _("There is no any purchase order line.")
                )
            if not self.timesheet_ids:
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Carga",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 2,
                        "saca_line_id": self.id,
                        "date": self.saca_id.date,
                        "date_end": self.saca_id.date,
                        "name": u'{} {}'.format(project.name, "Carga"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Espera",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 3,
                        "saca_line_id": self.id,
                        "date": self.saca_id.date,
                        "date_end": self.saca_id.date,
                        "name": u'{} {}'.format(project.name, "Espera"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Chofer",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 1,
                        "saca_line_id": self.id,
                        "date": self.saca_id.date,
                        "date_end": self.saca_id.date,
                        "name": u'{} {}'.format(project.name, "Chofer"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Matanza",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 4,
                        "saca_line_id": self.id,
                        "date": self.saca_id.date,
                        "date_end": self.saca_id.date,
                        "name": u'{} {}'.format(project.name, "Matanza"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Matanza(Parte II)",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 5,
                        "saca_line_id": self.id,
                        "date": self.saca_id.date,
                        "date_end": self.saca_id.date,
                        "name": u'{} {}'.format(project.name, "Matanza(Parte II)"),
                        "project_id": project.id})]})
            for line in self.timesheet_ids:
                line.employee_id = False
                line.user_id = False
