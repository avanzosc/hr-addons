# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common
from dateutil.relativedelta import relativedelta


class TestEmployeeBirthdateCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEmployeeBirthdateCommon, cls).setUpClass()
        cls.employee_obj = cls.env["hr.employee"]
        cls.today = fields.Date.today()
        cls.bday_today = cls.employee_obj.create({
            "name": "Birthday is today",
            "birthday": cls.today,
        })
        new_employees = cls.employee_obj
        for days in range(1, 8):
            new_date = cls.today + relativedelta(days=days)
            new_employees |= cls.employee_obj.create({
                "name": "Bday is {}".format(new_date),
                "birthday": new_date,
            })
