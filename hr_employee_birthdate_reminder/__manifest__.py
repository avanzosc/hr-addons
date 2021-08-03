# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Employee's birthdate reminder",
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/hr_employee_birthdate_report_view.xml",
        "reports/hr_employee_birthday_report_view.xml",
        "views/hr_employee_view.xml",
    ],
    "installable": True,
}
