# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, exceptions, _
from odoo.addons.resource.models.resource import HOURS_PER_DAY
from dateutil.relativedelta import relativedelta


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    attendance_resume_date = fields.Date(
        string='Attendance resume date')
    created_from_attendance_resume = fields.Boolean(
        string='Created from attendance resume', default=False)
    difference_hours = fields.Float(
        string='Difference hours')
    creation_date_from_resume = fields.Date(
        string='Creation date from resume')

    @api.multi
    @api.depends('number_of_days', 'employee_id')
    def _compute_number_of_hours_display(self):
        for allocation in self:
            if allocation and allocation.type_request_unit == "hour":
                allocation.number_of_hours_display = allocation.number_of_days
            elif (allocation.parent_id and
                  allocation.parent_id.type_request_unit == "hour"):
                allocation.number_of_hours_display = (
                    allocation.number_of_days * HOURS_PER_DAY)
            else:
                hours_per_day = (
                    allocation.employee_id.resource_calendar_id.hours_per_day)
                allocation.number_of_hours_display = (
                    allocation.number_of_days * (hours_per_day or
                                                 HOURS_PER_DAY))
    _sql_constraints = [
        ('duration_check', "CHECK (number_of_days == 0 )",
         "The number of days is cero."),
    ]

    @api.multi
    def name_get(self):
        res = []
        for allocation in self:
            target = allocation.employee_id.name
            if (not allocation.holiday_status_id or
                    allocation.holiday_status_id.request_unit != 'day'):
                if allocation.holiday_type == 'company':
                    target = allocation.mode_company_id.name
                elif allocation.holiday_type == 'department':
                    target = allocation.department_id.name
                elif allocation.holiday_type == 'category':
                    target = allocation.category_id.name
            if allocation.type_request_unit == 'hour':
                hours_days = allocation.number_of_hours_display
                mytype = _('hours')
            else:
                hours_days = allocation.number_of_days
                mytype = _('days')
            name = _(u'Allocation of {}: Employee {}, {} {}').format(
                allocation.holiday_status_id.name,
                target, round(hours_days, 2), mytype)
            if allocation.type_request_unit != 'hour':
                hours = allocation.number_of_days * 24
                name += _(u', hours: {}').format(round(hours, 2))
            res.append((allocation.id, name))
        return res


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    @api.multi
    def unlink(self):
        types = self.env['hr.leave.type']
        types += self.env.ref(
            'hr_attendance_resume_absences.hr_leave_type_holiday_bonus')
        for mtype in self:
            if mtype.id in types.ids:
                raise exceptions.Warning(
                    _('You cannot delete an leave type created by the system.')
                    )
        return super(HrLeaveType, self).unlink()


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    hour_from = fields.Float(string='Hour from')
    hour_to = fields.Float(string='Hour to')
    hours_per_day = fields.Float(string='Hours per day')
    show_hours = fields.Boolean(
        string='Show hours', compute='_compute_show_hours',
        store=True)
    old_request_date_from = fields.Date(
        string='Old request date')

    @api.multi
    @api.depends('leave_type_request_unit', 'request_date_from',
                 'request_date_to', 'employee_id')
    def _compute_show_hours(self):
        for leave in self:
            show_hours = True
            if (not leave.leave_type_request_unit or
                    leave.leave_type_request_unit == 'hour'):
                show_hours = False
            if (leave.request_date_from and leave.request_date_to and
                    leave.request_date_from != leave.request_date_to):
                show_hours = False
            leave.show_hours = show_hours

    @api.onchange('request_date_from_period', 'request_hour_from',
                  'request_hour_to', 'request_date_from', 'request_date_to',
                  'employee_id')
    def _onchange_request_parameters(self):
        if (not self.old_request_date_from or
                self.old_request_date_from != self.request_date_from):
            self.request_date_to = self.request_date_from
            self.old_request_date_from = self.request_date_from
        return super(HrLeave, self). _onchange_request_parameters()

    @api.onchange('request_date_from', 'request_date_to', 'employee_id',
                  'holidays_status_id')
    def _onchange_leave_dates(self):
        festive_obj = self.env['hr.holidays.public.line']
        if self.request_date_from and self.employee_id:
            calendar = self.employee_id._get_employee_calendar(
                date=self.request_date_from)
            work, hour_from, hour_to = self.employee_id._get_day_info(
                calendar, self.request_date_from)
            self.hour_from = hour_from
            self.hour_to = hour_to
            self.hours_per_day = work
            if self.request_date_to:
                from_date = self.request_date_from
                days = 0
                while from_date <= self.request_date_to:
                    country = self.employee_id.company_id.country_id
                    cond = [('date', '=', from_date),
                            ('year_id.country_id', '=', country.id),
                            ('year_id.year', '=', from_date.year)]
                    festive = festive_obj.search(cond, limit=1)
                    if not festive:
                        calendar = self.employee_id._get_employee_calendar(
                            date=from_date)
                        employee = self.employee_id
                        work, hour_from, hour_to = employee._get_day_info(
                            calendar, from_date)
                        if work:
                            days += 1
                    from_date = (from_date + relativedelta(days=1))
                self.number_of_days = days
