# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class Machine(models.Model):
    _inherit = "machine"

    employee_ids = fields.Many2many(
        string="Machine Users", comodel_name="hr.employee",
        relation="rel_machine_employee", column1="machine_id",
        column2="employee_id",
    )
