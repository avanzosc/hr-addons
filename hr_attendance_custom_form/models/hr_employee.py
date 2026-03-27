from odoo import fields, models, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def attendance_manual_custom_form(self, next_action, entered_pin=None):
        self.ensure_one()
        attendance_user_and_no_pin = self.user_has_groups(
            'hr_attendance.group_hr_attendance_user,'
            '!hr_attendance.group_hr_attendance_use_pin')
        
        can_check_without_pin = attendance_user_and_no_pin or \
                               (self.user_id == self.env.user and entered_pin is None)

        if can_check_without_pin:
            return {'action': 'valid', 'employee_id': self.id}
        elif entered_pin is not None and entered_pin == self.sudo().pin:
            return {'action': 'valid', 'employee_id': self.id}
        
        if not self.user_has_groups('hr_attendance.group_hr_attendance_user'):
            warning_message = _('To activate Kiosk mode without pin code, you must have access right as an Officer or above in the Attendance app. Please contact your administrator.')
            return {'warning': warning_message}
        
        warning_message = _('Wrong PIN')
        return {'warning': warning_message}