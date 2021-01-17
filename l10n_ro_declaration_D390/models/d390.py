# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ANAFD390(models.TransientModel):
    _name = "anaf.d390"
    _inherit = "anaf.mixin"
    _description = "Declaratie 390"

    @api.model
    def _get_default_declaration(self):
        d390 = self.env["anaf.declaration"].search([("name", "=", "d390")], limit=1)
        if d390:
            return d390
        return super()._get_default_declaration()

    declaration_id = fields.Many2one(default=_get_default_declaration)
