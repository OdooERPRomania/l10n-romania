# -*- coding: utf-8 -*-
# ©  2008-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details



from odoo import models, fields, api, _



class res_partner(models.Model):
    _inherit = 'res.partner'

    mean_transp = fields.Char(string='Mean transport')
