# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "HR Employee Private Email",
    "summary": "Keep the private email on the employee",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["hr"],
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "category": "Human Resources",
    "data": [
        "views/res_users_view.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
