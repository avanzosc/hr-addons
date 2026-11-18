# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_attendance_user_menu_status(self):
        """Return the attendance status of the employee of the current user
        in the current company, to be displayed in the user menu."""
        employee = self.env.user.employee_id.sudo()
        if not employee:
            return {}
        return {
            "employee_id": employee.id,
            "attendance_state": employee.attendance_state,
        }
