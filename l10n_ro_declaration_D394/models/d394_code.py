# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from odoo import _, api, fields, models
# from odoo.exceptions import ValidationError
#
#
# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     d394_id = fields.Many2one("report.394.code", string="D394 codes")
#
#
# class ANAFD394Code(models.Model):
#     _name = "anaf.394.code"
#     _description = "D394 code"
#     _parent_store = True
#     _order = "name"
#
#     name = fields.Char("D394 Code")
#     parent_id = fields.Many2one(
#         "anaf.394.code", "Parent Code", index=True, ondelete="restrict"
#     )
#     child_ids = fields.One2many("anaf.394.code", "parent_id", "Child Codes")
#     description = fields.Char("Description")
#     product_ids = fields.One2many("product.product", "d394_id", string="Products")
#
#     @api.constrains("parent_id")
#     def _check_parent_id(self):
#         if not self._check_recursion():
#             raise ValidationError(_("You can not create recursive codes."))
