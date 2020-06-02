# -*- coding: utf-8 -*-
# ©  2017 Deltatech
# See README.rst file on addons root folder for license details


from odoo import models, fields, api, _



class ResPartner(models.Model):
    _inherit = "res.partner"

#     vat_subjected = fields.Boolean('VAT Legal Statement') # also in partner_create_by_vat
#     split_vat = fields.Boolean('Split VAT') # also in partner_create_by_vat      does not exist anymore from 2020
    