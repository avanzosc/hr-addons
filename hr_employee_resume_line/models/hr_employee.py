
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    last_resume_line_ids = fields.One2many(
        'hr.resume.line', 'employee_id', string="Last resumé lines",
        compute="_compute_last_resume_lines", store=True
    )

    @api.depends('resume_line_ids')
    def _compute_last_resume_lines(self):
        for record in self:
            line_channels = record.resume_line_ids.mapped('channel_id')
            unique_last_resume_line_ids = []
            for channel in line_channels:
                last_channel_record = record.resume_line_ids.filtered(
                    lambda r: r.channel_id == channel).sorted('date_end')
                unique_last_resume_line_ids.append(last_channel_record[0].id)

            record.last_resume_line_ids = record.resume_line_ids.filtered(
                lambda r: r.id in unique_last_resume_line_ids
            )
