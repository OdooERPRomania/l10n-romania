# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_is_zero, float_compare


class AccountMove(models.Model):
    _inherit = "account.move"


    def _stock_account_prepare_anglo_saxon_in_lines_vals(self):
        ''' ORIGINAL FROM PURCHASE_STOCK (is adding lines at purchase) that is overridden of stock_account _stock_account_prepare_anglo_saxon_in_lines_vals (that is adding accounting lines at sale)
            
        Prepare values used to create the journal items (account.move.line) corresponding to the price difference
         lines for vendor bills.

        Example:

        Buy a product having a cost of 9 and a supplier price of 10 and being a storable product and having a perpetual
        valuation in FIFO. The vendor bill's journal entries looks like:

        Account                                     | Debit | Credit
        ---------------------------------------------------------------
        101120 Stock Interim Account (Received)     | 10.0  |
        ---------------------------------------------------------------
        101100 Account Payable                      |       | 10.0
        ---------------------------------------------------------------

        This method computes values used to make two additional journal items:

        ---------------------------------------------------------------
        101120 Stock Interim Account (Received)     |       | 1.0
        ---------------------------------------------------------------
        xxxxxx Price Difference Account             | 1.0   |
        ---------------------------------------------------------------

        :return: A list of Python dictionary to be passed to env['account.move.line'].create.
        '''
        lines_vals_list = []

        for move in self:
#orig            if move.move_type not in ('in_invoice', 'in_refund', 'in_receipt') or not move.company_id.anglo_saxon_accounting:
            if move.move_type not in ('in_invoice', 'in_refund', 'in_receipt') or\
               not move.company_id.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1]\
               or move.company_id.anglo_saxon_accounting :  # if this is the case, use the original purchase_stock function \  
                continue

            move = move.with_company(move.company_id)
            for line in move.invoice_line_ids.filtered(lambda line: line.product_id.type == 'product' and line.product_id.valuation == 'real_time'):

                # Filter out lines being not eligible for price difference.
                if line.product_id.type != 'product' or line.product_id.valuation != 'real_time':
                    continue

                # Retrieve accounts needed to generate the price difference.
                # default must be 348000 Diferenţe de preţ la produse
                debit_pdiff_account = line.product_id.property_account_creditor_price_difference \
                                or line.product_id.categ_id.property_account_creditor_price_difference_categ
                if not debit_pdiff_account:
                    raise UserError(f'For product {line.product_id.name} does not exist property_account_creditor_price_difference')
                
                debit_pdiff_account = move.fiscal_position_id.map_account(debit_pdiff_account)

                if line.product_id.cost_method != 'standard' and line.purchase_line_id:
                    po_currency = line.purchase_line_id.currency_id
                    po_company = line.purchase_line_id.company_id

                    # Retrieve stock valuation moves.
                    valuation_stock_moves = self.env['stock.move'].search([
                        ('purchase_line_id', '=', line.purchase_line_id.id),
                        ('state', '=', 'done'),
                        ('product_qty', '!=', 0.0),
                    ])
                    if move.move_type == 'in_refund':
                        valuation_stock_moves = valuation_stock_moves.filtered(lambda stock_move: stock_move._is_out())
                    else:
                        valuation_stock_moves = valuation_stock_moves.filtered(lambda stock_move: stock_move._is_in())

                    if valuation_stock_moves:
                        valuation_price_unit_total = 0
                        valuation_total_qty = 0
                        for val_stock_move in valuation_stock_moves:
                            # In case val_stock_move is a return move, its valuation entries have been made with the
                            # currency rate corresponding to the original stock move
                            valuation_date = val_stock_move.origin_returned_move_id.date or val_stock_move.date
                            svl = val_stock_move.mapped('stock_valuation_layer_ids').filtered(lambda l: l.quantity)
                            layers_qty = sum(svl.mapped('quantity'))
                            layers_values = sum(svl.mapped('value'))
                            valuation_price_unit_total += line.company_currency_id._convert(
                                layers_values, move.currency_id,
                                move.company_id, valuation_date, round=False,
                            )
                            valuation_total_qty += layers_qty
                        valuation_price_unit = valuation_price_unit_total / valuation_total_qty
                        valuation_price_unit = line.product_id.uom_id._compute_price(valuation_price_unit, line.product_uom_id)

                    elif line.product_id.cost_method == 'fifo':
                        # In this condition, we have a real price-valuated product which has not yet been received
                        valuation_price_unit = po_currency._convert(
                            line.purchase_line_id.price_unit, move.currency_id,
                            po_company, move.date, round=False,
                        )
                    else:
                        # For average/fifo/lifo costing method, fetch real cost price from incoming moves.
                        price_unit = line.purchase_line_id.product_uom._compute_price(line.purchase_line_id.price_unit, line.product_uom_id)
                        valuation_price_unit = po_currency._convert(
                            price_unit, move.currency_id,
                            po_company, move.date, round=False
                        )

                else:
                    # Valuation_price unit is always expressed in invoice currency, so that it can always be computed with the good rate
                    price_unit = line.product_id.uom_id._compute_price(line.product_id.standard_price, line.product_uom_id)
                    valuation_price_unit = line.company_currency_id._convert(
                        price_unit, move.currency_id,
                        move.company_id, fields.Date.today(), round=False
                    )

                invoice_cur_prec = move.currency_id.decimal_places

                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                if line.tax_ids:
                    price_unit = line.tax_ids.compute_all(
                        price_unit, currency=move.currency_id, quantity=1.0, is_refund=move.move_type == 'in_refund')['total_excluded']

                if float_compare(valuation_price_unit, price_unit, precision_digits=invoice_cur_prec) != 0 \
                        and float_compare(line['price_unit'], line.price_unit, precision_digits=invoice_cur_prec) == 0:

                    price_unit_val_dif = price_unit - valuation_price_unit

                    if move.currency_id.compare_amounts(price_unit, valuation_price_unit) != 0 and debit_pdiff_account:
                        # Add price difference account line.
                        vals = {
                            'name': line.name[:64],
                            'move_id': move.id,
                            'currency_id': line.currency_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom_id.id,
                            'quantity': line.quantity,
                            'price_unit': price_unit_val_dif,
                            'price_subtotal': line.quantity * price_unit_val_dif,
                            'account_id': debit_pdiff_account.id,
                            'analytic_account_id': line.analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                            'exclude_from_invoice_tab': True,
                            'is_anglo_saxon_line': True,
                        }
                        vals.update(line._get_fields_onchange_subtotal(price_subtotal=vals['price_subtotal']))
                        lines_vals_list.append(vals)

                        # Correct the amount of the current line.
                        vals = {
                            'name': line.name[:64],
                            'move_id': move.id,
                            'currency_id': line.currency_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom_id.id,
                            'quantity': line.quantity,
                            'price_unit': -price_unit_val_dif,
                            'price_subtotal': line.quantity * -price_unit_val_dif,
                            'account_id': line.account_id.id,
                            'analytic_account_id': line.analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                            'exclude_from_invoice_tab': True,
                            'is_anglo_saxon_line': True,
                        }
                        vals.update(line._get_fields_onchange_subtotal(price_subtotal=vals['price_subtotal']))
                        lines_vals_list.append(vals)
        return lines_vals_list


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


#    is_price_diffrence = fields.Boolean(help="When posting a invoice, tells if this line represent differences of price/quantity with the reception if exist will delete them, and recreate if necessary")
# we are going to use  field is_anglo_saxon_line that exist and we do not need to unlink them ...


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
