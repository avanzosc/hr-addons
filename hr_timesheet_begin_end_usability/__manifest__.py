# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Hr Timesheet Begin End Usability",
    "version": "14.0.1.0.0",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        "analytic",
        "hr_timesheet",
        "hr_timesheet_activity_begin_end",
    ],
    "data": [
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
}
