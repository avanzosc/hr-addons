# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Personal Equipment Report Email",
    "summary": "New report and mail template for personal equipment requests.",
    "version": "14.0.1.0.0",
    "category": "",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": ["stock_picking_date_done", "hr_personal_equipment_signature"],
    "data": [
        "report/personal_equipment_report.xml",
        "data/email_template.xml",
    ],
    "installable": True,
}
