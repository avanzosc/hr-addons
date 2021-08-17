# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute("""
        DELETE FROM hr_employee_supervised_year a
        USING hr_employee_supervised_year b
        WHERE a.id > b.id
        AND a.student_id = b.student_id
        AND a.school_year_id = b.school_year_id
        AND a.teacher_id = b.teacher_id;
    """)

    if openupgrade.column_exists(
        cr,
        "calendar_event",
        "supervised_year_id"
    ):
        cr.execute("""
            UPDATE calendar_event c
            SET supervised_year_id = (
                SELECT id
                FROM hr_employee_supervised_year y
                WHERE y.student_id = c.student_id
                AND y.school_year_id = c.academic_year_id
                AND y.teacher_id = c.teacher_id
                ORDER BY id
                LIMIT 1)
            WHERE supervised_year_id NOT IN (
                SELECT id FROM hr_employee_supervised_year);
        """)

    cr.execute("""
        DELETE FROM hr_employee_supervised_year a
        USING hr_employee_supervised_year b
        WHERE a.id > b.id
        AND a.student_id = b.student_id
        AND a.school_year_id = b.school_year_id
    """)

    if openupgrade.column_exists(
        cr,
        "calendar_event",
        "supervised_year_id"
    ):
        cr.execute("""
            UPDATE calendar_event c
            SET supervised_year_id = (
                SELECT id
                FROM hr_employee_supervised_year y
                WHERE y.student_id = c.student_id
                AND y.school_year_id = c.academic_year_id
                ORDER BY id
                LIMIT 1)
            WHERE supervised_year_id NOT IN (
                SELECT id FROM hr_employee_supervised_year);
        """)
