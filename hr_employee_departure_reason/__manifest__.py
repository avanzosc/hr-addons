# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Employee Departure Reason",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "https://www.avanzosc.es",
    "category": "Human Resources/Employees",
    "depends": [
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/hr_employee_departure_reason.xml",
        "views/hr_employee_departure_reason.xml",
        "wizard/hr_departure_wizard_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
