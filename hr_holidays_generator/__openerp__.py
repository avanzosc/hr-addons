# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Hr Holidays Generator",
    "version": "8.0.1.2.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Human Resources",
    "depends": [
        "hr_contract_stages",
        "hr_holidays",
        "hr_employee_catch_partner"
    ],
    "data": [
        "data/hr_holidays_generator_data.xml",
        "views/res_company_view.xml",
        "views/hr_holidays_status_view.xml",
        "views/hr_contract_type_view.xml"
    ],
    "installable": True,
}
