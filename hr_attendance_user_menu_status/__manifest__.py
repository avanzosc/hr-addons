# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "HR Attendance User Menu Status",
    "summary": "Show the attendance status of the logged user in the systray and "
    "check in or out from it",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["hr_attendance"],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "category": "Human Resources",
    "assets": {
        "web.assets_backend": [
            "hr_attendance_user_menu_status/static/src/components/**/*",
        ],
    },
    "installable": True,
    "application": False,
}
