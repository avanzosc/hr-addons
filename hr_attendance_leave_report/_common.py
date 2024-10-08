# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta


def _get_local_date(date_to_convert, tz="UTC"):
    if isinstance(date_to_convert, str):
        date_to_convert = datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S")
    local_tz = pytz.timezone(tz)
    if date_to_convert.tzinfo is None:
        date_to_convert = pytz.utc.localize(date_to_convert)
    return date_to_convert.astimezone(local_tz)


def _catch_employees_dates_to_treat(employee_dates, employee, date_from, date_to):
    date_from = date_from
    date_to = date_to
    while date_from <= date_to:
        found_company_employee = False
        for employee_date in employee_dates:
            if employee_date.get("employee") == employee:
                found_company_employee = True
                if date_from not in employee_date.get("work_date"):
                    employee_date["work_date"].append(date_from)
        if not found_company_employee:
            vals = {"employee": employee, "work_date": [date_from]}
            employee_dates.append(vals)
        date_from = date_from + relativedelta(days=1)
    return employee_dates
