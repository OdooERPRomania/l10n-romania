# ©  2008-201 9Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_compare



class stock_picking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    # prin acest camp se indica daca un produs care e stocabil trece prin contul 408 / 418 la achizitie sau vanzare
    # receptie/ livrare in baza de aviz
    notice = fields.Boolean(
        "Is a notice",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        default=False,
        help = "Prin acest camp se indica daca un produs care e stocabil trece prin contul 408 / 418 la achizitie sau vanzare \nreceptie/ livrare in baza de aviz"
    )

#    has no purpose because the last line of _action_done() is writing the date_done as now.   
#     if is necessary must be first with super
#     def _action_done(self):
#         for pick in self:
#             pick.write({"date_done": pick.date})
#         res = super()._action_done()
#         return res

# exist in account_move
#     def action_cancel(self):
#         for pick in self:
#             for move in pick.move_lines:
#                 if move.account_move_ids:
#                     move.account_move_ids.button_cancel()
#                     move.account_move_ids.unlink()
#         return super().action_cancel()

# nu exista. poate este doar unlink   care mai intai face move_line._action_cancel()  deci este acelasi lucru ca aici
#     def action_unlink(self):
#         for pick in self:
#             for move in pick.move_lines:
#                 if move.account_move_ids:
#                     move.account_move_ids.button_cancel()
#                     move.account_move_ids.unlink()
#         return super().action_unlink()

# exist and is default True
# class StockReturnPickingLine(models.TransientModel):
#     _inherit = "stock.return.picking.line"
# 
#     to_refund = fields.Boolean(default=True)

# 
# class ReturnPicking(models.TransientModel):
#     _inherit = "stock.return.picking"
# 
# # orginal 
#     @api.model
#     def default_get(self, default_fields):
#         res = super(StockReturnPicking, self).default_get(default_fields)
#         for i, k, vals in res.get('product_return_moves', []):
#             vals.update({'to_refund': True})
# 
# # wanted to change, byt I think is the same
#     @api.model
#     def default_get(self, fields_list):
#         res = super().default_get(fields_list)
#         if "product_return_moves" in res:
#             product_return_moves = res["product_return_moves"]
#             for product_return_move in product_return_moves:
#                 product_return_move[2]["to_refund"] = True
#         return res
