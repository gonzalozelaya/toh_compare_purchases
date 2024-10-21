from odoo import models, fields, api,_
from odoo.exceptions import UserError
import logging
import json
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    val_financiera = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
    ], 'Valoración financiera')
    val_tecnica = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
    ], 'Valoración técnica')
    cal_producto = fields.Selection([
        ('1', 'Pésimo'),
        ('2', 'Mal'),
        ('3', 'Bueno'),
        ('4', 'Muy bueno'),
    ], 'Calidad de los productos')
    
   