# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Personal Equipment Request Cancel",
    "summary": "Server action to cancel PPE Requests.",
    "version": "14.0.1.0.0",
    "category": "Hr",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        "hr_personal_equipment_request",
        "stock_picking_cancel",
    ],
    "data": ["data/hr_personal_equipment_request_actions.xml"],
    "installable": True,
}
