from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
import json
_logger = logging.getLogger(__name__)

class PurchaseOrderDecline(models.Model):
    _name = 'purchase.order.decline'
    _description = 'Productos Rechazados'

    name = fields.Text(string='Description')
    product_qty = fields.Float(string='Cantidad', digits='Product Unit of Measure', required=True)
    product_id = fields.Many2one('product.product', string='Producto', domain=[('purchase_ok', '=', True)], change_default=True)
    price_unit = fields.Float(string='Precio unitario', required=True, digits='Product Price')

    price_subtotal = fields.Monetary(string='Subtotal')
    taxes_id = fields.Many2many('account.tax', string='Impuestos', domain=['|', ('active', '=', False), ('active', '=', True)])

    order_id = fields.Many2one('purchase.order', string='Order Reference', index=True, required=True, ondelete='cascade')

    currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)