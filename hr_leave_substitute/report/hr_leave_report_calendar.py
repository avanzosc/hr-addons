# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models, tools


class HrLeaveReportCalendarInherited(models.Model):
    _inherit = (
        "hr.leave.report.calendar"  # Asegúrate de que el nombre de modelo sea correcto.
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, "hr_leave_report_calendar")
        substitute_text = _(", Substitute: ")
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW hr_leave_report_calendar AS
            SELECT
            hl.id AS id,
            hl.id AS leave_id,

            hl.date_from AS start_datetime,
            hl.date_to AS stop_datetime,

            hl.employee_id AS employee_id,
            hl.state AS state,

            hl.department_id AS department_id,
            hl.number_of_days AS duration,
            hl.private_name AS description,
            hl.holiday_status_id AS holiday_status_id,

            em.company_id AS company_id,
            em.job_id AS job_id,

            COALESCE(
                rr.tz,
                rc.tz,
                cc.tz,
                'UTC'
            ) AS tz,

            (hl.state = 'refuse') AS is_striked,
            (hl.state NOT IN ('validate', 'refuse')) AS is_hatched,

            CONCAT(
                em.name, ': ', hl.number_of_days,
                CASE
                    WHEN hl.substitute_id IS NOT NULL THEN
                        ', ' || %s || sub_partner.name
                    ELSE ''
                END
            ) AS name

        FROM hr_leave hl
            LEFT JOIN hr_employee em
                ON em.id = hl.employee_id

            LEFT JOIN resource_resource rr
                ON rr.id = em.resource_id

            LEFT JOIN resource_calendar rc
                ON rc.id = em.resource_calendar_id

            LEFT JOIN res_company co
                ON co.id = em.company_id

            LEFT JOIN resource_calendar cc
                ON cc.id = co.resource_calendar_id

            LEFT JOIN res_users sub_user
                ON sub_user.id = hl.substitute_id

            LEFT JOIN res_partner sub_partner
                ON sub_partner.id = sub_user.partner_id

        WHERE
            hl.state IN ('confirm', 'validate', 'validate1', 'refuse')
        """,
        [
            substitute_text,
        ],
        )
