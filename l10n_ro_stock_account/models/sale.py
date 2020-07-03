# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        """Modify the account if this inovice is for a notice/aviz stock movement that hapend before.
           Is setting account 418 that must be used if the goods where sent before the invoice
           Account 418 must be != recivable        if not it can not be put into invoice and also the base is wrong at computing taxes
           If location has a property_account_income_location_id we will give this instead of that from product

           If is sale from a store will put also the noneligible vat 

        

        """
        res = super()._prepare_invoice_line(**optional_values)
        # Overwrite with at least one location with income account defined
        for picking in self.order_id.picking_ids:
            moves = picking.move_line_ids.filtered(lambda m: m.state == "done")
            for move in moves:
                if move.location_id.property_account_income_location_id:
                    res["account_id"] = move.location_id.property_account_income_location_id
                    break

# put the account 418  clienti facturi de intocmit 
        if self.product_id.invoice_policy == "delivery":
            if any([picking.notice  for picking in self.order_id.picking_ids]):
                res["account_id"] = self.company_id.property_stock_picking_receivable_account_id 

        return res

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        override the original to create in invoice also a line 4428 - (418 or 7xx)   with the vat values
        
        """

        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            # if the source location is type store will add  a line with 4428 = 4427     vat 
            lines_to_add = []
            for line in move.line_ids:
                # if is a tax from a store location we are going to search for vat
                if line.display_type: 
                    continue
                if not (line.product_id.type=="product" and line.product_id.valuation == "real_time"):
                    continue
# working only on notice | aviz
#                 sale_lines = line.sale_line_ids
#                 stock_moves = self.env['stock.move'].search([('id', 'in', sale_lines._ids)])
#                 if stock_moves.filterd(lambda sm: sm.location_id.merchandise_type == "store"):
#                         print("we must create the account lines")
#                 else: 
#                     continue
                if self.picking_ids.filtered(lambda p: p.location_id.merchandise_type == "store"):
                    print("we must create the account_lines; this is the line with product that has vat or does not have")
                    # search the vat tax for this line if exist
                    if not line.tax_ids: 
                        continue
                    product_account_id = line.account_id.id 
                    tax_line = move.line_ids.filtered(lambda l: l.tax_base_amount == line.credit and l.tax_line_id in line.tax_ids)[0]
                    tax_value = tax_line.credit
                    acc_uneligibl_tax = self.company_id.property_uneligible_tax_account_id.id
                    if not acc_uneligibl_tax:
                        raise UserError(_(
                            'Configuration error. Please configure in romania company settings property_uneligible_tax_account_id .'))
                    modified_tax_value_copy_dict = tax_line.copy_data()[0]
                    modified_tax_value_copy_dict.update({'account_id': product_account_id,
                                                                      'debit': 0,
                                                                      'credit': tax_value,
                                                                       'tax_repartition_line_id': False,
                                                                       'name': f"uneligible for product={line.product_id.name} qty={line.quantity} tax={tax_line.name} id={line.id}",
                                                                       "full_reconcile_id": False,
                                                                       "matching_number": False,
                                                                       })
                    lines_to_add.append(modified_tax_value_copy_dict.copy()) 
                    modified_tax_value_copy_dict.update({'account_id': acc_uneligibl_tax,
                                                                      'debit': tax_value,
                                                                      'credit': 0,
                                                                       'tax_repartition_line_id': False,
                                                                       'name': f"uneligible for product={line.product_id.name} qty={line.quantity} tax={tax_line.name} id={line.id}",
                                                                       "full_reconcile_id": False,
                                                                       "matching_number": False,
                                                                       })
                    lines_to_add.append(modified_tax_value_copy_dict.copy()) 

            if lines_to_add:
                self.env['account.move.line'].create(lines_to_add)
#                move["line_ids"] = [lines_to_add]
        return moves
    