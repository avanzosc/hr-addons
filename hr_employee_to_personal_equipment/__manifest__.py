# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HR Employee to Personal Equipment",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Employees",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        "hr",
        "hr_personal_equipment_request",
        "hr_employee_sees_himself",
    ],
    "data": [
        "views/hr_employee_view.xml",
    ],
    "installable": True,
}
