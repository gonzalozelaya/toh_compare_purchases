from odoo import models, fields, api,_

class ResPartner(models.Model):
    _inherit = 'res.partner'

    val_financiera = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Valoración financiera', readonly=True)
    val_tecnica = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], string='Valoración técnica',readonly=True)
    cal_producto = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Calidad de los productos',readonly=True)
    
    demora_entrega = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
        ('5', 'Excelente'),
        ('6', 'God'),
    ], 'Nuevo campo xd',readonly=True)
    
   