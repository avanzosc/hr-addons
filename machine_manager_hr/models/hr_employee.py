# -*- coding: utf-8 -*-
# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    machine_ids = fields.Many2many(
        string="Machines", comodel_name="machine",
        relation="rel_machine_employee", column1="employee_id",
        column2="machine_id",
    )
