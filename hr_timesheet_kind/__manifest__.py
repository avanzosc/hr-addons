# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Task Logs Classification",
    "version": "13.0.1.0.0",
    "category": "Operations/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "analytic_line_kind",
        "hr_timesheet",
    ],
    "excludes": [],
    "data": [
        "views/hr_timesheet_views.xml",
        "views/project_task_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
