# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Attendance Leave Report",
    "version": "16.0.1.0.0",
    "category": "Human Resources/Attendances",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": ["resource", "hr_attendance", "hr_contract", "hr_holidays"],
    "data": [
        "security/ir.model.access.csv",
        "security/hr_attendance_leave_report_security.xml",
        "data/scheduled_action.xml",
        "views/hr_attendance_views.xml",
        "views/hr_attendance_leave_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_dates_without_hour",
}
