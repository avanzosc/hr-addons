# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HR Employee To Account Move Line",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Employees",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        "hr",
        "account",
        "hr_employee_sees_himself",
    ],
    "data": [
        "views/account_account_view.xml",
        "views/hr_employee_view.xml",
    ],
    "installable": True,
}
