# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    birthdate_day = fields.Integer(
        string="Birthdate Day", compute="_compute_birthdate", store=True,
        index=True)
    birthdate_month = fields.Integer(
        string="Birthdate Month", compute="_compute_birthdate", store=True,
        index=True)
    birthday_today = fields.Boolean(
        string="Birthday's Today", compute="_compute_birthday",
        search="_search_birthday")

    @api.depends("birthday")
    def _compute_birthdate(self):
        for record in self.filtered("birthday"):
            record.birthdate_day = record.birthday.day
            record.birthdate_month = record.birthday.month

    @api.multi
    def _compute_birthday(self):
        today = fields.Date.context_today(self)
        for employee in self.filtered("birthday"):
            employee.birthday_today = (
                employee.birthdate_day == today.day and
                employee.birthdate_month == today.month)

    @api.multi
    def _search_birthday(self, operator, value):
        today = fields.Date.context_today(self)
        if operator != '=':
            if operator == '!=' and isinstance(value, bool):
                value = not value
            else:
                raise NotImplementedError()
        employees = self.search_birthdate(today)
        if value:
            search_operator = "in"
        else:
            search_operator = "not in"
        return [('id', search_operator, employees.ids)]

    def next_week_birthday(self):
        today = fields.Date.context_today(self)
        employees = self.env["hr.employee"]
        for days in range(1, 8):
            new_date = today + relativedelta(days=days)
            employees |= self.search_birthdate(new_date)
        return employees

    def search_birthdate(self, birthdate):
        return self.search([
            ("birthdate_day", "=", birthdate.day),
            ("birthdate_month", "=", birthdate.month),
        ])
