from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    @api.model
    def _domain_employee_id(self):
        employee = self.env.user.employee_id
        if not employee:
            return [("id", "=", False)]
        return ["|", ("id", "=", employee.id), ("leave_manager_id", "=", employee.id)]

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        domain=lambda self: self._domain_employee_id(),
        required=True,
    )
