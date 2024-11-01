from odoo import models, fields, _
import logging
from datetime import datetime, time
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class SurveyWizard(models.Model):
    _name = 'survey.wizard'
    _description = 'Survey Wizard'
    
    partner_id = fields.Many2one('res.partner', string="Proveedor", required=True,readonly=True)
    order_id = fields.Many2one('purchase.order', string="Orden de compra",required=True,readonly=True)
    
    val_financiera = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Valoración financiera')
    val_tecnica = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Valoración técnica')
    cal_producto = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Calidad de los productos')
    
    demora_entrega = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Tiempos de entrega')

    def action_confirm(self):
        # Guardar el registro y calcular los promedios
        _logger.info("Confirmación de la encuesta realizada.")
        
        # Llamar a la función para actualizar los promedios
        self._update_supplier_average()

        # Mostrar mensaje de éxito

    def _update_supplier_average(self):
        # Obtén todas las encuestas anteriores de este proveedor
        surveys = self.search([('partner_id', '=', self.partner_id.id)])
        
        # Convertir las valoraciones a números para calcular el promedio
        fields_to_average = ['val_financiera', 'val_tecnica', 'cal_producto', 'nuevo_campo']
        
        # Diccionario para almacenar los promedios
        averages = {}
        
        for field in fields_to_average:
            values = surveys.mapped(field)
            numeric_values = [int(v) for v in values if v]  # Convertir a número si no está vacío
            if numeric_values:
                average = sum(numeric_values) / len(numeric_values)
                averages[field] = average
        
        # Actualizar directamente los campos en el modelo de proveedor
        _logger.info(f"Val_financiera: {str(int(round(averages['val_financiera'])))}")
        self.partner_id.write({
            'val_financiera': str(int(round(averages['val_financiera']))),
            'val_tecnica': str(int(round(averages['val_tecnica']))),
            'cal_producto': str(int(round(averages['cal_producto']))),
            'demora_entrega': str(int(round(averages['demora_entrega']))),
        })
        self.order_id.survey_id = self.id
        _logger.info(f"Promedios actualizados para el proveedor {self.partner_id.name}.")
    