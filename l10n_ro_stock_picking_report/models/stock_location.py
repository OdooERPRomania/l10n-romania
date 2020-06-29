# -*- coding: utf-8 -*-
# ©  2008-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details



from odoo import models, fields, api, _


class stock_location(models.Model):
    _inherit = "stock.location"

    user_id = fields.Many2one('res.users', string='Manager')
