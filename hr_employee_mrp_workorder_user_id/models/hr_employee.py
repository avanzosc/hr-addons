from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    calendar_id = fields.Many2one('employee.work.schedule', string="Work Schedule")
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id and self.user_id.employee_id:
            self.calendar_id = self.user_id.employee_id.calendar_id
