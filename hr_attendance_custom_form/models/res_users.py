from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_punching_user = fields.Boolean(
        string="Is Punching User",
        default=False,
        help="Indicates if this user is enabled for time punching/attendance tracking."
    )