from odoo import models, fields, api

class WorkSchedule(models.Model):
    _name = 'employee.work.schedule'
    _description = 'Employee Work Schedule'

    name = fields.Char('Name', required=True)
    working_hours = fields.Float('Working Hours per Day', required=True)
    shift_type = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ], string='Shift Type')
