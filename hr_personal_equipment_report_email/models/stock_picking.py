# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
import base64


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            if picking.equipment_request_id and picking.equipment_request_id.employee_id:
                employee = picking.equipment_request_id.employee_id
                
                if ',' in employee.name:
                    parts = [p.strip() for p in employee.name.split(',')]
                    formatted_name = f"{parts[1].replace(' ', '_')}_{parts[0].replace(' ', '_')}"
                else:
                    formatted_name = employee.name.replace(' ', '_')
                
                template = self.env.ref('hr_personal_equipment_report_email.mail_template_ppe_delivery')
                report_action = self.env.ref('hr_personal_equipment_report_email.action_personal_equipment_report')
                pdf_content, _ = report_action._render_qweb_pdf([picking.id])

                attachment = self.env['ir.attachment'].create({
                    'name': f"PPE_Report_{formatted_name}.pdf",
                    'type': 'binary',
                    'datas': base64.b64encode(pdf_content),
                    'res_model': 'stock.picking',
                    'res_id': picking.id,
                    'mimetype': 'application/pdf',
                })

                template.send_mail(picking.id, force_send=True, email_values={
                    'attachment_ids': [attachment.id],
                })
        return res
