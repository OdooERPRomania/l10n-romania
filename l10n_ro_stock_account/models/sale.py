# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    """modify the account if this inovice is for a notice/aviz stock movement that hapend before
       is setting account 418 that must be used if the goods where sent before the invoice
    """

    _inherit = "sale.order.line"

    def _prepare_invoice_line(self,sequence):
        res = super()._prepare_invoice_line(sequence=sequence)
        if self.product_id.invoice_policy == "delivery":
            notice = False
            for picking in self.order_id.picking_ids:
                if picking.notice:
                    notice = True
            if notice:
                res["account_id"] = self.company_id.property_stock_picking_receivable_account_id #or res["account_id"]

        return res
