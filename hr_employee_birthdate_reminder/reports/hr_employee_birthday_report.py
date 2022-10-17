# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, tools
from psycopg2.extensions import AsIs


class HrEmployeeBirthdateReport(models.Model):
    _name = "hr.employee.birthday.report"
    _inherit = "hr.employee.birthdate.report"
    _description = "Employee's Birthdate Report"
    _auto = False
    _rec_name = "employee_id"

    def _select(self):
        return super(HrEmployeeBirthdateReport, self)._select()

    def _from(self):
        return super(HrEmployeeBirthdateReport, self)._from()

    def _where(self):
        where_str = """
            AND
                DATE_PART('day', birthday) = date_part('day', CURRENT_DATE)
            AND
                DATE_PART('month', birthday) = date_part('month', CURRENT_DATE)
        """
        return super(HrEmployeeBirthdateReport, self)._where() + where_str

    def _group_by(self):
        return super(HrEmployeeBirthdateReport, self)._group_by()

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()),
                AsIs(self._from()), AsIs(self._where()),
                AsIs(self._group_by()),))
