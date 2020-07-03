# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_is_zero, float_compare


# all just adds a field in view;  
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

# the relation from  stock_inventory   acc_move_line_ids = fields.One2many.
#  just to show in view
    stock_inventory_id = fields.Many2one(
        "stock.inventory", readonly=1,
        string="Stock Inventory",
        help="This account move line has been generated by this inventory. A field made just in this module just to show in inventory",
    )

# to know that this account.move.line was for a change of price in a location type store
# just showing in form view
    stock_location_id = fields.Many2one(
        "stock.location", readonly=1,
        string="Price change in this location",
        help="This account move line has been generated by a change of price for this location ( the location has a inventory valuation at sale price (shop))",
    )


# MAyBE OK? NOT TO CHAGE IN INVOICE QTY OF RECIVEND PRODUCTS???
    # @api.onchange('quantity')
    # def _onchange_quantity(self):
    #     message = ''
    #     if self.move_id.type in ['in_refund', 'out_refund']:
    #         return
    #     if self.product_id and self.product_id.type == 'product':
    #
    #         if self.purchase_line_id:
    #             qty = 0
    #             for inv_line in self.purchase_line_id.invoice_lines:
    #                 if not isinstance(inv_line.id, models.NewId) and inv_line.move_id.state not in ['cancel']:
    #                     if inv_line.move_id.type == 'in_invoice':
    #                         qty += inv_line.uom_id._compute_quantity(inv_line.quantity,
    #                                                                  self.purchase_line_id.product_uom)
    #                     elif inv_line.move_id.type == 'in_refund':
    #                         qty -= inv_line.uom_id._compute_quantity(inv_line.quantity,
    #                                                                  self.purchase_line_id.product_uom)
    #
    #             qty_invoiced = qty
    #
    #             qty = self.purchase_line_id.qty_received - qty_invoiced
    #
    #             qty = self.purchase_line_id.product_uom._compute_quantity(qty, self.uom_id)
    #
    #             if qty < self.quantity:
    #                 raise UserError(
    #                     _('It is not allowed to record an invoice for a quantity bigger than %s') % str(qty))
    #         else:
    #             message = _('It is not indicated to change the quantity of a stored product!')
    #     if message:
    #         return {
    #             'warning': {'title': "Warning", 'message': message},
    #         }
