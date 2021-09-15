# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    departure_reason_id = fields.Many2one(
        string='Employee Departure Reason',
        comodel_name='hr.employee.departure.reason')
    departure_observation = fields.Char(
        string='Departure Observation')

    def action_register_departure(self):
        result = super(HrDepartureWizard, self).action_register_departure()
        if not self.departure_reason_id:
            raise ValidationError(
                _("You must introduce the employee departure reason."))
        return result
