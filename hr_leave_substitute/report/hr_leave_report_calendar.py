# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models, tools


class HrLeaveReportCalendarInherited(models.Model):
    _inherit = (
        "hr.leave.report.calendar"  # Asegúrate de que el nombre de modelo sea correcto.
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, "hr_leave_report_calendar")

        # Traducción de la cadena
        substitute_text = _(", Substitute: ")

        self._cr.execute(
            """CREATE OR REPLACE VIEW hr_leave_report_calendar AS
        (SELECT
            row_number() OVER() AS id,
            CONCAT(em.name, ': ', hl.duration_display,
                CASE
                    WHEN hl.substitute_id IS NOT NULL THEN ', ' || %s || sub_partner.name
                    ELSE ''
                END
            ) AS name,
            hl.date_from AS start_datetime,
            hl.date_to AS stop_datetime,
            hl.employee_id AS employee_id,
            hl.state AS state,
            em.company_id AS company_id,
            CASE
                WHEN hl.holiday_type = 'employee' THEN rr.tz
                ELSE %s
            END AS tz
        FROM hr_leave hl
            LEFT JOIN hr_employee em
                ON em.id = hl.employee_id
            LEFT JOIN res_users sub_user
                ON sub_user.id = hl.substitute_id
            LEFT JOIN res_partner sub_partner
                ON sub_partner.id = sub_user.partner_id
            LEFT JOIN resource_resource rr
                ON rr.id = em.resource_id
        WHERE
            hl.state IN ('confirm', 'validate', 'validate1')
        ORDER BY id);
        """,
            [
                substitute_text,
                self.env.company.resource_calendar_id.tz or self.env.user.tz or "UTC",
            ],
        )
