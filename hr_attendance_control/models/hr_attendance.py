# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    entry_without_exit = fields.Boolean(
        string='Entry without exit', compute='_compute_entry_without_exit',
        store=True)

    @api.depends('check_in', 'check_out')
    def _compute_entry_without_exit(self):
        for record in self:
            entry = False
            if record.check_out:
                worked_hours = record._catch_worked_hours()
                if worked_hours >= 20.0:
                    entry = True
            record.entry_without_exit = entry

    @api.multi
    def write(self, vals):
        result = super(HrAttendance, self).write(vals)
        if 'check_out' in vals and vals.get('check_out', False):
            for attendance in self:
                if attendance.check_out:
                    worked_hours = attendance._catch_worked_hours()
                    if worked_hours >= 20.0:
                        vals = {'employee_id': attendance.employee_id.id,
                                'check_in': attendance.check_out,
                                'checkt_out': False}
                        self.create(vals)
        return result

    @api.multi
    def _catch_worked_hours(self):
        delta = self.check_out - self.check_in
        worked_hours = delta.total_seconds() / 3600.0
        return worked_hours
