# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RunDeclaration(models.TransientModel):
    _name = "anaf.d390"
    _inherit = "anaf.mixin"
    _description = "Declaratie 390"

    intocmit_id = fields.Many2one(
        "res.partner",
        string="Intocmit",
    )
    optiune = fields.Boolean(string="optiune")
    schimb_optiune = fields.Boolean(string="schimb_optiune")
    prsAfiliat = fields.Boolean(string="prsAfiliat")


