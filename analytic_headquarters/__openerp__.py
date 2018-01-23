# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Analytic Headquarters",
    "version": "8.0.1.0.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Accounting & Finance",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet_invoice",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/headquarters_view.xml",
        "views/account_analytic_line_view.xml",
        "views/account_invoice_view.xml",
        "views/account_move_line_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
