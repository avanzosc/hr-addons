# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agrpl-3.0.html
from odoo import models, fields, api


class Hrleave(models.Model):
    _inherit = 'hr.leave'

    @api.multi
    def get_date_from_to(self):
        date_from = fields.Datetime.now
        date_to = fields.Datetime.now
        if 'from_resume' in self.env.context:
            date_from = ('{} 08:00:00').format(
                self.env.context.get('request_date'))
            date_to = ('{} 20:00:00').format(
                self.env.context.get('request_date'))
        for leave in self:
            leave.date_from = date_from
            leave.date_to = date_to

    date_from = fields.Datetime(default=get_date_from_to)
    date_to = fields.Datetime(default=get_date_from_to)
