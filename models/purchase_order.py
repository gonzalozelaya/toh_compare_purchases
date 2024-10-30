from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
import json
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    ventajas = fields.Text('Ventajas')
    inconvenientes = fields.Text('Inconvenientes')
    validez_oferta = fields.Datetime('Validez de la oferta')
    forma_pago = fields.Char('Forma de pago')
    aprobado_por = fields.Many2one('res.users',string='Aprobado por', readonly=True)
    aprobado_el = fields.Datetime('Aprobado el', readonly=True)

    order_decline = fields.One2many('purchase.order.decline', 'order_id', string='Rechazados')

    survey_id = fields.Many2one('survey.wizard', string='Encuesta', readonly=True)
    
    def open_survey(self):
        for record in self:
            if record.state != 'purchase':
                raise UserError('La orden debe estar confirmada para poder realizar la encuesta')
            existing_survey = self.env['survey.wizard'].search([('order_id', '=', record.id)], limit=1)
            if existing_survey:
                raise UserError('Ya existe una encuesta asociada a esta orden de compra.')
            if record.user_id != self.env.user:
                raise UserError('Solo el comprador asignado puede realizar la encuesta.')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Encuesta de proveedor',
                'res_model': 'survey.wizard',
                'view_mode': 'form',
                'target': 'new',
                # Aquí pasamos el partner_id al wizard mediante el contexto
                'context': {
                    'default_partner_id': record.partner_id.id,
                    'default_order_id': record.id,
                    },
            }
    
    def open_wizard(self):
        if len(self) < 2:
            raise UserError(_("Por favor seleccione dos o mas registros para poder comparar."))
        draft = True
        for record in self:
            if record.state == 'purchase' or record.state=='cancel' or record.state=='done':
                draft = False
        if draft == False:
            raise UserError(_("No se pueden comparar cotizaciones ya confirmadas o canceladas."))
        return {
                'type': 'ir.actions.act_window',
                'name': 'Abrir comparador',
                'res_model': 'compare.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'context': {'order_ids': self.ids},
                'target': 'new',
            }
    
    
   