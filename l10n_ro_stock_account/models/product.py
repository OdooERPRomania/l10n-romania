# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = "product.category"

    hide_stock_in_out_account = fields.Boolean(compute="_is_romania_accounting",help="only for Romania, to hide stock_input and stock_output account because are the same as stock_valuation account")

    @api.depends('name')
    def _is_romania_accounting(self):
        for record in self:
            if record.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1]:
                record.hide_stock_in_out_account = True
            else:
                record.hide_stock_in_out_account = False

    @api.constrains('property_stock_valuation_account_id', 'property_stock_account_output_categ_id', 'property_stock_account_input_categ_id')
    def _check_valuation_accouts(self):
        """ overwrite default constraint for Romania
            for Romania, stock_valuation output and input are the same
        """
        if self.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1]:
            # is a romanian company:
            for record in self:
                    if record.property_stock_account_input_categ_id != record.property_stock_account_output_categ_id and \
                       record.property_stock_account_input_categ_id != record.property_stock_valuation_account_id:
                        raise UserError(f"At  {record.name} for Romania the stoc_input account must be the same as stock_output and the same as valuation")
        else:
            self.super()._check_valuation_accouts()

    @api.onchange('property_stock_valuation_account_id', 'property_stock_account_output_categ_id', 'property_stock_account_input_categ_id')
    def _onchange_stock_accouts(self):
        """ only for Romania, stock_valuation output and input are the same
        """
        for record in self:
            if record.hide_stock_in_out_account:
                # is a romanian company:
                record.property_stock_account_input_categ_id = record.property_stock_valuation_account_id
                record.property_stock_account_output_categ_id = record.property_stock_valuation_account_id


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_stock_valuation_account_id = fields.Many2one("account.account", "Stock Valuation Account",
        company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]",
        check_company=True,
        help="In Romania accounting is only one account for valuation/input/output. If this value is set, we will use it, otherwise will use the category value. ",
    )

    def _get_product_accounts(self):
        "default account value is taken from category. now values in product will overwrite those from category"
        accounts = super()._get_product_accounts()
 
        if  self.property_stock_valuation_account_id:
            accounts.update({
                'stock_input': self.property_stock_valuation_account_id,
                'stock_output': self.property_stock_valuation_account_id,
                'stock_valuation': self.property_stock_valuation_account_id,
            })

        return accounts


    def write(self, vals):
        "override the write at any change in list_price to call a function that creates accounting entries"
        if "list_price" in vals:
            self.do_change_list_price(vals["list_price"])
        res = super().write(vals)
        return res


    def do_change_list_price(self, new_price):
        """ Changes the Standard Price of Product and creates an account move accordingly.
            just for products that have real_time valuation
        """
        AccountMove = self.env["account.move"]

        products = self.env["product.product"]
        for product_tmpl_id in self.filtered(lambda r: r.valuation == "real_time" and r.type == "product"):  
            products |= product_tmpl_id.product_variant_ids
            
        quant_locs = self.env["stock.quant"].sudo().read_group(
                [("product_id", "in", products.ids)], ["location_id"], ["location_id"]
            )
        quant_loc_ids = [loc["location_id"][0] for loc in quant_locs]
        locations =  self.env["stock.location"].search([ ("usage", "=", "internal"),
                                                        ("merchandise_type", "=", "store"),
                                                        ("company_id", "=", self.env.company.id), #self.env.user.company_id.id 
                                                        ("id", "in", quant_loc_ids),])
 
        product_accounts = { product.id: product.product_tmpl_id.get_product_accounts() for product in products}
        ref = self.env.context.get("ref", _("Price changed")+f" ->{new_price}")
        to_date = fields.Date.today()
        for location in locations:
            for product in products:
                old_price = product.list_price
                diff = old_price - new_price
                if not diff:
                    continue
                if not product_accounts[product.id].get("stock_valuation", False):
                    raise UserError(_( "You don't have any stock valuation account defined on your product category. You must define one before processing this operation."))

                account_id = product.property_account_creditor_price_difference or product.categ_id.property_account_creditor_price_difference_categ
                if not account_id:
                    raise UserError( _("Configuration error. Please configure the price difference account on the product or its category to process this operation."))

                product = product.with_context(location=location.id, compute_child=False)

                qty_available = product.qty_available
                if qty_available:
                    # Accounting Entries

                    debit_account_id = account_id.id
                    credit_account_id = product_accounts[product.id][ "stock_valuation"].id

                    if diff * qty_available < 0:
                        debit_account_id, credit_account_id = credit_account_id, debit_account_id
                    name =  _("List Price changed ") + product.display_name  +f" {product.list_price}->{new_price} X {product.qty_available}"
                    move_vals = {
                        "journal_id": product_accounts[product.id]["stock_journal"].id,
                        "company_id": location.company_id.id,
                        "ref": ref,
                        "line_ids": [
                            (0, 0, {
                                    "name": name,
                                    "account_id": debit_account_id,
                                    "debit": abs(diff * qty_available),
                                    "credit": 0,
                                    "product_id": product.id,
                                    "stock_location_id": location.id,
                                },),
                            (0, 0, {
                                    "name": name,
                                    "account_id": credit_account_id,
                                    "debit": 0,
                                    "credit": abs(diff * qty_available),
                                    "product_id": product.id,
                                    "stock_location_id": location.id,
                                }, ), ],
                                }
                    move = AccountMove.create(move_vals)
                    move.post()

        return True

