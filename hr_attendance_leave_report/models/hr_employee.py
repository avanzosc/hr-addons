# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrEmpployee(models.Model):
    _inherit = "hr.employee"

    attendance_leave_ids = fields.One2many(
        string="Attendances And Absences",
        comodel_name="hr.attendance.leave",
        inverse_name="employee_id",
        copy=False,
    )
