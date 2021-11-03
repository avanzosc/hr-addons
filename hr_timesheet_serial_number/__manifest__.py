# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Hr Timesheet Serial Number",
    'version': '12.0.2.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Project",
    "depends": [
        "storable_product_generate_task",
        "sale_order_lot_selection"
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_task_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
