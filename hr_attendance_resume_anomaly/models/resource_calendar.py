# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    percentage_excess_hours = fields.Float(
        string='Percentage excess hours')
    percentage_defect_hours = fields.Float(
        string='Percentage defect hours')
