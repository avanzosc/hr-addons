# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools
from psycopg2.extensions import AsIs

MONTH_SELECTION = [(1, 'January'),
                   (2, 'February'),
                   (3, 'March'),
                   (4, 'April'),
                   (5, 'May'),
                   (6, 'June'),
                   (7, 'July'),
                   (8, 'August'),
                   (9, 'September'),
                   (10, 'October'),
                   (11, 'November'),
                   (12, 'December')]


class HrEmployeeBirthdateReport(models.Model):
    _name = "hr.employee.birthdate.report"
    _description = "Employee's Birthdate Report"
    _auto = False
    _rec_name = "employee_id"

    employee_id = fields.Many2one(comodel_name="hr.employee")
    birthdate = fields.Date()
    birthdate_day = fields.Integer()
    birthdate_month = fields.Selection(selection=MONTH_SELECTION)
    birthdate_year = fields.Integer()

    _depends = {
        "hr.employee": [
            "birthday",
        ],
    }

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER () as id,
                emp.id as employee_id,
                emp.birthday as birthdate,
                EXTRACT (YEAR FROM birthday) AS birthdate_year,
                EXTRACT (MONTH FROM birthday) AS birthdate_month,
                EXTRACT (DAY FROM birthday) AS birthdate_day
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
                hr_employee emp
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE
                emp.birthday IS NOT NULL
            AND
                active = True
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                emp.id, emp.birthday
        """
        return group_by_str

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
