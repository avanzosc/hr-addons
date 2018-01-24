# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Hr Employee Product',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'summary': '''Hr employee with product''',
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Human Resources',
    'depends': [
        'project',
        'hr_timesheet',
        'account'
    ],
    'data': [
        "views/hr_employee_view.xml",
        "views/account_analytic_line_view.xml"
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
