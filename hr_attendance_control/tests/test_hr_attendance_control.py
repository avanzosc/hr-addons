# -*- coding: utf-8 -*-
# Copyright (c) 2017  Daniel Campos - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp.tests.common import TransactionCase
from openerp import fields, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime


class TestHrAttendanceControl(TransactionCase):

    def setUp(self):
        super(TestHrAttendanceControl, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        self.attendance = self.env['hr.attendance']
        self.attendance_control_group = self.env.ref(
            'hr_attendance_control.group_attendance_control')
        self.today = fields.Date.from_string(fields.Date.today())
        self.today2 = datetime.now() + relativedelta(hours=2)
        self.employee_model = self.env['hr.employee']
        self.partner = self.env['res.partner'].create({
            'name': 'Partner',
        })
        self.user = self.env['res.users'].create({
            'partner_id': self.partner.id,
            'login': 'user',
            'password': 'pass',
        })
        employee_vals = {
            'name': 'Test Employee',
            'user_id': self.user.id,
        }
        employee_vals.update(
            self.employee_model.onchange_user(
                user_id=employee_vals['user_id'])['value'])
        self.employee = self.employee_model.create(employee_vals)

    def test_constraint(self):
        is_in_group = self.user.has_group(
            'hr_attendance_control.group_attendance_control')
        if is_in_group:
            self.user.groups_id -= self.env.ref(
                'hr_attendance_control.group_attendance_control')
        self.attendance_in = self.attendance.sudo(self.user).create({
            'employee_id': self.employee.id,
            'name': self.today.strftime("%Y-%m-%d 00:00:00"),
            'action': 'sign_in'
        })
        with self.assertRaises(exceptions.ValidationError):
            self.attendance.sudo(self.user).create({
                'employee_id': self.employee.id,
                'name': self.today2.strftime("%Y-%m-%d %H:%M:%S"),
                'action': 'sign_in'
            })
        self.user.groups_id |= self.env.ref(
            'hr_attendance_control.group_attendance_control')
        self.attendance.sudo(self.user).create(
            {'employee_id': self.employee.id,
             'name': self.today2.strftime("%Y-%m-%d %H:%M:%S"),
             'action': 'sign_in'
             })
        prev_att_ids = self.attendance.search(
            [('employee_id', '=', self.employee.id),
             ('name', '<', self.today2.strftime("%Y-%m-%d %H:%M:%S")),
             ('action', '=', 'sign_in')], limit=1,
            order='name DESC')
        self.assertEquals(len(prev_att_ids), 1,
                          "Previous Attendances need to be in sign_in.")
