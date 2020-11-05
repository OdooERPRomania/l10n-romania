# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    order_code = fields.Char("Order Code")
