from odoo import models, fields, api, _
from odoo.exceptions import UserError
class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    compare_count = fields.Integer('Comparar', compute='_compute_compare_count')

    def open_wizard(self):
        if len(self.purchase_ids) < 2:
            raise UserError(_("Se necesitan 2 o mas RFQ/Órdenes para poder comparar."))
        return {
                'type': 'ir.actions.act_window',
                'name': 'Abrir comparador',
                'res_model': 'compare.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'context': {'order_ids': self.purchase_ids.ids},
                'target': 'new',
            }
    
    @api.depends('order_count')
    def _compute_compare_count(self):
        for record in self:
            record.compare_count = record.order_count