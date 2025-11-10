# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "HR Personal Equipment Show Companies",
    "summary":"Show employee and product companies on PPE Request assignments.",
    "version": "14.0.1.0.0",
    "category": "Hr",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/hr-addons",
    "depends": [
        'hr_personal_equipment_request',
        'product_multi_company_usability',
    ],
    "data": [
        'views/hr_personal_equipment_views.xml'
    ],
    "installable": True,
}

