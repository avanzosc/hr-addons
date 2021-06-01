# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime
from pytz import timezone, utc

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrAttendanceReportXlsx(models.AbstractModel):
    _name = "report.hr_attendance.report_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def _get_date_format(self, lang):
        return "{} {}".format(lang.date_format, lang.time_format)

    def _format_date(self, date, lang):
        # format date following user language
        if not date:
            return False
        new_date = (
            fields.Datetime.from_string(date) if isinstance(date, str) else
            date)
        new_date = new_date.replace(tzinfo=utc)
        local_date = new_date.astimezone(timezone(self.env.user.tz or "UTC")
                                         ).replace(tzinfo=None)
        date_format = self._get_date_format(lang)
        return datetime.strftime(local_date, date_format)

    def create_new_sheet(self, workbook):
        lang_model = self.env["res.lang"]
        lang = lang_model._lang_get(self.env.user.lang)
        header_format = workbook.add_format({
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vjustify",
            "fg_color": "#F2F2F2",
        })
        date_format = workbook.add_format({
            "num_format": self._get_date_format(lang),
        })

        sheet = workbook.add_worksheet(_("Attendances"))

        sheet.write("A1", _("Employee"), header_format)
        sheet.write("B1", _("Check In"), header_format)
        sheet.write("C1", _("Check Out"), header_format)
        sheet.write("D1", _("Worked Hours"), header_format)

        sheet.set_column("B:C", 17, date_format)
        return sheet

    def fill_attendance_row_data(self, sheet, row, attendance):
        lang_model = self.env["res.lang"]
        lang = lang_model._lang_get(self.env.user.lang)
        sheet.write("A" + str(row), attendance.employee_id.display_name)
        sheet.write("B" + str(row),
                    self._format_date(attendance.check_in, lang))
        sheet.write("C" + str(row),
                    self._format_date(attendance.check_out, lang))
        sheet.write("D" + str(row), attendance.worked_hours)

    def generate_xlsx_report(self, workbook, data, objects):
        if not objects:
            raise UserError(
                _("You must select attendances to generate xlsx report."))
        new_sheet = self.create_new_sheet(workbook)
        row = 2
        for attendance in objects:
            self.fill_attendance_row_data(new_sheet, row, attendance)
            row += 1
