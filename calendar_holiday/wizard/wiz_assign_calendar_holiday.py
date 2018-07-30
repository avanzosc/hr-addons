# -*- coding: utf-8 -*-
# (c) 2018 Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class WizAssignCalendarHoliday(models.TransientModel):
    _name = 'wiz.assign.calendar.holiday'

    calendar_holidays_ids = fields.Many2many(comodel_name="calendar.holiday",
                                             string="Assign holidays")
    calendar_year = fields.Integer(string="Generate calendar for year",
                                   required="true")

    @api.multi
    def button_assign_calendar_holiday_in_contracts(self):
        for contract in self.env['hr.contract'].browse(
                self.env.context.get('active_ids')):
            contract.holiday_calendars = [
                (6, 0, self.calendar_holidays_ids.ids)]
            contract._generate_calendar_from_wizard(self.calendar_year)
