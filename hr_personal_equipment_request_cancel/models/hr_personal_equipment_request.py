from odoo import models


class HrPersonalEquipmentRequest(models.Model):
    _inherit = "hr.personal.equipment.request"

    def cancel_request(self):
        res = super().cancel_request()
        if "picking_ids" not in self._fields:
            return res
        pickings = self.mapped("picking_ids")
        pickings.filtered(lambda picking: picking.state == "done").do_cancel_done()
        pickings.filtered(lambda picking: picking.state != "cancel").action_cancel()
        return res
