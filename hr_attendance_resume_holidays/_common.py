# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, _


def _catch_dayofweek(date):
    day = str(date.weekday())
    if day == '0':
        return _('Monday')
    if day == '1':
        return _('Tuesday')
    if day == '2':
        return _('Wednesday')
    if day == '3':
        return _('Thursday')
    if day == '4':
        return _('Friday')
    if day == '5':
        return _('Saturday')
    if day == '6':
        return _('Sunday')
