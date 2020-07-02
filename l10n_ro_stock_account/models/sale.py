# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self,sequence):
        """Modify the account if this inovice is for a notice/aviz stock movement that hapend before.
           Is setting account 418 that must be used if the goods where sent before the invoice
           Account 418 must be != recivable        if not it can not be put into invoice and also the base is wrong at computing taxes
           If location has a property_account_income_location_id we will give this instead of that from product
        """
        res = super()._prepare_invoice_line(sequence=sequence)
        # Overwrite with at least one location with income account defined
        for picking in self.order_id.picking_ids:
            moves = picking.move_line_ids.filtered(lambda m: m.state == "done")
            for move in moves:
                if move.location_id.property_account_income_location_id:
                    res["account_id"] = move.location_id.property_account_income_location_id
                    break

        if self.product_id.invoice_policy == "delivery":
            if any([picking.notice  for picking in self.order_id.picking_ids]):
                res["account_id"] = self.company_id.property_stock_picking_receivable_account_id 
    
        return res
    