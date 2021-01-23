# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCopany(models.Model):
    _inherit = "res.company"

    optiune = fields.Boolean("ANAF Crosschecking")
