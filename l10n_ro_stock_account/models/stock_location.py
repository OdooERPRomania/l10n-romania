# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------
# Stock Location
# ----------------------------------------------------------


class stock_location(models.Model):
    _name = "stock.location"
    _inherit = "stock.location"

# field property_stock_account_input_location_id  is  valuation_in_account_id  defined in stock_account 
#     valuation_in_account_id = fields.Many2one(
#         'account.account', 'Stock Valuation Account (Incoming)',
#         domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)],
#         help="Used for real-time inventory valuation. When set on a virtual location (non internal type), "
#              "this account will be used to hold the value of products being moved from an internal location "
#              "into this location, instead of the generic Stock Output Account set on the product. "
#              "This has no effect for internal locations.")
#                                                            string='Stock Input Account',
#                                                            help="When doing real-time inventory valuation, counterpart journal items for all incoming stock moves will be posted in this account, unless "
#                                                                 "there is a specific valuation account set on the source location. When not set on the product, the one from the product category is used.",
# filed property_stock_account_output_location_id is  valuation_out_account_id
#         help="Used for real-time inventory valuation. When set on a virtual location (non internal type), "
#              "this account will be used to hold the value of products being moved out of this location "
#              "and into an internal location, instead of the generic Stock Output Account set on the product. "
#              "This has no effect for internal locations.")
#                                                             string='Stock Output Account',
#                                                             help="When doing real-time inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account, unless "
#                                                                  "there is a specific valuation account set on the destination location. When not set on the product, the one from the product category is used.",
    property_account_creditor_price_difference_location_id = fields.Many2one(
        "account.account",
        string="Price Difference Account",
        help="This account will be used to value price difference between purchase price and cost price.",
    )
    property_account_income_location_id = fields.Many2one(
        "account.account",
        string="Income Account",
        help="This account will be used to value outgoing stock using sale price.",
    )
    property_account_expense_location_id = fields.Many2one(
        "account.account",
        string="Expense Account",
        help="This account will be used to value outgoing stock using cost price.",
    )


