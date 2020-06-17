# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from forks_addons.odoo.doc._extensions.pyjsparser.parser import false

_logger = logging.getLogger(__name__)

#svl= StockValuationLine

class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    picking_type_code = fields.Selection(related='picking_id.picking_type_code', readonly=True,help="taken from stock_picking that is taken from stock_picking_type.code")

    stock_move_type = fields.Char(help="""
reception
reception_refund # rambursare receptie

reception_notice", "Reception with notice"  # receptie pe baza de aviz
reception_refund_notice", "Reception refund with notice",  # rabursare receptie facuta cu aviz
            
reception_store", "Reception in store"  # receptie in magazin
reception_refund_store", "Reception regund in store"  # rambursare receptie in magazin

            
reception_store_notice", "Reception in store with notice"
reception_refund_store_notice", "Reception refund in store with notice",  # rabursare receptie in magazin facuta cu aviz

delivery", "Delivery"
delivery_refund", "Delivery refund"

delivery_notice", "Delivery with notice"
delivery_refund_notice", "Delivery refund with notice"

delivery_store", "Delivery from store"
delivery_refund_store", "Delivery refund in store"

delivery_store_notice", "Delivery from store with notice"
delivery_refund_store_notice", "Delivery refund in store with notice"

consume", "Consume"
            
inventory_plus", "Inventory plus"
inventory_plus_store", "Inventory plus in store"
inventory_minus", "Inventory minus"
inventory_minus_store", "Inventory minus in store"
            
production", "Reception from production"
            
transfer", "Transfer"
transfer_store", "Transfer in Store"
transfer_in", "Transfer in"
transfer_out", "Transfer out"
            
consume_store", "Consume from Store"
production_store", "Reception in store from production"
""",
        default="")

    def _action_cancel(self):
        for move in self:
            if move.account_move_ids:
                move.account_move_ids.button_cancel()
                move.account_move_ids.unlink()
        return super()._action_cancel()


    def _get_accounting_data_for_valuation(self):
        " Modificare conturi determinate standard"
        self.ensure_one()
        self = self.with_company(self.company_id)
        journal_id, acc_src, acc_dest, acc_valuation = super()._get_accounting_data_for_valuation()

        stock_move_type = self.env.context.get("stock_move_type", self.stock_move_type)

        if stock_move_type == "inventory_plus_store":
            if self.location_dest_id.valuation_in_account_id:
                acc_valuation = self.location_dest_id.valuation_in_account_id
            if self.location_dest_id.property_account_expense_location_id:
                acc_dest = self.location_dest_id.property_account_expense_location_id
                acc_src = acc_dest
        if stock_move_type == "inventory_minus_store":
            if self.location_id.valuation_out_account_id:
                acc_valuation = self.location_id.valuation_out_account_id
            if  self.location_id.property_account_expense_location_id:  
                # 758800 Alte venituri din exploatare
                acc_dest = self.location_id.property_account_expense_location_id
                acc_src = acc_dest

        if "delivery_store" in stock_move_type:  
            # la livrarea din magazin se va folosi contrul specificat in locatie!
            if  self.location_id.valuation_out_account_id:  
                # produsele sunt evaluate dupa contrul de evaluare din locatie
                acc_valuation = self.location_id.valuation_out_account_id

        if "reception" in stock_move_type and "notice" in stock_move_type:
            acc_src = self.company_id.property_stock_picking_payable_account_id
            acc_dest = self.company_id.property_stock_picking_payable_account_id

        if (
            "consume" in stock_move_type
            or "delivery" in stock_move_type
            or "production" in stock_move_type
        ):
            acc_dest = self.product_id.property_account_expense_id
            if not acc_dest:
                acc_dest = self.product_id.categ_id.property_account_expense_categ_id
            if self.location_id.property_account_expense_location_id:
                acc_dest = self.location_id.property_account_expense_location_id
            acc_src = acc_dest

        if "inventory_plus" == stock_move_type:
            # cont stoc la cont de cheltuiala
            acc_dest = self.product_id.property_account_expense_id
            if not acc_dest:
                acc_dest = self.product_id.categ_id.property_account_expense_categ_id
            if self.location_id.property_account_expense_location_id:  
                # 758800 Alte venituri din exploatare
                acc_dest = self.location_id.property_account_expense_location_id
            acc_src = acc_dest

        if "inventory_minus" == stock_move_type:
            # cont de cheltuiala la cont de stoc
            acc_src = self.product_id.property_account_income_id
            if not acc_src:
                acc_src = self.product_id.categ_id.property_account_income_categ_id
            if self.location_dest_id.property_account_income_location_id:  
                # 758800 Alte venituri din exploatare
                acc_src = self.location_dest_id.property_account_income_location_id
            acc_dest = acc_src

        # de regula se fac la pretul de stocare!
        return journal_id, acc_src, acc_dest, acc_valuation


##################### generare note contabile suplimentare pentru micarea de stoc################################################################
##################### generare note contabile suplimentare pentru micarea de stoc################################################################
    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries called from stock_account.stock_move.action_done that is called form stock_picking.button_validate"""
        self.ensure_one()
        # convert from UTC (server timezone) to user timezone
#         use_date = fields.Datetime.context_timestamp(
#             self, timestamp=fields.Datetime.from_string(self.date)
#         )
#         use_date = fields.Date.to_string(use_date)
# 
#         move = self.with_context(force_period_date=use_date, stock_move_type=stock_move_type)
        self = self.with_context(force_period_date=self.date)
        
        if self.product_id.type != 'product':  
            return False   # no stock valuation for consumable products
        if self.restrict_partner_id:
            return False   # if the move isn't owned by the company, we don't make any valuation

        location_from = self.location_id
        location_to = self.location_dest_id

        store = location_from.merchandise_type == "store" or location_to.merchandise_type == "store"
        notice = self.picking_id and self.picking_id.notice
        stock_move_type = "_store" if store else '' + '_notice' if notice else ''
        stock_move_type_initial = stock_move_type

        company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False

        if self.origin_returned_move_id:     ############# is a refund   ############# is a refund  ############# is a refund ############# is a refund 
            print(f"is a returned move of this move {self.origin_returned_move_id}")
            if location_from.usage == "internal" and location_to.usage == "supplier":
                stock_move_type += "_reception_refund"
            elif location_from.usage == "customer" and location_to.usage == "internal":
                stock_move_type += "_delivery_refund"
            # here we just need to call    _reverse_moves(self, default_values_list=None, cancel=False) if exist account moves on orginal stock move:
                
        elif location_from.usage == "supplier":
            if  location_to.usage == "internal":
                stock_move_type +=  "_reception"
                if notice:
                    self.stock_move_type = stock_move_type
#                     on all created stock_moves we must make this and put this stock_move 
#                     _reverse_moves
                    self._create_account_reception_14( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                elif store:
                    self.stock_move_type = stock_move_type
                    self._create_account_reception_14( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                    self._create_account_delivery_from_store(refund="refund" in stock_move_type, qty=qty ,description=description, svl_id=svl_id, cost=cost)

                else:
                    _logger.info(f"Nici o nota contabila delivery pt ca e in factura 371+4426 = 401")
                    self.stock_move_type = stock_move_type
                    return # we are not doing accounting entry because those done in invoice are sufficient
                
        
        elif location_from.usage == "internal":
            if location_to.usage == "customer":
                stock_move_type += "_delivery"   ##############  delivery   ##############  delivery
            
                if notice:  
                    # livrare pe baza de aviz de facut nota contabila 418 = 70x
                    _logger.info(f"Nota contabila livrare cu aviz stock_move_type={stock_move_type}")
                    self._create_account_delivery_14( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                elif "store" in stock_move_type:
                    _logger.info(f"Nota contabila livrare din magazin stock_move_type={stock_move_type}")
                    self._create_account_delivery_from_store(refund="refund" in stock_move_type, qty=qty ,description=description, svl_id=svl_id, cost=cost)
                else:
                    self.stock_move_type = stock_move_type
                    _logger.info(f"Nici o nota contabila delivery pt ca e in factura 371+4426 = 401")
                    return
#                     self._valid_only_if_dif_credit_debit_account
#                     self._create_account_delivery_14( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                
            elif location_to.usage == "production":
                stock_move_type += "_consume"
            elif location_to.usage == "inventory":
                stock_move_type += "inventory_minus"
            elif location_to.usage == "internal":
                stock_move_type += "_transfer"
                
            elif location_to.usage == "transit":
                if ( self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id ):
                    stock_move_type += "_delivery"      ##############  delivery  
                else:
                    stock_move_type += "_transit_out"

        elif location_from.usage == "inventory":
            if location_to.usage == "internal":
                stock_move_type += "_inventory_plus"
                
        elif location_from.usage == "production":
            if  location_to.usage == "internal":
                 stock_move_type += "_production"
          
        elif location_from.usage == "transit":
            if location_to.usage == "internal":
                if self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id:
                    stock_move_type += "_reception"
                else:
                    stock_move_type += "_transit_in"
        
        if stock_move_type == stock_move_type_initial:
            raise UserError(f"Something is wrong at creating stock_move account entries.\nUnknown operation for location_from={location_from.complete_name} location_to={location_to.complete_name};\nlocation_from.usage={location_from.usage} location_to.usage={location_to.usage} ")
        self.stock_move_type = stock_move_type
        return





            
        if "transfer" in stock_move_type:
            # iesire  marfa din stoc
            _logger.info("Nota contabila transfer de stoc ")
            transfer_move = move.with_context( stock_location_id=move.location_id.id, stock_location_dest_id=move.location_dest_id.id)
            transfer_move._create_account_stock_to_stock( refund=False, permit_same_account=True, qty=qty, description=description, svl_id=svl_id, cost=cost)
            #     # intrare marfa in stoc
            #     _logger.info("Nota contabila intrare stoc in vederea transferului ")
            #     move.with_context(stock_location_id=move.location_dest_id.id)._create_account_stock_to_stock(refund=True, permit_same_account=False)

        elif "transit" in stock_move_type:
            if "transit_out" in stock_move_type:
                _logger.info("Nota contabila iesire stoc in tranzit ")
                move._create_account_stock_to_stock(refund=True, permit_same_account=True, stock_transfer_account=move.company_id.property_stock_transfer_account_id, qty=qty, description=description, svl_id=svl_id, cost=cost)
            elif "transit_in" in stock_move_type:
                _logger.info("Nota contabila intrare stoc in tranzit ")
                move._create_account_stock_to_stock(refund=False, permit_same_account=True, stock_transfer_account=move.company_id.property_stock_transfer_account_id, qty=qty, description=description, svl_id=svl_id, cost=cost)

        elif  "store" in stock_move_type:
            if ("reception" in stock_move_type or "transfer" in stock_move_type or "transit_in" in stock_move_type) and "store" in stock_move_type:
                _logger.info("Nota contabila receptie in magazin")
                move.with_context(  stock_location_id=move.location_dest_id.id )._create_account_reception_in_store(refund="refund" in stock_move_type, qty=qty, description=description, svl_id=svl_id, cost=cost)

            elif stock_move_type == "inventory_plus_store":
                _logger.info("Nota contabila plus de inventar in magazin")
                move.with_context( stock_location_id=move.location_dest_id.id)._create_account_inventory_plus_in_store(description=description, svl_id=svl_id, cost=cost)
            elif stock_move_type == "inventory_minus_store":
                _logger.info("Nota contabila minus de inventar in magazin")
                move.with_context( stock_location_id=move.location_id.id)._create_account_inventory_minus_in_store(description=description, svl_id=svl_id, cost=cost)

    def _create_account_stock_to_stock(self, refund, stock_transfer_account, permit_same_account, qty ,description, svl_id, cost):
#    def _create_account_stock_to_stock(self, refund, stock_transfer_account=None, permit_same_account=True,description, svl_id, cost):
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        forced_quantity = self.product_qty if not refund else -1 * self.product_qty
        move = self.with_context( forced_quantity=forced_quantity, permit_same_account=permit_same_account)

        if refund:
            # if acc_valuation == acc_dest :
            if stock_transfer_account:
                acc_dest = stock_transfer_account
            # aml = move._create_account_move_line(acc_src, acc_dest, journal_id)
            aml = move._create_account_move_line(acc_dest, acc_valuation, journal_id, qty=forced_quantity, description=description, svl_id=svl_id, cost=cost)
        else:
            # if acc_valuation == acc_dest:
            if stock_transfer_account:
                acc_dest = stock_transfer_account
            aml = move._create_account_move_line(acc_valuation, acc_dest, journal_id, qty=forced_quantity, description=description, svl_id=svl_id, cost=cost)
        return aml

    def _create_account_inventory_plus_in_store(self, qty, description, svl_id, cost):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store(refund=False,qty=qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_inventory_minus_in_store(self,qty, description, svl_id, cost):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store(refund=True, qty=qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_delivery_14(self, qty ,description, svl_id, cost):
        """  # Create account moves for deliveries with notice (e.g. 418 = 707)"""
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_src = self.company_id.property_stock_picking_receivable_account_id.id
        acc_dest = accounts_data['stock_valuation'].id
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines
        self._create_account_move_line(acc_src, acc_dest, journal_id,qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_reception_14(self, qty ,description, svl_id, cost):
        "Primirea marfurilor pe baza de aviz de insotire: ex 371 = 408    "
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data['stock_valuation'].id  
        acc_src = self.company_id.property_stock_picking_payable_account_id.id
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id

        # is creating a account_move type entry and  corresponding account_move_lines
        self._create_account_move_line(acc_src, acc_dest, journal_id,qty, description=description, svl_id=svl_id, cost=cost)


    def _create_account_reception_in_store(self, refund, qty, description, svl_id, cost):
#    def _create_account_reception_in_store(self, refund=False,description, svl_id, cost):
        """
        Receptions in location with inventory kept at list price
        Create account move with the price difference one (3x8) to suit move: 3xx = 3x8
        Create account move with the uneligible vat one (442810) to suit move: 3xx = 442810
        """
        move = self
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        accounts_data = move.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data.get("stock_valuation", False)

        if self.location_dest_id.valuation_in_account_id:
            acc_dest = self.location_dest_id.valuation_in_account_id.id
        else:
            if self.location_id.valuation_out_account_id:
                acc_dest = self.location_id.valuation_out_account_id.id
            else:
                acc_dest = accounts_data["stock_input"]

        journal_id = accounts_data["stock_journal"].id

        acc_src = move.product_id.property_account_creditor_price_difference
        if not acc_src:
            acc_src =  move.product_id.categ_id.property_account_creditor_price_difference_categ 
        if move.location_dest_id.property_account_creditor_price_difference_location_id:
            acc_src =  move.location_dest_id.property_account_creditor_price_difference_location_id 
        if not acc_src:
            raise UserError(
                _(
                    "Configuration error. Please configure the price difference account on the product or its category to process this operation."
                )
            )
        qty = move.product_qty
        cost_price = (
            move.product_id.cost_method == "fifo"
            and move.value / qty
            or move.product_id.standard_price
        )
        cost_price = abs(cost_price)
        taxes_ids = move.product_id.taxes_id.filtered(
            lambda r: r.company_id == move.company_id
        )

        list_price = move.product_id.list_price or 0.00
        if taxes_ids:
            taxes = taxes_ids.compute_all(list_price, product=move.product_id)
            list_price = taxes["total_excluded"]

        if list_price <= cost_price and list_price != 0.0:
            raise UserError(
                _(
                    "You cannot move a product if price list is lower than cost price. Please update list price to suit to be higher than %s"
                    % cost_price
                )
            )

        # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
        # the company currency... so we need to use round() before  creating the accounting entries.
        stock_value = move.company_id.currency_id.round(cost_price * abs(qty))
        valuation_amount = list_price * abs(qty) - stock_value
        uneligible_tax = 0

        if taxes_ids:
            # tva la valoarea de vanzare
            taxes = taxes_ids.compute_all(
                move.product_id.list_price, product=move.product_id, quantity=abs(qty)
            )
            round_diff = taxes["total_excluded"] - valuation_amount - stock_value
            uneligible_tax = ( taxes["total_included"] - taxes["total_excluded"] + round_diff)

        move = move.with_context(
            force_valuation_amount=valuation_amount, forced_quantity=0.0
        )
        if refund:
            acc_src, acc_dest = acc_dest, acc_src

        move._create_account_move_line(acc_src, acc_dest, journal_id,xx)

        if uneligible_tax:
            if not move.company_id.tax_cash_basis_journal_id.default_debit_account_id:
                # raise UserError(_('Please set account for uneligible tax '))
                _logger.info(_("Please set account for uneligible tax "))
            if not refund:
                acc_src =  move.company_id.tax_cash_basis_journal_id.default_debit_account_id
            else:
                acc_dest = move.company_id.tax_cash_basis_journal_id.default_debit_account_id 

            move = move.with_context( force_valuation_amount=uneligible_tax, forced_quantity=0.0)
            if acc_src and acc_dest:
                move._create_account_move_line(acc_src, acc_dest, journal_id,qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_delivery_from_store(self, refund, qty, description, svl_id, cost):
        self._create_account_reception_in_store(not refund, qty=qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_delivery_notice(self, refund, qty, description, svl_id, cost):
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        journal_id = accounts_data["stock_journal"].id

        acc_src = ( 
            self.product_id.property_account_income_id
            or self.product_id.categ_id.property_account_income_categ_id
        ) #????
        # not beeter:
        #acc_src = accounts_data['income']
        if self.location_id.property_account_income_location_id:
            acc_src = self.location_id.property_account_income_location_id
        acc_dest = self.company_id.property_stock_picking_receivable_account_id
        if not acc_dest:
            return

        if refund:
            acc_src, acc_dest = acc_dest, acc_src


#???????????????? here when we are making the aviz are we giving the price?
#        valuation_amount = self.price_unit * self.product_uom_qty #self.value
#   here what price do I need to put? maybe from product?
# if we are not giving the price than the price must be that from stock 
# not used anymore ? the valuation_amount?
        valuation_amount = self.product_id._prepare_out_svl_vals(quantity=self.product_uom_qty, company=self.company_id)['value']
        if self.sale_line_id:
            sale_line = self.sale_line_id
            price_invoice = sale_line.price_subtotal / sale_line.product_uom_qty
            valuation_amount = price_invoice * abs(self.product_qty)
            valuation_amount = sale_line.order_id.currency_id.compute(
                valuation_amount, self.company_id.currency_id
            )

        self.with_context(force_valuation_amount=valuation_amount)._create_account_move_line(acc_src, acc_dest, journal_id, qty, description=description, svl_id=svl_id, cost=cost)

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        self.ensure_one()
        res = super()._prepare_account_move_line(  qty, cost, credit_account_id, debit_account_id, description)

        if "refund" in self.stock_move_type:
            if (self.env["ir.module.module"].sudo().search([("name", "=", "account_storno"), ("state", "=", "installed")])):
                if ( self.product_id.categ_id.property_stock_journal.posting_policy == "storno" ):
                    for acl in res:
                        acl[2]["credit"], acl[2]["debit"] = -acl[2]["debit"],-acl[2]["credit"]

        if not res:
            return res
        # stock_move_type = self.env.context.get('stock_move_type', self.get_stock_move_type())
        stock_move_type = self.env.context.get("stock_move_type", self.stock_move_type)

        location_id = self.env.context.get("stock_location_id", False)
        location_dest_id = self.env.context.get("stock_location_dest_id", False)
        if not location_id and self.location_dest_id.usage == "internal":
            location_id = self.location_dest_id.id
        if not location_id and self.location_id.usage == "internal":
            location_id = self.location_id.id

        for acl in res:
            acl[2]["move_id"] = self.id
#             if location_id and not location_dest_id:
#                 acl[2]["stock_location_id"] = location_id
#             if location_id and location_dest_id:
#                 if acl[2]["credit"] != 0:
#                     acl[2]["stock_location_id"] = location_id
#                 else:
#                     acl[2]["stock_location_dest_id"] = location_dest_id
            # else:
            #     if self.location_id.usage == 'internal' and  self.location_dest_id.usage != 'internal':
            #         acl[2]['stock_location_id'] = self.location_id.id
            #     elif self.location_id.usage != 'internal' and self.location_dest_id.usage == 'internal':
            #         acl[2]['stock_location_id'] = self.location_dest_id.id
            # acl[2]['stock_location_id'] = self.location_id.id
            # acl[2]['stock_location_dest_id'] = self.location_dest_id.id

#20200610 stock_picking_id does not exist in account_move_line . 
#             if self.picking_id:
#                 acl[2]["stock_picking_id"] = self.picking_id.id
            if self.inventory_id:
                acl[2]["stock_inventory_id"] = self.inventory_id.id
            if "store" in stock_move_type and acl[2]["quantity"] == 0:
                acl[2]["ref"] = self.reference
        return res


# to do it at the end of normal tranfers
#     def _is_dropshipped(self):
#         stock_move_type = self.stock_move_type
#         if not stock_move_type:
#             stock_move_type = self.get_stock_move_type()
#         if stock_move_type and ("transfer" in stock_move_type or "transit" in stock_move_type):
#             return True
#         return super()._is_dropshipped()

    def correction_valuation(self):
        for move in self:
            move.product_price_update_before_done()
            move._run_valuation()
            move._account_entry_move()


    def _valid_only_if_dif_credit_debit_account( self, credit_account_id, debit_account_id, ):
        "raise error if debit and credit account are equal (must be called from transfers that are not internal)"
        if credit_account_id == debit_account_id :
            raise UserError("For this transfer, creidt_account_id=debit_account_id={debit_account_id.code} {debit_account_id.name}.\n Because is not a internal transfer something must be wrong configurated")
        