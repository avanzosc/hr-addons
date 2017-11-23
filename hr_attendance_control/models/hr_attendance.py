# -*- coding: utf-8 -*-
# Copyright (c) 2017  Daniel Campos - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    def _altern_si_so(self, cr, uid, ids, context=None):
        result = super(HrAttendance, self)._altern_si_so(cr, uid, ids,
                                                         context=context)
        user_obj = self.pool['res.users']
        return user_obj.has_group(
            cr, uid, 'hr_attendance_control.group_attendance_control') \
            or result

    _constraints = [
        (_altern_si_so, 'Error ! Sign in (resp. Sign out) must follow Sign out'
         ' (resp. Sign in)', ['action'])]
