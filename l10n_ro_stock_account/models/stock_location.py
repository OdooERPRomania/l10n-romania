# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class stock_location(models.Model):
    _name = "stock.location"
    _inherit = "stock.location"

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


