# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class PersonalEquipmentRequest(models.Model):
    _inherit = "hr.personal.equipment.request"

    signature = fields.Binary(string="Firma del Solicitante")

    def accept_request(self):
        for request in self:
            if not request.signature:
                raise UserError(
                    _("It is not possible to validate a request without a signature.")
                )
        return super().accept_request()
