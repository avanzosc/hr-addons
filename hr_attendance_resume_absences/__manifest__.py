# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Attendance Resume Absences",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_attendance_resume",
        "hr_holidays_public",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Human Resources",
    "data": [
        "data/hr_attendance_resume_absences_data.xml",
        "views/hr_attendance_resume_view.xml",
        "views/hr_leave_allocation_view.xml",
        "views/hr_leave_view.xml",
        "wizard/wiz_hr_attendance_resume_absence_view.xml",
    ],
    "installable": True,
}
