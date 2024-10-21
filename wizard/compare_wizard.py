from odoo import models, fields,_
import logging
from odoo.exceptions import UserError,ValidationError
_logger = logging.getLogger(__name__)
# ---------------------------------------------------
# Modelo para el wizard de cambio de usuario y contraseña
# ---------------------------------------------------
class change_data_wizard(models.TransientModel):
    
    _name = 'compare.wizard'
    _description =  'Selecciona que ver'

    # ---------------------------------------------------
    # Método para obtener la id y el name
    # ---------------------------------------------------
    # Cuando el modelo es llamado, estas funciones obtienen los datos a travéz del context
    # se encuentra en la llamada.
    # Estos datos (id, name) son de la cuenta en la que se seleccionó editar.
    def _default_order_ids(self):
        return self._context['order_ids']

    order_ids = fields.Char("Id's", default=_default_order_ids)
    
    def open_pivot_graph_button(self):

        pivot_id = self.env.ref('toh_compare_purchases.purchase_order_line_compare_pivot').id
        graph_id = self.env.ref('toh_compare_purchases.purchase_order_line_compare_graph').id
        return {
            'name': 'Comparar',
            'type': 'ir.actions.act_window',
            'views': [[pivot_id, "pivot"],[graph_id,'graph']],
            #'view_mode': 'tree,pivot,graph',
            'res_model': 'purchase.order.line',
            #'view_id': self.env.ref('toh_compare_purchases.purchase_compare_act_window').id,
            'domain': [('order_id', 'in', eval(self.order_ids))]
            #'target': 'new',
            #'context': ctx,
        }
    
    def open_dashboard_button(self):
        domain = {'domain': [('order_id', 'in', eval(self.order_ids))]}
        self.validate_duplicate_products()
        _logger.info(domain)
        return {
            'type': 'ir.actions.client',
            'name': 'Comparar cotizaciones',
            'tag': 'CompareTemplate', 
            'context': {'purchase_order_ids': eval(self.order_ids)}
        }
    
    #verifica que un producto no este en mas de una linea
    def validate_duplicate_products(self):
        seen_products = set()
        orders = self.env['purchase.order'].search([('id', 'in', eval(self.order_ids))])
        for order in orders:
            seen_products.clear()
            for line in order.order_line:
                product_id = line['product_id']
                if product_id in seen_products:
                    raise ValidationError(f"La order {order.name} contiene el producto {product_id.name} en más de una línea. No es posible realizar una comparativa")
                else:
                    seen_products.add(product_id)
        
            


