# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    timesheet_ids = fields.One2many(
        string="Timesheet",
        comodel_name="account.analytic.line",
        inverse_name="saca_line_id",
        compute="_compute_timesheet_ids")
    clasified_ids = fields.One2many(
        string="Classified",
        comodel_name="account.analytic.line",
        inverse_name="saca_line_id",
        compute="_compute_classified_ids")

    def _compute_timesheet_ids(self):
        for line in self:
            cond = [("saca_line_id", "=", line.id), (
                "classified", "=", False)]
            timesheet = self.env["account.analytic.line"].search(cond)
            line.timesheet_ids = [(6, 0, timesheet.ids)]

    def _compute_classified_ids(self):
        for line in self:
            cond = [("saca_line_id", "=", line.id), (
                "classified", "=", True)]
            classified = self.env["account.analytic.line"].search(cond)
            line.clasified_ids = [(6, 0, classified.ids)]

    def action_next_stage(self):
        super(SacaLine, self).action_next_stage()
        stage_descarga = self.env.ref("custom_descarga.stage_descarga")
        stage_clasificado = self.env.ref("custom_descarga.stage_clasificado")
        if self.stage_id == stage_clasificado:
            project = self.env.ref("custom_descarga.project_saca")
            today = fields.Date.today()
            cond = [('user_id', '=', self.env.user.id)]
            employee = self.env['hr.employee'].search(cond, limit=1)
            self.env["project.task"].create({
                "project_id": project.id,
                "name": "Clasificado",
                "saca_line_id": self.id,
                "timesheet_ids": [(0, 0, {
                    "saca_line_id": self.id,
                    "date": today,
                    "employee_id": employee.id,
                    "name": u'{} {}'.format(project.name,"Clasificado"),
                    "project_id": project.id,
                    "classified":True})]})
        if self.stage_id == stage_descarga:
            if not self.purchase_order_line_ids:
                raise ValidationError(
                    _("There is no any purchase order line.")
                )
            if not self.timesheet_ids:
                project = self.env.ref("custom_descarga.project_saca")
                today = fields.Date.today()
                cond = [('user_id', '=', self.env.user.id)]
                employee = self.env['hr.employee'].search(cond, limit=1)
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Carga",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 2,
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Carga"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Espera",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 3,
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Espera"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Chofer",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 1,
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Chofer"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Matanza",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 4,
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Matanza"),
                        "project_id": project.id})]})
                self.env["project.task"].create({
                    "project_id": project.id,
                    "name": "Corte",
                    "saca_line_id": self.id,
                    "timesheet_ids": [(0, 0, {
                        "sequence": 5,
                        "saca_line_id": self.id,
                        "date": today,
                        "employee_id": employee.id,
                        "name": u'{} {}'.format(project.name,"Corte"),
                        "project_id": project.id})]})
