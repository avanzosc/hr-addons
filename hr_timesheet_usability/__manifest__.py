# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Timesheet Usability",
    'version': '12.0.1.1.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "depends": [
        "project",
        "hr_timesheet",
        "hr_timesheet_activity_begin_end",
        "account"
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_task_views.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
