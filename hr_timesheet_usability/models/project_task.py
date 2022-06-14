# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta
import pytz


class ProjectTask(models.Model):
    _inherit = 'project.task'

    show_init_task = fields.Boolean(
        string='Show initiate task button', compute='_compute_show_init_task')
    employee_id = fields.Many2one(
        string='Employee', comodel_name='hr.employee')

    def _compute_show_init_task(self):
        for task in self:
            if not task.timesheet_ids:
                task.show_init_task = True
            else:
                found = task.timesheet_ids.filtered(
                    lambda x: x.employee_id == (
                        self.employee_id) and x.time_stop == x.time_start)
                if found:
                    task.show_init_task = False
                else:
                    task.show_init_task = True

    def action_button_initiate_task(self):
        self.ensure_one()
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        date_start = fields.Datetime.now()
        date_start = date_start.replace(tzinfo=pytz.timezone(
            'UTC')).astimezone(timezone)
        hours = int(date_start.strftime("%H"))
        minutes = int(date_start.strftime("%M"))
        initiate_timesheet_vals = {
            'name': self.name,
            'task_id': self.id,
            'project_id': self.project_id.id,
            'date': date_start.date(),
            'time_start': round(hours + minutes/60, 14),
            'time_stop': round(hours + minutes/60, 14)
            }
        if self.user_id:
            cond = [('user_id', '=', self.user_id.id)]
            self.employee_id = self.env['hr.employee'].search(cond, limit=1).id
            if not self.employee_id:
                raise UserError(_(
                    'Employee not found for user: {}').format(
                        self.user_id.name))
            initiate_timesheet_vals.update({
                'user_id': self.user_id.id,
                'employee_id': self.employee_id.id})
        return self.env['account.analytic.line'].create(
            initiate_timesheet_vals)

    def action_button_end_task(self):
        self.ensure_one()
        lines = self.timesheet_ids.filtered(
            lambda x: x.employee_id == self.employee_id and (
                x.time_stop == x.time_start))
        for line in lines:
            timezone = pytz.timezone(self._context.get('tz') or 'UTC')
            date_end = fields.Datetime.now()
            date_end = date_end.replace(tzinfo=pytz.timezone(
                'UTC')).astimezone(timezone)
            hours = int(date_end.strftime("%H"))
            minutes = int(date_end.strftime("%M"))
            stop = hours + minutes/60
            stop1 = timedelta(hours=stop)
            start = timedelta(hours=line.time_start)
            if stop1 > start:
                unit_amount = (stop1 - start).seconds / 3600
                vals = {'time_stop': round(stop, 14),
                        'unit_amount': unit_amount}
                line.write(vals)
