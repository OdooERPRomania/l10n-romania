# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AnafDeclaration(models.Model):
    _name = "anaf.declaration"
    _description = "Anaf Declaration"

    name = fields.Char(string="Name", required=True)
    version_ids = fields.One2many(
        "anaf.declaration.version", "declaration_id", string="Versions"
    )


class AnafDeclarationVersion(models.Model):
    _name = "anaf.declaration.version"
    _description = "Anaf Declaration Version"
    _order = "declaration_id, name desc"

    name = fields.Char(string="Name", required=True)
    model = fields.Many2one(
        "ir.model", string="Odoo Model", required=True, ondelete="cascade"
    )
    declaration_id = fields.Many2one(
        "anaf.declaration", string="Declaration", required=True
    )
    validator = fields.Binary(string="Validator File")
