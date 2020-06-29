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
# mvoed in ro_stock because is used also in stock_picking_report
#     notice = fields.Boolean(
#         "Is a notice",
#         states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
#         default=False,
#         help = "Prin acest camp se indica daca un produs care e stocabil trece prin contul 408 / 418 la achizitie sau vanzare \nreceptie/ livrare in baza de aviz"
#     )
# just for a view   
    acc_move_line_ids = fields.One2many('account.move.line',  compute='_compute_acc_move_line_ids', string='Generated accounting lines', help="Lines generated by this picking as sum of all stock.moves. Just for view.")

    def _compute_acc_move_line_ids(self):
        "just to show in view"
        for record in self:
            acc_move_ids = self.env['account.move'].search([('stock_move_id','in',record.stock_move_ids.ids)])
            acc_move_line_ids = self.env['account.move.line'].search([('move_id','in',acc_move_ids.ids)])
            record.acc_move_line_ids = [(6,0,acc_move_line_ids.ids)]
