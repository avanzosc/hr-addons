# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Custom Saca Timesheet",
    "version": "14.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "hr_timesheet_activity_begin_end",
        "custom_descarga"
    ],
    "data": [
        "data/project.xml",
        "views/saca_line_view.xml",
        "views/account_analytic_line_view.xml",
        "views/project_task_view.xml",
    ],
    "installable": True,
}
