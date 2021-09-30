# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Hr Expense Event With Commute",
    'version': '14.0.1.0.0',
    'author': 'AvanzOSC',
    'website': 'http://www.avanzosc.es',
    'category': 'Marketing/Events',
    'license': 'AGPL-3',
    'depends': [
        'hr_expense_from_analytic',
        'event_with_commute',
    ],
    'data': [
        'views/event_view.xml'
    ],
    'installable': True,
    'auto_install': True,
}
