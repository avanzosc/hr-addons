from odoo import models


class HrPersonalEquipmentRequest(models.Model):
    _inherit = "hr.personal.equipment.request"

    def cancel_request(self):
        res = super().cancel_request()
        for request in self:
            for picking in request.picking_ids:
                if picking.state == "done":
                    picking.do_cancel_done()
                if picking.state != "cancel":
                    picking.action_cancel()
        return res
