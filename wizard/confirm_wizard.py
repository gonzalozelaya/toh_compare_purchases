from odoo import models, fields, _
import logging
from datetime import datetime, time
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)
# ---------------------------------------------------
# Modelo para el wizard de cambio de usuario y contraseña
# ---------------------------------------------------


class ConfirmWizard(models.TransientModel):

    _name = 'confirm.wizard'
    _description = 'Wizard de confirmación'

    def _default_order_ids(self):
        return self._context['orders']

    order_ids = fields.Char("Id's", default=_default_order_ids)

    def confirm_orders(self):
        # Busca las lineas de la orden para eliminar las que no se confirmaron en la cotización
        for record in self._context['orders']:
            id = record['id']
            product_id = record['product_id']
            order_line = self.env['purchase.order.line'].search(
                [('order_id.id', '=', id), ('product_id.id', '=', product_id)])
            if record['accept'] == False:
                self.env['purchase.order.decline'].create(
                    self.get_data(order_line))
                order_line.unlink()
        # Una vez eliminado las lineas que son rechazadas cancelas las ordenes que estan vacias y confirma las que no
        for rec in self._context['orders']:
            id = rec['id']
            order = self.env['purchase.order'].search([('id', '=', id)])
            if order.state not in ['purchase','cancel']:
                if len(order.order_line) == 0:
                    order.button_cancel()
                else:
                    order.aprobado_por = self._uid
                    order.aprobado_el = datetime.now()
                    order.button_confirm()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def get_data(self, order_line):
        return {
            'order_id': order_line.order_id.id,
            'name': order_line.name,
            'product_qty': order_line.product_qty,
            'product_id': order_line.product_id.id,
            'price_unit': order_line.price_unit,
            'price_subtotal': order_line.price_subtotal,
            'taxes_id': order_line.taxes_id.ids,

        }
