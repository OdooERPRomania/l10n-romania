# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import fields, models


"""
class purchase_order(models.Model):
    _inherit = 'purchase.order'

    # todo: care o fi metoda in Odoo10  - pregateste  pretul cu care se va face intrare in stoc
    @api.model
    def _prepare_order_line_move(self, order, order_line,  picking_id, group_id ):
        '''
        prepare the stock move data from the PO line. This function
        returns a list of dictionary ready to be used in stock.move's
        create()
        '''

        res = super()._prepare_order_line_move(  order, order_line, picking_id, group_id)
        product_uom = self.pool.get('uom.uom')
        price_unit = order_line.price_unit
        if order_line.product_uom.id != order_line.product_id.uom_id.id:
            price_unit *= order_line.product_uom.factor /  order_line.product_id.uom_id.factor
        ctx = dict(self.env.context)
        ctx.update({'date': order.date_order})
        if order.currency_id.id != order.company_id.currency_id.id:
            #we don't round the price_unit, as we may want to store the
            #standard price with more digits than allowed by the currency
            price_unit = self.pool.get('res.currency').compute(  order.currency_id.id, order.company_id.currency_id.id,  price_unit, round=False)
        for line in res:
            line['price_unit'] = price_unit
        return res
"""


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_account_move_line(self, move=False):
        """modify the account if this inovice is for a notice/aviz stock movement that hapend before
            is setting account 408 that must be used if the goods where received with notice/aviz before the invoice"""
        
        data = super()._prepare_account_move_line(move)  
#     408000    Furnizori - facturi nesosite  must be  Current Liabilities    ​            
#  it can not be selected in account-move_line  because is anything beside  receivable payable 
# if not the amount is going to be wrong computed and = with taxex

#     purchase_method =
#         ('purchase', 'On ordered quantities:Control bills based on ordered quantities
#         ('receive', 'On received quantities' Control bills based on received quantities

        if  self.product_id.purchase_method == "receive":  
            # receptia in baza cantitatilor primite
            if self.product_id.type == "product":
                notice = False
                for picking in self.order_id.picking_ids:
                    if picking.notice:
                        notice = True
                if notice:  # daca e stocabil si exista un document facut  ???????????
                    data["account_id"] = self.company_id.property_stock_picking_payable_account_id.id 
                else:
                    data["account_id"] = self.product_id._get_product_accounts()["stock_valuation"]
# default behavior so we are not going to put anymore
#             else:  # daca nu este stocabil trebuie sa fie un cont de cheltuiala
#                 data["account_id"] = self.product_id.categ_id.property_account_expense_categ_id.id
        else:  # Control bills based on ordered quantities
            if self.product_id.type == "product":
                data["account_id"] = self.product_id._get_product_accounts()["stock_valuation"]

        return data
