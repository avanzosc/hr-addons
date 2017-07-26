# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def assign_contract_in_partner_calendar(cr):
    contracts = []
    sql = ("SELECT c.id as contract_id, r.id as partner_id, "
           "c.date_start, c.date_end "
           "FROM   hr_contract c, res_partner r "
           "where  c.employee_id = r.employee_id")
    cr.execute(sql)
    for contract in cr.fetchall():
        vals = {'contract_id': contract[0],
                'partner': contract[1],
                'date_start': contract[2],
                'date_end': contract[3]}
        contracts.append(vals)
    for contract in contracts:
        if contract.get('date_end', False):
            cr.execute(("UPDATE res_partner_calendar_day "
                        "set contract = %s "
                        "where partner = %s "
                        "and   date >= '%s' "
                        "and   date <= '%s'") %
                       (contract.get('contract_id'), contract.get('partner'),
                        contract.get('date_start'), contract.get('date_end')))
        else:
            cr.execute(("UPDATE res_partner_calendar_day "
                        "set contract = %s "
                        "where partner = %s "
                        "and   date >= '%s'") %
                       (contract.get('contract_id'), contract.get('partner'),
                        contract.get('date_start')))


def migrate(cr, version):
    if not version:
        return
    assign_contract_in_partner_calendar(cr)
