# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class ProductCategory(models.Model):
    _inherit = "product.category"

    # TO REMOVE
    def propagate_account(self):
        for categ in self:
            childs = self.search([("id", "child_of", [categ.id])])

            values = {
                # Cont diferență de preț
                "property_account_creditor_price_difference_categ": self.property_account_creditor_price_difference_categ.id,
                # Cont de cheltuieli
                "property_account_expense_categ_id": self.property_account_expense_categ_id.id,
                # Cont de venituri
                "property_account_income_categ_id": self.property_account_income_categ_id.id,
                #  Cont Intrare Stoc
                "property_stock_account_input_categ_id": self.property_stock_account_input_categ_id.id,
                # Cont ieșire din stoc
                "property_stock_account_output_categ_id": self.property_stock_account_output_categ_id.id,
                # Cont Evaluare  Stoc
                "property_stock_valuation_account_id": self.property_stock_valuation_account_id.id,
                # Jurnal de stoc
                "property_stock_journal": self.property_stock_journal.id,
                # Metodă de cost
                "property_cost_method": self.property_cost_method,
                # property_valuation
                "property_valuation": self.property_valuation,
            }
            childs.write(values)

    # TO REMOVE - DACA NU FOLOSIM CAMPUL - DE COMPLETAT CU UN EXTRABILANTIER
    @api.constrains(
        "property_stock_valuation_account_id",
        "property_stock_account_output_categ_id",
        "property_stock_account_input_categ_id",
    )
    def _check_valuation_accouts(self):
        # pentru Romania contul de evaluarea a stocului este egal cu cel intrare/iesire
        pass


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_stock_account_input_id = fields.Many2one(
        "account.account",
        "Stock Input Account",
        company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]",
        check_company=True,
        help="""Counterpart journal items for all incoming stock moves will be posted in this account, unless there is a specific valuation account
                set on the source location. This is the default value for this product""",
    )
    property_stock_account_output_id = fields.Many2one(
        "account.account",
        "Stock Output Account",
        company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]",
        check_company=True,
        help="""When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account,
                unless there is a specific valuation account set on the destination location. This is the default value for this product""",
    )

    def write(self, vals):
        if "list_price" in vals:
            self.do_change_list_price(vals["list_price"])
        res = super(ProductTemplate, self).write(vals)
        return res

    # TO REMOVE - USE _get_product_accounts sa facem update la stock_input si stock_output cu cele din produs, poate si din locatie daca o putem da in context
    def get_product_accounts(self, fiscal_pos=None):
        res = super(ProductTemplate, self).get_product_accounts(fiscal_pos)
        notice = self.env.context.get("notice")
        if notice and self.purchase_method == "receive" and self.type == "product":
            res["stock_input"] = (
                self.env.user.company_id.property_stock_picking_payable_account_id.id
                or self.property_stock_account_input.id
                or self.categ_id.property_stock_account_input_categ_id.id
            )

        fix_stock_input = self.env.context.get("fix_stock_input")
        if fix_stock_input:
            res["stock_input"] = fix_stock_input
        return res

    def do_change_list_price(self, new_price):
        """ Changes the Standard Price of Product and creates an account move accordingly."""
        AccountMove = self.env["account.move"]

        products = self.env["product.product"]
        for product_tmpl_id in self:
            products |= product_tmpl_id.product_variant_ids

        quant_locs = (
            self.env["stock.quant"]
            .sudo()
            .read_group(
                [("product_id", "in", products.ids)], ["location_id"], ["location_id"]
            )
        )
        quant_loc_ids = [loc["location_id"][0] for loc in quant_locs]
        locations = self.env["stock.location"].search(
            [
                ("usage", "=", "internal"),
                ("company_id", "=", self.env.user.company_id.id),
                ("id", "in", quant_loc_ids),
            ]
        )

        product_accounts = {
            product.id: product.product_tmpl_id.get_product_accounts()
            for product in products
        }
        ref = self.env.context.get("ref", _("Price changed"))
        to_date = fields.Date.today()
        for location in locations.filtered(lambda r: r.merchandise_type == "store"):

            for product in products.filtered(lambda r: r.valuation == "real_time"):
                old_price = product.list_price
                diff = old_price - new_price
                if not diff:
                    continue
                if not product_accounts[product.id].get("stock_valuation", False):
                    raise UserError(
                        _(
                            "You don't have any stock valuation account defined on your product category. You must define one before processing this operation."
                        )
                    )

                account_id = product.property_account_creditor_price_difference
                if not account_id:
                    account_id = (
                        product.categ_id.property_account_creditor_price_difference_categ
                    )
                if not account_id:
                    raise UserError(
                        _(
                            "Configuration error. Please configure the price difference account on the product or its category to process this operation."
                        )
                    )

                # product = product.with_context(to_date=to_date)

                # if product.qty_available:
                #     old_price = abs(product.stock_value / product.qty_available)

                product = product.with_context(
                    location=location.id, compute_child=False
                )

                qty_available = product.qty_available
                if qty_available:
                    # Accounting Entries

                    if diff * qty_available > 0:
                        debit_account_id = account_id.id
                        credit_account_id = product_accounts[product.id][
                            "stock_valuation"
                        ].id
                    else:
                        debit_account_id = product_accounts[product.id][
                            "stock_valuation"
                        ].id
                        credit_account_id = account_id.id
                    name = self.env.context.get(
                        "ref", _("List Price changed  - %s") % (product.display_name)
                    )
                    move_vals = {
                        "journal_id": product_accounts[product.id]["stock_journal"].id,
                        "company_id": location.company_id.id,
                        "ref": ref,
                        "line_ids": [
                            (
                                0,
                                0,
                                {
                                    "name": name,
                                    "account_id": debit_account_id,
                                    "debit": abs(diff * qty_available),
                                    "credit": 0,
                                    "product_id": product.id,
                                    "stock_location_id": location.id,
                                },
                            ),
                            (
                                0,
                                0,
                                {
                                    "name": name,
                                    "account_id": credit_account_id,
                                    "debit": 0,
                                    "credit": abs(diff * qty_available),
                                    "product_id": product.id,
                                    "stock_location_id": location.id,
                                },
                            ),
                        ],
                    }
                    move = AccountMove.create(move_vals)
                    move.post()

        return True


class ProductProduct(models.Model):
    _inherit = "product.product"

    # TO CHECK - METODA NU MAI EXISTA
    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        res = super(ProductProduct, self)._convert_prepared_anglosaxon_line(
            line, partner
        )
        res["stock_location_id"] = line.get("stock_location_id", False)
        res["stock_location_dest_id"] = line.get("stock_location_dest_id", False)
        return res

    # TO CHECK - METODA NU MAI EXISTA
    def _compute_stock_value(self):
        location = self.env.context.get("location")
        return super(ProductProduct, self)._compute_stock_value()
