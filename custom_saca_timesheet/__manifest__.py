# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Saca Timesheet",
    "summary": "Timesheet integration for saca lines",
    "version": "18.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        "custom_descarga",
        "hr_timesheet_begin_end_usability",
    ],
    "data": [
        "data/project.xml",
        "views/saca_line_view.xml",
        "views/account_analytic_line_view.xml",
        "views/project_task_view.xml",
    ],
    "installable": True,
}
