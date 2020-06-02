
from odoo import api, fields, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

# just to show also date in known/advertise format
    inverted_rate = fields.Float(digits=0, compute="_computed_inverted_rate",store=True, traking=True)
    @api.depends('rate')
    def _computed_inverted_rate(self):
        for record in self:
            record.inverted_rate = 1.0/ record.rate if record.rate else 1 

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _name = "res.currency.rate"

    inverted_rate = fields.Float(digits=0, compute="_computed_inverted_rate",store=True, traking=True)
    @api.depends('rate')
    def _computed_inverted_rate(self):
        for record in self:
            record.inverted_rate = 1.0/ record.rate
#/ just to show also date in known/advertise format
