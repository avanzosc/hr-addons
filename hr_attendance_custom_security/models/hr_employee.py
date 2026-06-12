from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    attendance_manager_id = fields.Many2one(
        "res.users",
        store=True,
        readonly=False,
        domain="[('share', '=', False), ('company_ids', 'in', company_id)]",
        groups="hr_attendance.group_hr_attendance_officer,hr_attendance.group_hr_attendance_own_reader",
    )
