# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Attendances Report",
    "version": "11.0.1.0.0",
    "category": "Human Resources",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "hr_attendance",
        "report_xlsx",
    ],
    "excludes": [],
    "data": [
        "reports/hr_attendance_report_xlsx.xml",
    ],
    "installable": True,
}
