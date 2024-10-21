from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
import json
_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    accept = fields.Boolean('Producto aceptado', default=False)

    def delete_record(self):
        self.unlink()
        return True

    @api.model
    def get_data(self,domain,domain_order):
        purchase = self.env['purchase.order.line'].search(domain)
        purchase_order = self.env['purchase.order'].search(domain_order)
        data = {}
        data['product_id']={}
        product_list = [] # Listado de los productos que contienen las cotizaciones
        order_list =[] # Listado de las cotizaciones
        # Recorriendo todos los registros para agregar el listado de productos
        for record in purchase:
            details_list=[] # Estan la cantidad, precio, etc.
            flag = False # Utilizado para saber si el producto ya esta agregado a la lista para no repetirla
            for product in product_list:
                if record.product_id.id == product['id']:
                    flag = True
                    """ for line in purchase:
                        if line.product_id.id == record.product_id.id:  
                            details_list.append({'id':record.id, 'state': record.order_id.state,'cantidad':record.product_qty,'precio':record.price_subtotal})
                        else:

                            details_list.append({'id':False, 'state': 'purchase','cantidad':'-','precio':'-'}) """
                    break
                else:
                    flag = False
            if flag == False:
                for order in purchase_order:
                    flag_2 = False # Utilizado para saber si hay el producto en la cotización

                    # aqui se agrega todas la información con los detalles del producto ej.
                    # cajon grande, {2,$40,$80},{1,$10,$10} y cada {} es una citización-
                    for line in order.order_line:
                        if line.product_id.id == record.product_id.id:  
                            details_list.append({'id':line.id,'order_id':line.order_id.id, 'state': line.order_id.state,'product_qty':line.product_qty, 'price_unit': line.price_unit,'subtotal':line.price_subtotal})
                            flag_2 = True
                    if flag_2 == False: # En caso de no haber agrega "-" en cada linea
                        details_list.append({'id':False, 'state': 'purchase','product_qty': '-','price_unit':'-','subtotal':'-'})
                product_list.append({'id':record.product_id.id, 'name':record.product_id.name, 'details': details_list})
        # Recorrido para sacar la información de las cotizaciones
        for record in purchase_order:
            flag = False
            for order in order_list:
                if record.id == order['id']:
                    flag = True
                    break
                else:
                    flag = False
            if flag == False:
                attachment = []
                attachment_ids = self.env['ir.attachment'].search([('res_id','=',record.id),('res_model','=','purchase.order')])
                for row in attachment_ids:
                    attachment.append({'id':row.id,'name':row.name,'access_token':row.access_token})
                # Información necesaria de las ordenes de compra, junto con la información del contacto.
                order_list.append({
                    'id':record.id, 
                    'name':record.name, 
                    'partner_id':record.partner_id.id, 
                    'partner_name': record.partner_id.name, 
                    'partner_phone':record.partner_id.phone,
                    'partner_email':record.partner_id.email,
                    'partner_val_financiera':record.partner_id.val_financiera,
                    'partner_val_tecnica':record.partner_id.val_tecnica,
                    'partner_cal_producto':record.partner_id.cal_producto,

                    'attachment':attachment,

                    'ventajas':record.ventajas,
                    'inconvenientes':record.inconvenientes,
                    'state': record.state, 
                    'date_planned': record.date_planned,
                    'currency_id': record.currency_id.name, 
                    'amount_tax':record.amount_tax,
                    'amount_total':record.amount_total})
        data.update({'product_list': product_list, 'order_list': order_list} )
    
        return data
    
    def open_wizard(context_id):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Abrir comparador',
                'res_model': "purchase.order",
                'view_type': 'form',
                'view_mode': 'form',
                'res_id':context_id,
                # 'context': {'order_ids': self.purchase_ids.ids},
                'target': 'main',
            }
    
   