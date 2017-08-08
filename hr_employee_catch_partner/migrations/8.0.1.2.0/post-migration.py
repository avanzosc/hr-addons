# -*- coding: utf-8 -*-
# © Copyright 2017 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def remove_duplicate_res_partner_employee_references(cr):
    sql = ("update res_partner "
           "set employee_id = null "
           "where id in "
           "(select r.id "
           "from res_partner r inner join hr_employee h "
           "on r.employee_id = h.id "
           "where h.address_home_id != r.id)")
    cr.execute(sql)
    sql2 = ("update res_partner res "
            "set employee_id = sub.id "
            "from "
            "(select h.id, h.address_home_id "
            "from res_partner r inner join hr_employee h on "
            "h.address_home_id = r.id "
            "where r.employee_id is null) as sub "
            "where res.id = sub.address_home_id")
    cr.execute(sql2)


def migrate(cr, version):
    if not version:
        return
    remove_duplicate_res_partner_employee_references(cr)
