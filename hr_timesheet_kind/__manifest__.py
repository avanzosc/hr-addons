# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Timesheets Classification",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "analytic_line_kind",
        "hr_timesheet",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Human Resources",
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
