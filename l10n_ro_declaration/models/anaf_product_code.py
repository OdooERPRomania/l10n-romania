# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ANAFD394Code(models.Model):
    _name = "anaf.product.code"
    _description = "ANAF Product code"
    _parent_store = True
    _order = "name"

    name = fields.Char("D394 Code")
    parent_id = fields.Many2one(
        "anaf.product.code", "Parent Code", index=True, ondelete="restrict"
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many("anaf.product.code", "parent_id", "Child Codes")
    description = fields.Char("Description")
    product_ids = fields.One2many("product.template", "anaf_code_id", string="Products")

    @api.constrains("parent_id")
    def _check_anaf_code_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive ANAF codes."))
        return True
