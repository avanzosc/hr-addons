# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Timesheet Schedule",
    "version": "14.0.1.0.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Services/Timesheets",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet",
        "event_track_analytic",
    ],
    "data": [
        "report/hr_timesheet_report.xml",
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
}
