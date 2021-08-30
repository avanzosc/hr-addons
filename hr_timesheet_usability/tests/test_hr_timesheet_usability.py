# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo import fields
from odoo.exceptions import UserError


@common.at_install(False)
@common.post_install(True)
class TestHrTimesheetUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHrTimesheetUsability, cls).setUpClass()
        cls.analytic_vals1 = {
            'date': '2021-07-12',
            'time_start': 6.00,
            'time_stop': 6.00,
            'unit_amount': 0.0,
            'name': 'aaaa',
            'project_id': cls.env['project.project'].search(
                [], limit=1).id}
        cls.analytic1 = cls.env['account.analytic.line'].create(
            cls.analytic_vals1)
        cls.task_vals1 = {
            'name': 'abcd',
            'user_id': 2,
            'project_id': cls.env['project.project'].search([], limit=1).id}
        cls.task1 = cls.env['project.task'].create(cls.task_vals1)
        cls.task_vals2 = {
            'name': 'ijkl',
            'user_id': 7,
            'project_id': cls.env['project.project'].search([], limit=1).id}
        cls.task2 = cls.env['project.task'].create(cls.task_vals2)

    def test_hr_timesheet_usability(self):
        self.date = fields.Datetime.now()
        hours = int(self.date.strftime("%H"))
        minutes = int(self.date.strftime("%M"))
        self.analytic1.action_button_end()
        self.analytic1.onchange_hours_start_stop()
        self.assertEqual(
            self.analytic1.time_stop, round(hours + minutes/60, 14))
        self.assertEqual(self.task1.show_init_task, True)
        self.task1.action_button_initiate_task()
        self.assertEqual(
            self.task1.user_id.id, self.task1.timesheet_ids[0].user_id.id)
        self.assertEqual(
            self.task1.employee_id.id,
            self.task1.timesheet_ids[0].employee_id.id)
        self.task1._compute_show_init_task()
        self.assertEqual(self.task1.show_init_task, False)
        self.task1.timesheet_ids[0].write({
            'time_start': 6.0,
            'time_stop': 6.0
            })
        self.task1.action_button_end_task()
        self.assertEqual(
            self.analytic1.time_stop, round(hours + minutes/60, 14))
        self.task1._compute_show_init_task()
        self.assertEqual(self.task1.show_init_task, True)
        with self.assertRaises(UserError):
            self.task2.action_button_initiate_task()
