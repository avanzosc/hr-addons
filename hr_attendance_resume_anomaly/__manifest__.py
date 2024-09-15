# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Attendance Resume Anomaly",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "hr_attendance_control",
        "hr_attendance_resume_holidays",
        "hr_attendance_resume_absences"
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Human Resources",
    "data": [
        "security/ir.model.access.csv",
        "data/hr_attendance_resume_anomaly_data.xml",
        "wizard/wiz_attendance_resume_put_resolved_view.xml",
        "views/hr_attendance_resume_view.xml",
        "views/resource_calendar_view.xml",
    ],
    "installable": True,
}
