from odoo import models, fields, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    work_schedule_id = fields.Many2one('employee.work.schedule', string="Work Schedule")

    @api.onchange('user_id')
    def _onchange_user_id_workorder(self):
        if self.user_id and self.user_id.employee_id:
            self.work_schedule_id = self.user_id.employee_id.calendar_id
