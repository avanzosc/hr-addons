# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Hr Employee Associated Picking',
    'version': '11.0.1.0.0',
    'license': "AGPL-3",
    'author':  "AvanzOSC",
    'website': 'http://www.avanzosc.es',
    'contributors': [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es",
    ],
    'category': 'Human Resources',
    'depends': [
        'stock',
        'hr_employee_catch_partner',
    ],
    'data': [
        "views/hr_employee_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
