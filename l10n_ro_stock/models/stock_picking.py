# ©  2008-201 9Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_compare



class stock_picking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    # prin acest camp se indica daca un produs care e stocabil trece prin contul 408 / 418 la achizitie sau vanzare ( daca exista ro_stock_account instalat)
    # receptie/ livrare in baza de aviz
    notice = fields.Boolean(
        "Is a notice",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        default=False,
        help = "Prin acest camp se indica daca un produs care e stocabil trece prin contul 408 / 418 la achizitie sau vanzare \nreceptie/ livrare in baza de aviz"
    )
