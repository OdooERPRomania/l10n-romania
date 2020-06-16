# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_is_zero, float_compare


class AccountMove(models.Model):
    _inherit = "account.move"

    def post(self):
        """at post add account_move_lines with the goods price difference if can be the case"""
        if self._context.get("move_reverse_cancel"):
            return super().post()
        # Create additional price difference lines for vendor bills.
        for record in self:
            if record.move_type in ["in_invoice", "in_refund"]:

                # cineva a zis: chiar daca nu este sistem anglo saxon diferentele de pret dintre receptie si factura trebuie inregistrate
                #if not self.env.user.company_id.anglo_saxon_accounting:
                # the logical condition is to compute the price difference if this company has romanian chart_template_id
                if record.company_id.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1]:
                    invoice_stock_price_difference_move_lines = record._invoice_line_move_line_get_diff()
                    record.line_ids = invoice_stock_price_difference_move_lines
        return super().post()

    @api.model
    def _invoice_line_move_line_get_diff(self):
        # se adaga linii contabile de diferente pret
        self.ensure_one()
        res = []

        account_id = self.company_id.property_stock_picking_payable_account_id
        get_param = self.env["ir.config_parameter"].sudo().get_param
        # chiar daca nu este sistem anglo saxon diferentele de pret dintre receptie si factura trebuie inregistrate
        invoice=self
        diff_limit = float(get_param("stock_account.diff_limit", "2.0"))

        add_diff_from_config = eval(  get_param("stock_account.add_diff", "False"))

        for i_line in invoice.invoice_line_ids:
            if i_line.display_type in ['line_section', 'line_note']:
                continue
            if i_line.is_price_diffrence:  
                res+= [(2,i_line.id,0)]             #delete the previous line differences not to have them multiple times
                continue
            if i_line.product_id.cost_method == "standard":
                add_diff = True  # daca pretul este standard se inregistreaza diferentele de pret.
            else:
                add_diff = add_diff_from_config

            # daca linia a fost receptionata  de pe baza de aviz se seteaza contul 408 pe nota contabile
            if account_id and i_line.account_id == account_id:
                i_line = i_line.with_context(fix_stock_input=account_id)
                add_diff = True  # trbuie sa adaug diferenta dintre recpetia pe baza de aviz si receptia din factura

# !!!!!!!!!!!!!!! de verificat here is computing the diffrence between price/quantity reception and invoice
            price_diff_account = i_line.product_id.property_account_creditor_price_difference
            if not price_diff_account:
                price_diff_account = i_line.product_id.categ_id.property_account_creditor_price_difference_categ
            if not price_diff_account:
                raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.')+f"product.name ={i_line.product_id.name}")
            diff_line = []
            received_qty = i_line.purchase_line_id.qty_received
            received_move = self.env['stock.move'].search([('purchase_line_id','=',i_line.purchase_line_id.id),('product_id','=',i_line.product_id.id),('company_id','=',i_line.company_id.id)])
            received_price = received_move.price_unit
            
            line_diff_value = received_qty * received_price - i_line.quantity * i_line.price_unit
#!!!!!!!!!!!!!!! de verificat ...

            if not float_is_zero(line_diff_value,2):
                name = f" Price difference={line_diff_value};received_qty={received_qty};received_price={received_price}"
                res +=  [(0, 0, {
                        'move_id':invoice.id,
                        'name': name,
                        'account_id': price_diff_account.id,  # must be verified
                        'debit': abs(line_diff_value),  # must be verified
                        'credit': 0,
                        "is_price_diffrence":True, 
                        'product_id': i_line.product_id.id,  #maybe mot ?
                    }), (0, 0, {
                        'move_id':invoice.id,
                        'name': name,
                        'account_id': i_line.account_id.id,
                        'debit': 0,
                        'credit': abs(line_diff_value),
                        "is_price_diffrence":True,
                        'product_id': i_line.product_id.id,  # maybe mot ?
                        })  ]

                if line_diff_value > diff_limit:
                        raise UserError(  "The price difference for the product %s exceeds the %d limit " % (i_line.product_id.name, diff_limit))

        return res



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_price_diffrence = fields.Boolean(help="When posting a invoice, tells if this line represent differences of price/quantity with the reception if exist will delete them, and recreate if necessary")

#    !!!!!!!!!  maybe is_price_difference must be is_anglo_saxon_line  ?????????????
# and the function at create must be  ???????????
#_stock_account_prepare_anglo_saxon_out_lines_vals
# to verify


    stock_inventory_id = fields.Many2one(
        "stock.inventory",
        string="Stock Inventory",
        help="This account move line has been generated by this inventory",
    )

#     def _get_computed_account(self):
#         self.ensure_one()
#         if self.product_id.type == "product" and self.move_id.is_purchase_document():
#             fiscal_position = self.move_id.fiscal_position_id
#             accounts = self.product_id.product_tmpl_id.get_product_accounts(
#                 fiscal_pos=fiscal_position
#             )
#             if accounts["stock_input"]:
#                 return accounts["stock_input"]
#         return super()._get_computed_account()


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
