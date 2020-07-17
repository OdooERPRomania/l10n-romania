# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class stock_location(models.Model):
    _inherit = "stock.location"

    property_account_creditor_price_diff_location_id = fields.Many2one(
        "account.account",
        string="Price Difference Account",
        help="This account will be used to value price difference between purchase price and cost price.",
    )
    property_account_income_location_id = fields.Many2one(
        "account.account",
        company_dependent=True,
        string="Income Account",
#         domain="['&', ('deprecated', '=', False),"
#         "('company_id', '=', current_company_id)]",           location has company
        help="This account will overwrite the income accounts from product "
        "or category.",
    )
    property_account_expense_location_id = fields.Many2one(
        "account.account",
        company_dependent=True,
        string="Expense Account",
#         domain="['&', ('deprecated', '=', False),"
#         "('company_id', '=', current_company_id)]",   
        help="This account will overwrite the expense accounts from product "
        "or category.",
    )