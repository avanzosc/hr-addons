# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class HrEmployeeDepartureReason(models.Model):
    _name = 'hr.employee.departure.reason'
    _description = 'Employee Departure Reason'

    name = fields.Char(string='Employee Departure Reason')
