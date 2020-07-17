from odoo import models, fields, api, _



class res_partner(models.Model):
    _inherit = 'res.partner'

    mean_transp = fields.Char(string='Mean transport')
