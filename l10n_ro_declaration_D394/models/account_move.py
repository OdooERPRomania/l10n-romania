# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
import logging
from odoo import fields, models, api
_logger = logging.getLogger(__name__)
OPERATION_TYPE = [
    ("L", "Customer Invoice"),
    ("A", "Supplier Invoice"),
    ("LS", "Special Customer Invoice"),
    ("AS", "Special Supplier Invoice"),
    ("AI", "VAT on Payment Supplier Invoice"),
    ("V", "Inverse Taxation Customer Invoice"),
    ("C", "Inverse Taxation Supplier Invoice"),
    ("N", "Fizical Persons Supplier Invoice"),
]
SEQUENCE_TYPE = [
    ("normal", "Invoice"),
    ("autoinv1", "Customer Auto Invoicing"),
    ("autoinv2", "Supplier  Auto Invoicing"),
]
INVOICE_ORIGIN = [('', 'Company'),
                  ('1', 'facturi'),
                  ('2', 'borderouri'),
                  ('3', 'file carnet comercializare'),
                  ('4', 'contracte'),
                  ('5', 'alte documente')]
class product_product(models.Model):
    _inherit = "product.product"

    d394_id = fields.Many2one('report.394.code', string='D394 codes')

class AccountMove(models.Model):
    _inherit = "account.move"


  



    @api.depends('partner_id')
    def _get_partner_type(self):
        for inv in self:
            partner = inv.partner_id
            eur_countries = []
            eur_grp = self.env.ref('base.europe')
            if eur_grp:
                eur_countries = [country.id for country in eur_grp.country_ids]
            if partner.country_id and \
                partner.country_id.id == self.env.ref('base.ro').id:
                if partner.vat_subjected:
                    new_type = '1'
                else:
                    new_type = '2'
            elif partner.country_id.id in eur_countries:
                new_type = '3'
            else:
                new_type = '4'
            inv.partner_type = new_type
        return True

    sequence_type = fields.Selection(
        SEQUENCE_TYPE, string="Sequence Type"
    )

    invoice_origin_d394 = fields.Selection(INVOICE_ORIGIN, string = 'Document type', default = '1')

    inv_number = fields.Char(
        "Invoice Number", compute="_get_inv_number", store=True, index=True
    )
    partner_type = fields.Char(
        "D394 Partner Type", compute="_get_partner_type", store=True, index=True
    )
