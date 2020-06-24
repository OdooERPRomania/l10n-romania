# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


# all just adds a field in view;  
class StockInventory(models.Model):
    _inherit = "stock.inventory"
    

    acc_move_line_ids = fields.One2many(
        "account.move.line", "stock_inventory_id", string="Generated accounting lines", help = "A field just to be easier to see the generated accounting entries "
    )

    def post_inventory(self):
        "just to have the acc_move_line_ids used in view. can be also without this fields"
        res = super().post_inventory()
        for inv in self:
            acc_move_line_ids = self.env["account.move.line"]
            for move in inv.move_ids:
                for acc_move in move.account_move_ids:
                    acc_move_line_ids |= acc_move.line_ids
            acc_move_line_ids.write({"stock_inventory_id": inv.id})
        return res

 

