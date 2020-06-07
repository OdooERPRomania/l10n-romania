# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    picking_type_code = fields.Selection(related='picking_id.picking_type_code', readonly=True,help="taken from stock_picking that is taken from stock_picking_type.code")



# I think that this filed is only used to know what accounts is going to take.
# we are going to do a dictionary with source and destination location and based on this is going to tell what accounts to take        
    move_type = fields.Selection(
        [
            ("reception", "Reception"),
            ("reception_notice", "Reception with notice"),  # receptie pe baza de aviz
            ("reception_store", "Reception in store"),  # receptie in magazin
            ("reception_refund", "Reception refund"),  # rambursare receptie
            (
                "reception_refund_notice",
                "Reception refund with notice",
            ),  # rabursare receptie facuta cu aviz
            (
                "reception_refund_store_notice",
                "Reception refund in store with notice",
            ),  # rabursare receptie in magazin facuta cu aviz
            ("reception_store_notice", "Reception in store with notice"),
            ("delivery", "Delivery"),
            ("delivery_notice", "Delivery with notice"),
            ("delivery_store", "Delivery from store"),
            ("delivery_store_notice", "Delivery from store with notice"),
            ("delivery_refund", "Delivery refund"),
            ("delivery_refund_notice", "Delivery refund with notice"),
            ("delivery_refund_store", "Delivery refund in store"),
            ("delivery_refund_store_notice", "Delivery refund in store with notice"),
            ("consume", "Consume"),
            ("inventory_plus", "Inventory plus"),
            ("inventory_plus_store", "Inventory plus in store"),
            ("inventory_minus", "Inventory minus"),
            ("inventory_minus_store", "Inventory minus in store"),
            ("production", "Reception from production"),
            ("transfer", "Transfer"),
            ("transfer_store", "Transfer in Store"),
            ("transfer_in", "Transfer in"),
            ("transfer_out", "Transfer out"),
            ("consume_store", "Consume from Store"),
            ("production_store", "Reception in store from production"),
        ],
        compute="_compute_move_type",
    )

    # DE VAZUT DACA MAI TREBUIE - daca notele se fac cu picking_id.date
    @api.onchange("date")
    def onchange_date(self):
        if self.picking_id:
            self.date_expected = self.picking_id.date
        super(StockMove, self).onchange_date()

    def action_done(self):
        res = super(StockMove, self).action_done()
        for move in self:
            if move.picking_id:
                move.write({"date": move.picking_id.date})
        return res

    def action_cancel(self):
        for move in self:
            if move.account_move_ids:
                move.account_move_ids.button_cancel()
                move.account_move_ids.unlink()
        return super(StockMove, self).action_cancel()

    # def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
    # Nu are rost sa facem note pe aceleasi conturi
    def _create_account_move_line(
        self,
        credit_account_id,
        debit_account_id,
        journal_id,
        qty,
        description,
        svl_id,
        cost,
    ):
        if credit_account_id and not isinstance(credit_account_id, int):
            credit_account_id = credit_account_id.id

        if debit_account_id and not isinstance(debit_account_id, int):
            debit_account_id = debit_account_id.id

        debit = self.env["account.account"].browse(debit_account_id)
        credit = self.env["account.account"].browse(credit_account_id)
        _logger.info("NC: {}  = {}   ".format(debit.display_name, credit.display_name))

        permit_same_account = self.env.context.get("permit_same_account", False)
        if credit_account_id != debit_account_id or permit_same_account:
            super(StockMove, self)._create_account_move_line(
                credit_account_id,
                debit_account_id,
                journal_id,
                qty,
                description,
                svl_id,
                cost,
            )

    # DE VAZUT TOATE CUM LE PUTEM SIMPLIFICA SI SA FIE MAI INTELIGIBILE
    @api.depends("location_id", "location_dest_id")
    def _compute_move_type(self):
        for move in self:
            move.move_type = move.get_move_type()

    def get_move_type(self):

        move = self

        location_from = self.location_id
        location_to = self.location_dest_id
        notice = move.picking_id and move.picking_id.notice

        if notice:
            if (
                location_from.usage == "internal" and location_to.usage == "supplier"
            ) or (
                location_from.usage == "supplier" and location_to.usage == "internal"
            ):
                notice = move.product_id.purchase_method == "receive"

            if (
                location_from.usage == "internal" and location_to.usage == "customer"
            ) or (
                location_from.usage == "customer" and location_to.usage == "internal"
            ):
                if move.product_id.invoice_policy != "delivery":
                    notice = False
                    _logger.warning(
                        "Pentru produsul %s nu se poate utiliza livrare pe baza de aviz  "
                        % move.product_id.display_name
                    )

        move_type = ""
        if location_from.usage == "supplier" and location_to.usage == "internal":
            move_type = "reception"
        elif location_from.usage == "internal" and location_to.usage == "supplier":
            move_type = "reception_refund"
        elif location_from.usage == "internal" and location_to.usage == "customer":
            move_type = "delivery"
        elif location_from.usage == "customer" and location_to.usage == "internal":
            move_type = "delivery_refund"
        elif location_from.usage == "internal" and location_to.usage == "production":
            move_type = "consume"
        elif location_from.usage == "inventory" and location_to.usage == "internal":
            move_type = "inventory_plus"
        elif location_from.usage == "internal" and location_to.usage == "inventory":
            move_type = "inventory_minus"
        elif location_from.usage == "production" and location_to.usage == "internal":
            move_type = "production"
        elif location_from.usage == "internal" and location_to.usage == "internal":
            move_type = "transfer"
        elif location_from.usage == "internal" and location_to.usage == "transit":
            if (
                move.picking_id.partner_id.commercial_partner_id
                != move.company_id.partner_id
            ):
                move_type = "delivery"
            else:
                move_type = "transit_out"
        elif location_from.usage == "transit" and location_to.usage == "internal":
            if (
                move.picking_id.partner_id.commercial_partner_id
                != move.company_id.partner_id
            ):
                move_type = "reception"
            else:
                move_type = "transit_in"

        if (
            location_from.merchandise_type == "store"
            or location_to.merchandise_type == "store"
        ):
            move_type += "_store"
        if notice:
            move_type += "_notice"

        return move_type

    # Modificare conturi determinate standard

    def _get_accounting_data_for_valuation(self):
        journal_id, acc_src, acc_dest, acc_valuation = super(
            StockMove, self
        )._get_accounting_data_for_valuation()

        self.ensure_one()
        move = self

        # move_type = self.env.context.get('move_type', move.get_move_type())
        move_type = self.env.context.get("move_type", move.move_type)

        if move_type == "inventory_plus_store":
            if move.location_dest_id.valuation_in_account_id:
                acc_valuation = move.location_dest_id.valuation_in_account_id
            if move.location_dest_id.property_account_expense_location_id:
                acc_dest = move.location_dest_id.property_account_expense_location_id
                acc_src = acc_dest
        if move_type == "inventory_minus_store":
            if move.location_id.valuation_out_account_id:
                acc_valuation = move.location_id.valuation_out_account_id
            if (
                move.location_id.property_account_expense_location_id
            ):  # 758800 Alte venituri din exploatare
                acc_dest = move.location_id.property_account_expense_location_id
                acc_src = acc_dest

        if (
            "delivery_store" in move_type
        ):  # la livrarea din magazin se va folosi contrul specificat in locatie!
            if (
                move.location_id.valuation_out_account_id
            ):  # produsele sunt evaluate dupa contrul de evaluare din locatie
                acc_valuation = move.location_id.valuation_out_account_id

        if "reception" in move_type and "notice" in move_type:
            acc_src = move.company_id.property_stock_picking_payable_account_id
            acc_dest = move.company_id.property_stock_picking_payable_account_id

        if (
            "consume" in move_type
            or "delivery" in move_type
            or "production" in move_type
        ):
            acc_dest = move.product_id.property_account_expense_id
            if not acc_dest:
                acc_dest = move.product_id.categ_id.property_account_expense_categ_id
            if move.location_id.property_account_expense_location_id:
                acc_dest = move.location_id.property_account_expense_location_id
            acc_src = acc_dest

        if "inventory_plus" == move_type:
            # cont stoc la cont de cheltuiala
            acc_dest = move.product_id.property_account_expense_id
            if not acc_dest:
                acc_dest = move.product_id.categ_id.property_account_expense_categ_id
            if (
                move.location_id.property_account_expense_location_id
            ):  # 758800 Alte venituri din exploatare
                acc_dest = move.location_id.property_account_expense_location_id
            acc_src = acc_dest

        if "inventory_minus" == move_type:
            # cont de cheltuiala la cont de stoc
            acc_src = move.product_id.property_account_income_id
            if not acc_src:
                acc_src = move.product_id.categ_id.property_account_income_categ_id
            if (
                move.location_dest_id.property_account_income_location_id
            ):  # 758800 Alte venituri din exploatare
                acc_src = move.location_dest_id.property_account_income_location_id
            acc_dest = acc_src

        # de regula se fac la pretul de stocare!
        return journal_id, acc_src, acc_dest, acc_valuation

    # generare note contabile suplimentare pentru micarea de stoc
    def _account_entry_move(self, qty, description, svl_id, cost):
        """ Accounting Valuation Entries """
        self.ensure_one()
        # convert from UTC (server timezone) to user timezone
        use_date = fields.Datetime.context_timestamp(
            self, timestamp=fields.Datetime.from_string(self.date)
        )
        use_date = fields.Date.to_string(use_date)

        move_type = self.get_move_type()

        move = self.with_context(force_period_date=use_date, move_type=move_type)

        # nota contabila standard
        # if 'transfer' not in move_type:
        _logger.info("Nota contabila standard")
        super(StockMove, move)._account_entry_move(qty, description, svl_id, cost)

        if "transfer" in move_type:
            # iesire  marfa din stoc
            _logger.info("Nota contabila transfer de stoc ")
            transfer_move = move.with_context(
                stock_location_id=move.location_id.id,
                stock_location_dest_id=move.location_dest_id.id,
            )
            transfer_move._create_account_stock_to_stock(
                refund=False, permit_same_account=True
            )
            #     # intrare marfa in stoc
            #     _logger.info("Nota contabila intrare stoc in vederea transferului ")
            #     move.with_context(stock_location_id=move.location_dest_id.id)._create_account_stock_to_stock(refund=True, permit_same_account=False)

        if "transit_out" in move_type:
            _logger.info("Nota contabila iesire stoc in tranzit ")
            move._create_account_stock_to_stock(
                refund=True,
                stock_transfer_account=move.company_id.property_stock_transfer_account_id,
            )
        if "transit_in" in move_type:
            _logger.info("Nota contabila intrare stoc in tranzit ")
            move._create_account_stock_to_stock(
                refund=False,
                stock_transfer_account=move.company_id.property_stock_transfer_account_id,
            )

        if (
            "delivery" in move_type and "notice" in move_type
        ):  # livrare pe baza de aviz de facut nota contabila 418 = 70x
            _logger.info("Nota contabila livrare cu aviz")
            move._create_account_delivery_notice(refund="refund" in move_type)
        if (
            "reception" in move_type
            or "transfer" in move_type
            or "transit_in" in move_type
        ) and "store" in move_type:
            _logger.info("Nota contabila receptie in magazin")
            move.with_context(
                stock_location_id=move.location_dest_id.id
            )._create_account_reception_in_store(refund="refund" in move_type)
        if "delivery" in move_type and "store" in move_type:
            _logger.info("Nota contabila livrare din magazin ")
            move._create_account_delivery_from_store(refund="refund" in move_type)

        if move_type == "inventory_plus_store":
            _logger.info("Nota contabila plus de inventar in magazin")
            move.with_context(
                stock_location_id=move.location_dest_id.id
            )._create_account_inventory_plus_in_store()
        elif move_type == "inventory_minus_store":
            _logger.info("Nota contabila minus de inventar in magazin")
            move.with_context(
                stock_location_id=move.location_id.id
            )._create_account_inventory_minus_in_store()

    def _create_account_stock_to_stock(
        self, refund, stock_transfer_account=None, permit_same_account=True
    ):
        (
            journal_id,
            acc_src,
            acc_dest,
            acc_valuation,
        ) = self._get_accounting_data_for_valuation()
        forced_quantity = self.product_qty if not refund else -1 * self.product_qty
        move = self.with_context(
            forced_quantity=forced_quantity, permit_same_account=permit_same_account
        )

        if refund:
            # if acc_valuation == acc_dest :
            if stock_transfer_account:
                acc_dest = stock_transfer_account
            # aml = move._create_account_move_line(acc_src, acc_dest, journal_id)
            aml = move._create_account_move_line(acc_dest, acc_valuation, journal_id)
        else:
            # if acc_valuation == acc_dest:
            if stock_transfer_account:
                acc_dest = stock_transfer_account
            aml = move._create_account_move_line(acc_valuation, acc_dest, journal_id)
        return aml

    def _create_account_inventory_plus_in_store(self):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store()

    def _create_account_inventory_minus_in_store(self):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store(refund=True)

    def _create_account_reception_in_store(self, refund=False):
        """
        Receptions in location with inventory kept at list price
        Create account move with the price difference one (3x8) to suit move: 3xx = 3x8
        Create account move with the uneligible vat one (442810) to suit move: 3xx = 442810
        """
        move = self
        # journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
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
            acc_src = (
                move.product_id.categ_id.property_account_creditor_price_difference_categ
            )
        if move.location_dest_id.property_account_creditor_price_difference_location_id:
            acc_src = (
                move.location_dest_id.property_account_creditor_price_difference_location_id
            )
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
            uneligible_tax = (
                taxes["total_included"] - taxes["total_excluded"] + round_diff
            )

        move = move.with_context(
            force_valuation_amount=valuation_amount, forced_quantity=0.0
        )
        if refund:
            acc_src, acc_dest = acc_dest, acc_src

        move._create_account_move_line(acc_src, acc_dest, journal_id)

        if uneligible_tax:
            if not move.company_id.tax_cash_basis_journal_id.default_debit_account_id:
                # raise UserError(_('Please set account for uneligible tax '))
                _logger.info(_("Please set account for uneligible tax "))
            if not refund:
                acc_src = (
                    move.company_id.tax_cash_basis_journal_id.default_debit_account_id
                )
            else:
                acc_dest = (
                    move.company_id.tax_cash_basis_journal_id.default_debit_account_id
                )

            move = move.with_context(
                force_valuation_amount=uneligible_tax, forced_quantity=0.0
            )
            if acc_src and acc_dest:
                move._create_account_move_line(acc_src, acc_dest, journal_id)

    def _create_account_delivery_from_store(self, refund):
        self._create_account_reception_in_store(not refund)

    def _create_account_delivery_notice(self, refund):
        move = self
        accounts_data = move.product_id.product_tmpl_id.get_product_accounts()
        journal_id = accounts_data["stock_journal"].id

        acc_src = (
            move.product_id.property_account_income_id
            or move.product_id.categ_id.property_account_income_categ_id
        )
        if move.location_id.property_account_income_location_id:
            acc_src = move.location_id.property_account_income_location_id
        acc_dest = move.company_id.property_stock_picking_receivable_account_id
        if not acc_dest:
            return

        if refund:
            acc_src, acc_dest = acc_dest, acc_src

        valuation_amount = move.value
        if move.sale_line_id:
            sale_line = move.sale_line_id
            price_invoice = sale_line.price_subtotal / sale_line.product_uom_qty
            valuation_amount = price_invoice * abs(self.product_qty)
            valuation_amount = sale_line.order_id.currency_id.compute(
                valuation_amount, move.company_id.currency_id
            )

        move = move.with_context(force_valuation_amount=valuation_amount)

        move._create_account_move_line(acc_src, acc_dest, journal_id)

    def _prepare_account_move_line(
        self, qty, cost, credit_account_id, debit_account_id, description
    ):
        self.ensure_one()

        move = self
        res = super(StockMove, move)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, description
        )

        if "refund" in self.move_type:
            if (
                self.env["ir.module.module"]
                .sudo()
                .search([("name", "=", "account_storno"), ("state", "=", "installed")])
            ):
                if (
                    move.product_id.categ_id.property_stock_journal.posting_policy
                    == "storno"
                ):
                    for acl in res:
                        acl[2]["credit"], acl[2]["debit"] = (
                            -acl[2]["debit"],
                            -acl[2]["credit"],
                        )

        if not res:
            return res
        # move_type = self.env.context.get('move_type', move.get_move_type())
        move_type = self.env.context.get("move_type", move.move_type)

        location_id = self.env.context.get("stock_location_id", False)
        location_dest_id = self.env.context.get("stock_location_dest_id", False)
        if not location_id and move.location_dest_id.usage == "internal":
            location_id = move.location_dest_id.id
        if not location_id and move.location_id.usage == "internal":
            location_id = move.location_id.id

        for acl in res:
            acl[2]["stock_move_id"] = move.id
            if location_id and not location_dest_id:
                acl[2]["stock_location_id"] = location_id
            if location_id and location_dest_id:
                if acl[2]["credit"] != 0:
                    acl[2]["stock_location_id"] = location_id
                else:
                    acl[2]["stock_location_dest_id"] = location_dest_id
            # else:
            #     if move.location_id.usage == 'internal' and  move.location_dest_id.usage != 'internal':
            #         acl[2]['stock_location_id'] = move.location_id.id
            #     elif move.location_id.usage != 'internal' and move.location_dest_id.usage == 'internal':
            #         acl[2]['stock_location_id'] = move.location_dest_id.id
            # acl[2]['stock_location_id'] = move.location_id.id
            # acl[2]['stock_location_dest_id'] = move.location_dest_id.id
            if move.picking_id:
                acl[2]["stock_picking_id"] = move.picking_id.id
            if move.inventory_id:
                acl[2]["stock_inventory_id"] = move.inventory_id.id
            if "store" in move_type and acl[2]["quantity"] == 0:
                acl[2]["ref"] = move.reference

        return res

    def _is_dropshipped(self):
        move_type = self.move_type
        if not move_type:
            move_type = self.get_move_type()
        if move_type and ("transfer" in move_type or "transit" in move_type):
            return True
        return super(StockMove, self)._is_dropshipped()

    def correction_valuation(self):
        for move in self:
            move.product_price_update_before_done()
            move._run_valuation()
            move._account_entry_move()


