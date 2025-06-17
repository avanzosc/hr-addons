# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Personal Equipment Signature",
    "version": "14.0.2.0.0",
    "category": "Human Resources",
    "summary": "Adds a signature field to personal equipment request",
    "author": "AvanzOSC",
    "depends": [
        "hr_personal_equipment_request",
        "web_digital_sign",
        "website",
    ],
    "data": [
        "views/hr_personal_equipment_signature_view.xml",
    ],
    "website": "https://github.com/avanzosc/hr-addons",
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "AGPL-3",
}
