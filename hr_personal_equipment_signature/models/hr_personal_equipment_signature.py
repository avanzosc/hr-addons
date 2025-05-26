# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PersonalEquipmentRequest(models.Model):
    _inherit = "hr.personal.equipment.request"

    signature = fields.Binary(string="Firma del Solicitante")
