from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_dates_without_hour(cr, registry):
    """
    This method will set the production cost on already done manufacturing orders.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    admin_user = env.ref("base.user_admin")
    env["hr.attendance"].with_user(admin_user)._put_dates_without_hour()
    env["resource.calendar.leaves"].with_user(admin_user)._put_dates_without_hour()
    env["hr.leave"].with_user(admin_user)._put_dates_without_hour()
    env["hr.contract"].with_user(admin_user)._post_install_hr_leave_attendance()
