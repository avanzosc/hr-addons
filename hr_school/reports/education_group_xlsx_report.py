# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo import _, models

_logger = logging.getLogger(__name__)


class EducationGroupXlsx(models.AbstractModel):
    _inherit = "report.education.education_group_xlsx"

    def create_group_sheet(self, workbook, book):
        sheet = super(EducationGroupXlsx, self).create_group_sheet(
            workbook, book)
        title_format = workbook.add_format({
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vjustify",
        })
        header_format = workbook.add_format({
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vjustify",
            "fg_color": "#F2F2F2",
        })
        subheader_format = workbook.add_format({
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vjustify",
        })

        sheet.merge_range("A1:F1", _("STUDENT LIST"), title_format)
        sheet.merge_range(
            "C2:F2", book.center_id.display_name, subheader_format)
        sheet.merge_range(
            "C3:F3", book.academic_year_id.display_name, subheader_format)
        sheet.merge_range(
            "C4:F4", book.course_id.description, subheader_format)
        sheet.merge_range("A5:F5", book.description, header_format)

        sheet.write("F7", _("Supervising Professor"), subheader_format)
        sheet.set_column("F:F", 40)
        return sheet

    def fill_student_row_data(self, sheet, row, student, academic_year):
        super(EducationGroupXlsx, self).fill_student_row_data(
            sheet, row, student, academic_year)
        supervised_proffesor = student.year_tutor_ids.filtered(
            lambda t: t.school_year_id == academic_year)
        sheet.write(
            "F" + str(row), supervised_proffesor[:1].teacher_id.display_name)
