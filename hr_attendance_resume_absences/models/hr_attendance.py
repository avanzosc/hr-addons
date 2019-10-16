# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, exceptions, _


class HrAttendanceResume(models.Model):
    _inherit = 'hr.attendance.resume'

    treated = fields.Boolean(string='Treated', default=False)
    hr_leave_allocation_id = fields.Many2one(
        string='Allocation', comodel_name='hr.leave.allocation')

    @api.multi
    def unlink(self):
        for resume in self:
            if resume and resume.hr_leave_allocation_id:
                error = _(u'You cannot delete the hours imputations resume '
                          'with date {},  of the employee {}, because he has '
                          'assigned an allocation').format(
                              resume.date, resume.employee_id.name)
                raise exceptions.Warning(error)
        return super(HrAttendanceResume, self).unlink()

    @api.multi
    def write(self, vals):
        if 'treated' in vals and not vals.get('treated', False):
            for resume in self:
                if resume and resume.hr_leave_allocation_id:
                    error = _(u'You cannot delete the hours imputations resume'
                              ' with date {},  of the employee {}, because he'
                              ' has assigned an allocation').format(
                                  resume.date, resume.employee_id.name)
                    raise exceptions.Warning(error)
        return super(HrAttendanceResume, self).write(vals)

    def _generate_allocations(self):
        resumes = self.filtered(
            lambda c: not c.treated and c.difference_hours != 0 and
            c.employee_id.resource_calendar_id)
        max_fec = max(resumes, key=lambda x: x.date)
        cond = [('id', 'in', self.mapped('employee_id').ids),
                ('resource_calendar_id', '!=', False)]
        employees = self.env['hr.employee'].search(cond)
        for employee in employees:
            resumes = self.filtered(
                lambda c: c.employee_id.id == employee.id and not
                c.treated and c.difference_hours != 0)
            resumes._treat_employee_resumes(employee, max_fec.date)
            resumes.write({'treated': True})

    def _treat_employee_resumes(self, employee, date):
        allocation_obj = self.env['hr.leave.allocation']
        hours = sum(self.mapped('difference_hours'))
        vals = self._catch_values_for_create_allocation(employee, date, hours)
        allocation = allocation_obj.create(vals)
        vals = {'treated': True,
                'hr_leave_allocation_id': allocation.id}
        self.write(vals)

    def _catch_values_for_create_allocation(self, employee, date, hours):
        status = self.env.ref(
            'hr_attendance_resume_absences.hr_leave_type_holiday_bonus')
        calendar = employee._get_employee_calendar(date=date)
        days = hours / calendar.hours_per_day
        vals = {
            'name': _('Time difference by hours'),
            'attendance_resume_date': date,
            'created_from_attendance_resume': True,
            'holiday_status_id': status.id,
            'holiday_type': 'employee',
            'employee_id': employee.id,
            'number_of_days': days,
            'difference_hours': hours,
            'creation_date_from_resume': fields.Date.context_today(self)}
        return vals
