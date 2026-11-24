# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Copy the email of the private address to the private email."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    employees = (
        env["hr.employee"]
        .with_context(active_test=False)
        .search([("address_home_id.email", "!=", False)])
    )
    for employee in employees:
        employee.private_email = employee.address_home_id.email
