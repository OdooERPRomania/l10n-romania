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

    def action_done(self):
        for pick in self:
            pick.write({"date_done": pick.date})
        res = super().action_done()
        return res

    def action_cancel(self):
        for pick in self:
            for move in pick.move_lines:
                if move.account_move_ids:
                    move.account_move_ids.button_cancel()
                    move.account_move_ids.unlink()
        return super().action_cancel()

    def action_unlink(self):
        for pick in self:
            for move in pick.move_lines:
                if move.account_move_ids:
                    move.account_move_ids.button_cancel()
                    move.account_move_ids.unlink()
        return super().action_unlink()

class StockReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(default=True)


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "product_return_moves" in res:
            product_return_moves = res["product_return_moves"]
            for product_return_move in product_return_moves:
                product_return_move[2]["to_refund"] = True
        return res
