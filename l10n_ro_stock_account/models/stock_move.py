# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from forks_addons.odoo.doc._extensions.pyjsparser.parser import false, true

_logger = logging.getLogger(__name__)

#!!! svl= StockValuationLine
#!!! in create_account functions we are changing the acc_src with acc_dest because the value can be - and that is changing debit with credit


# is good to use from stock_account    ( functions of product)    maybe to be used?
#     def _stock_account_get_anglo_saxon_price_unit(self, uom=False):
#         price = self.standard_price
#         if not self or not uom or self.uom_id.id == uom.id:
#             return price or 0.0
#         return self.uom_id._compute_price(price, uom)

#     def _compute_average_price(self, qty_invoiced, qty_to_invoice, stock_moves):
#         """Go over the valuation layers of `stock_moves` to value `qty_to_invoice` while taking
#         care of ignoring `qty_invoiced`. If `qty_to_invoice` is greater than what's possible to
#         value with the valuation layers, use the product's standard price.
# 
#         :param qty_invoiced: quantity already invoiced
#         :param qty_to_invoice: quantity to invoice
#         :param stock_moves: recordset of `stock.move`
#         :returns: the anglo saxon price unit
#         :rtype: float
#         """
#         self.ensure_one()
#         if not qty_to_invoice:
#             return 0.0
# 
#         if not qty_to_invoice:
# ......
#             if float_is_zero(qty_to_take_on_candidates, precision_rounding=candidate.uom_id.rounding):
#                 break
# 
#         # If there's still quantity to invoice but we're out of candidates, we chose the standard
#         # price to estimate the anglo saxon price unit.
#         if not float_is_zero(qty_to_take_on_candidates, precision_rounding=self.uom_id.rounding):
#             negative_stock_value = self.standard_price * qty_to_take_on_candidates
#             tmp_value += negative_stock_value
# 
#         return tmp_value / qty_to_invoice


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    picking_type_code = fields.Selection(related='picking_id.picking_type_code', readonly=True,help="taken from stock_picking that is taken from stock_picking_type.code")

    stock_move_type = fields.Char(help="""
reception   - Nici o nota contabila pe receptie pt ca e in factura 371+4426 = 401
reception_refund  - rambursare receptie nu face note contabile 

reception_notice",   # receptie Primirea marfurilor pe baza de aviz de insotire: ex 371 = 408
reception_refund_notice", "Reception refund with notice",  # rabursare receptie facuta cu aviz. face nota inversa ponderata la cantitate
            
reception_store", "Reception in store"  # receptie in magazin
reception_refund_store", "Reception regund in store"  # rambursare receptie in magazin. face nota inversa ponderata la cantitate

            
reception_store_notice", 
reception_refund_store_notice   # rabursare receptie in magazin facuta cu aviz. face nota inversa ponderata la cantitate

delivery  - nu face note contabile pentru ca se fac pe factura
delivery_refund", "Delivery refund"

delivery_notice     # Create account moves for deliveries with notice (e.g. 418 = 707)
delivery_refund_notice   face nota inversa ponderata la cantitate

delivery_store 
delivery_refund_store  face nota inversa ponderata la cantitate

delivery_store_notice 
delivery_refund_store_notice   face nota inversa ponderata la cantitate

consume  darea in folosinta # cheltuiala = stock_valuation & 8035=8035
            
inventory_plus # cont stoc la cont de cheltuiala  # 758800 Alte venituri din exploatare ;  
                60X Cheltuieli privind stocurile    =    30X, 37X Conturi de stocuri    -Valoarea plusului
    *varianta aleasa         30X, 37X Conturi de stocuri    =    758 Alte venituri din exploatare    Valoarea plusului venitul este impozabil

inventory_plus_store, 
inventory_minus   # cont de cheltuiala la cont de stoc # 758800 Alte venituri din exploatare
inventory_minus_store, 
            
production  "Reception from production" 345" Produse finite" =711 "Venituri aferente costurilor stocurilor de produse"
            
transfer  371.gest1= 371.gest2 5 lei doar daca conturile sunt diferite daca exista cel putin un cont pe locatie si unul la produs
transfer_store

transit_in   30x =482   decont intre subunitati
transit_out   482 = 30x   decont intre subunitati
            
consume_store 
production_store
""",
        default="")


    def _get_out_move_lines(self):
        """ original from stock_account/sock_move.py  Returns the `stock.move.line` records of `self` considered as outgoing. 
It is done thanks   to the `_should_be_valued` method of their source and destionation location as well as their owner.
# def _should_be_valued(self):   if self.usage == 'internal' or (self.usage == 'transit' and self.company_id): return True
we overide this because otherwise will not make accounting entries for internal - transit

        :returns: a subset of `self` containing the outgoing records
        :rtype: recordset
        """
        self.ensure_one()
        res = self.env['stock.move.line']
        if  self.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1] :
            for move_line in self.move_line_ids:
                if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                    continue
                if (move_line.location_id._should_be_valued() and not move_line.location_dest_id._should_be_valued()) or \
                    (move_line.location_id.usage == "internal" and move_line.location_dest_id.usage == "transit"):
                    res |= move_line
        else:
            res = super()._get_out_move_lines()
        return res
    def _get_in_move_lines(self):
        self.ensure_one()
        res = self.env['stock.move.line']
        if  self.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1] :
            for move_line in self.move_line_ids:
                if move_line.owner_id and move_line.owner_id != move_line.company_id.partner_id:
                    continue
                if not move_line.location_id._should_be_valued() and move_line.location_dest_id._should_be_valued() or \
                    (move_line.location_id.usage == "transit" and move_line.location_dest_id.usage == "internal"):
                    res |= move_line
        else:
            res = super()._get_out_move_lines()
        return res

##################### generare note contabile suplimentare pentru miscarea de stoc################################################################
##################### generare note contabile suplimentare pentru miscarea de stoc################################################################
    def _account_entry_move(self, qty, description, svl_id, cost):
        """ 
        is only called if the product has real_time valuation. 
        if it has manual(periodic) valuation is not going to make accounting entries
        Accounting Valuation Entries called from stock_account.stock_move.py.action_done that is called form stock_picking.button_validate
        If is Romanian accounting will use this function otherwise the original from stock_account
        """
        self.ensure_one()
        if not self.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1]:
            # is not Romanian accounting
            return super()._account_entry_move(self, qty, description, svl_id, cost)
        
        # convert from UTC (server timezone) to user timezone
#         use_date = fields.Datetime.context_timestamp(self, timestamp=fields.Datetime.from_string(self.date))
#         use_date = fields.Date.to_string(use_date)
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

#         company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
#         company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False
        delivery = False
        if self.origin_returned_move_id:     ############# is a refund   ############# is a refund  ############# is a refund ############# is a refund 
            _logger.info(f"is a returned move of this move {self.origin_returned_move_id}")
            if location_from.usage == "internal" and location_to.usage == "supplier":
                stock_move_type += "_reception_refund"
            elif location_from.usage == "customer" and location_to.usage == "internal":
                stock_move_type += "_delivery_refund"
                delivery = True
            if "refund" in stock_move_type:
                if notice or store:
                    _logger.info( f'{stock_move_type}  notice or store reversing accounting entries')
                    original_accounting_move = self.env['account.move'].search([('state','=','posted'),('stock_move_id','=', self.origin_returned_move_id.id)])
                    refund_accounting_values = {'stock_move_id':self.id, 'journal_id':original_accounting_move.journal_id.id}
                    if self.origin_returned_move_id.product_qty != (-1 if not delivery else 1) * qty:  # partial refund, we must modify the accounting move lines
                        orig_acc_lines = original_accounting_move.with_context(include_business_fields=True).copy_data()[0]['line_ids']
                        for orig_acc_line in orig_acc_lines :
                            orig_acc_line[2]['quantity'] = qty
                            orig_acc_line[2]['debit'] *= -1*qty/self.origin_returned_move_id.product_qty 
                            orig_acc_line[2]['credit'] *= -1*qty/self.origin_returned_move_id.product_qty
                        refund_accounting_values['line_ids'] = orig_acc_lines
                    reversed_account_move = original_accounting_move._reverse_moves(default_values_list=[refund_accounting_values])
                    reversed_account_move.post()
                else:
                    _logger.info(f'{stock_move_type} no accounting entries because no accounting entries were done')

        elif location_from.usage == "supplier":  ############### is NOT refund 
            if  location_to.usage == "internal":
                stock_move_type +=  "_reception"
                if store or notice:
                    self.stock_move_type = stock_move_type
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, store=store, cost=cost, notice=notice)
                else:
                    _logger.info(f"Nici o nota contabila pe receptie pt ca e in factura 371+4426 = 401")
                    self.stock_move_type = stock_move_type
                    return # we are not doing accounting entry because those done in invoice are sufficient
                
        
        elif location_from.usage == "internal":
            if location_to.usage == "customer":
                stock_move_type += "_delivery"   ##############  delivery   ##############  delivery
                if store or notice:  
                    _logger.info(f"Nota contabila livrare din store={store} aviz={notice} stock_move_type={stock_move_type}")
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, delivery=True)
                    self.stock_move_type = stock_move_type
                    _logger.info(f"Nici o nota contabila delivery pt ca e in factura 371+4426 = 401")
                    return
                
            elif location_to.usage == "production":
                stock_move_type += "_consume"
                self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, delivery=True,consume=True)
                 
            elif location_to.usage == "inventory":
                stock_move_type += "inventory_minus"
                self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, inventory=True, delivery=True)
            
            elif location_to.usage == "internal":
                stock_move_type += "_transfer"
                self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, inventory=False, delivery=True) # or false?
                
            elif location_to.usage == "transit":
                #Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations
                if self.picking_id.partner_id.commercial_partner_id and ( self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id ):
                    stock_move_type += "_delivery"      ##############  delivery  
                    if store or notice:
                        self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, delivery=True)
                else:
                    stock_move_type += "_transit_out"
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, inventory=False, transit=True,  delivery=True)

        elif location_from.usage == "inventory":
            if location_to.usage == "internal":
                stock_move_type += "_inventory_plus"
                if store:
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, notice=notice, inventory=True)
                else:
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=False, notice=notice, inventory=True)
                
        elif location_from.usage == "production":
            if  location_to.usage == "internal":
                 stock_move_type += "_production"
                 self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, notice=notice, store=store,production=True)
                 
        elif location_from.usage == "transit":
            if location_to.usage == "internal":
                if self.picking_id.partner_id.commercial_partner_id and (self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id):
                    stock_move_type += "_reception"
                    if notice:
                        self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, notice=notice, store=store)
                    else:
                        pass  # the accounting moves are on invoice
                else:
                    stock_move_type += "_transit_in"
                    self._create_account_reception_in_store_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, store=store, notice=notice, inventory=False, transit=True)
        
        if stock_move_type == stock_move_type_initial:
            raise UserError(f"Something is wrong at creating stock_move account entries.\nUnknown operation for location_from={location_from.complete_name} location_to={location_to.complete_name};\nlocation_from.usage={location_from.usage} location_to.usage={location_to.usage} ")
        self.stock_move_type = stock_move_type
        return


##### functions called based on stock_move_type  ##### functions called based on stock_move_type   ##### functions called based on stock_move_type  
    def _create_account_move_lineS(self, parameters):#  0credit_account_id, 1debit_account_id, 2journal_id, 3qty, 4description, 5svl_id, 6cost
        "original from stock_account.stock_move.py._create_account_move_line; but this can create more move_lines"
        self.ensure_one()
        AccountMove = self.env['account.move'].with_context(default_journal_id=parameters[0][2])
        
        move_lines = []
        for param in parameters:
            move_lines += self._prepare_account_move_line(qty=param[3], cost=param[6], credit_account_id=param[0], debit_account_id=param[1], description=param[4])
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': parameters[0][2],
                'line_ids': move_lines,
                'date': date,
                'ref': ''.join([p[4] for p in parameters]),
                'stock_move_id': self.id,
                'stock_valuation_layer_ids': [(6, None, [p[5] for p in parameters])],
                'move_type': 'entry',
            })
            new_account_move.post()


    def _create_account_reception_in_store_14(self, qty ,description, svl_id, cost, store=True, notice=False, delivery=False, inventory=False, transit=False, production=False, consume=False, transfer=False):
        '''
        Receptions in location with inventory kept at list price
        Create account move with the price difference one (3x8) to suit move: 3xx = 3x8
        Create account move with the uneligible vat one (442810) to suit move: 3xx = 442810
https://www.contzilla.ro/monografii-contabile-pentru-activitatea-unui-magazin-comert-cu-amanuntul/
b) Calcularea si inregistrarea diferentelor de pret la marfuri

Datorita faptului ca pentru evidentierea in contabilitate a marfurilor entitatea utilizeaza pretul cu amanuntul, 
ulterior inregistrarii stocurilor la cost de achizitie, se calculeaza si se inregistreaza diferentele de pret care vin sa corecteze valoarea de achizitie pana la nivelul pretului de vanzare cu amanuntul, astfel:

Adaosul comercial = 30% * pretul de achizitie = 30% * 100.000 lei = 30.000 lei

Tva neexigibila = ( cost de achizitie + adaos comercial) * 19 % = (100.000 lei +30.000 lei )*19 % = 24.700 lei

Pentru a se obtine pretul de vanzare cu amanuntul se utilizeaza urmatoarea formula:

Capture

***) Tva –ul se reflecta in pretul de vanzare cu amanuntul insa devine exigibil numai cand se realizeaza vanzarea marfurilor. 
Pana la acel moment se reflecta in contul 4428 Tva neexigibil, dupa care se reflecta in contul 4427 Tva colectata.

Prin urmare, pretul de vanzare cu amanuntul = 100.000 lei + 30.000 lei + 24.700 lei = 154.700 lei

Notele contabile prin care se reflecta in contabilitate diferentele de pret sunt :

371 Marfuri            =                             %                                              54.700

                                             378 Diferente de pret la marfuri           30.000

                                             4428 Tva neexigibila                                24.700
        '''   
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data['stock_valuation'].id  
        journal_id = accounts_data['stock_journal'].id
        account_move_lineS = []
        if inventory or notice or transfer or consume or production or transit or (store and delivery and notice): 
            if store and delivery and notice:
                # descarcare de gestiune la pretul de cost
                acc_src = accounts_data['income'].id  #!!!!!!!!!!!!!!!!  aici trebuie luat un alt cont si nu stiu de unde de ex 711 
                acc_dst = accounts_data['stock_valuation'].id
            elif transfer:
                acc_dest =  self.location_id.valuation_out_account_id.id or accounts_data['stock_valuation'].id  
                acc_src = self.location_dest_id.valuation_in_account_id.id or accounts_data['stock_valuation'].id
                if acc_src == acc_dest:     
                    return # we are not creating any accounting entries
            elif consume:  
                acc_src1 = acc_dest2 = self.company_id.property_stock_usage_giving_account_id.id
                if not acc_src1:
                    raise UserError(f"Something is wrong at creating consume(darea in folosinta) stock_move account entries.\nYou have not selected a property_stock_picking_payable_account_id in settings on compnay.\n select 8035. ")
                acc_src = accounts_data['expense'].id
            elif production:
                acc_src = accounts_data['income'].id
            elif transit:
                acc_src = self.company_id.property_stock_transfer_account_id.id 
                if not acc_src:
                    raise UserError(f"Something is wrong at creating transit_out stock_move account entries.\nYou have not selected in company Romanian setting property_stock_transfer_id.\nUse 482 decont intre subunitati. ")
            elif inventory:
                if delivery:
                    acc_src = self.location_id.valuation_in_account_id.id
                else:
                    acc_src = self.location_id.valuation_out_account_id.id
                if not acc_src:
                    raise UserError(f"Something is wrong at creating inventory_plus stock_move account entries.\nYou have not selected a valuation_out_account_id for location {self.location_id.complete_name}.\n Use account 7588. ")
            elif notice:
                if delivery:
                    acc_src = self.company_id.property_stock_picking_receivable_account_id.id
                else:
                    acc_src = self.company_id.property_stock_picking_payable_account_id.id
                if not acc_src:
                    raise UserError(f"Something is wrong at creating accounting entry at reception.\n please configure property_stock_picking_receivable/payable_account_id in romanian settings ")


            self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)

            account_move_lineS = [(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)]

        if store:     
            if not delivery:    
                # price difference account
                acc_src_price_diff = self.location_dest_id.property_account_creditor_price_diff_location_id.id or \
                                        self.product_id.property_account_creditor_price_difference.id or \
                                        self.product_id.categ_id.property_account_creditor_price_difference_categ.id
        
                if not acc_src_price_diff:
                    raise UserError(_(
                        'Configuration error. Please configure the price difference account on the location or product or its category to process this operation.'))
                
                list_price = self.product_id.list_price #list_price=sales price taken from product filed lst_price  is the price from pricelist 
                taxes_ids = self.product_id.taxes_id.filtered(lambda r: r.company_id == self.company_id)
                if taxes_ids:
                    taxes = taxes_ids.compute_all(price_unit=list_price, quantity=qty, product=self.product_id)
                    stock_value = taxes['total_excluded']
                else:
                    stock_value = list_price * qty
        
                if abs(stock_value) <= abs(cost):  #??? and list_price != 0.0:
                    raise UserError(_(f"You cannot move a product '{self.product_id.name}' if price list is lower than cost price. Please update list price to suit to be higher than {stock_value}/{qty}"))
                self._valid_only_if_dif_credit_debit_account(acc_src_price_diff, acc_dest)
                account_move_lineS += [(acc_src_price_diff, acc_dest, journal_id,qty, description, svl_id, stock_value-cost)]
        
                # uneligible tax  | tva neexigibil
                uneligible_tax = 0
                if taxes_ids:
                    uneligible_tax = taxes['total_included'] - taxes['total_excluded'] 
                if uneligible_tax:
                    acc_uneligibl_tax = self.company_id.property_uneligible_tax_account_id.id
                    if not acc_uneligibl_tax:
                        raise UserError(_(
                            'Configuration error. Please configure in romania company settings property_uneligible_tax_account_id .'))
                    self._valid_only_if_dif_credit_debit_account(acc_uneligibl_tax, acc_dest)
                    account_move_lineS += [(acc_uneligibl_tax, acc_dest, journal_id,qty, description, svl_id, uneligible_tax)]
            elif delivery and notice:  # is delivery sale 
# accounting entires on delivery from store only if delivery and notice; else all the accounting are going to be on invoice
 # Societatea ABC livreaza pe baza de aviz de insotire a marfii firmei DEF produse finite pe care clientul urmeaza sa le comercializeze ca si 
 #marfuri la pretul de fabricare fara TVA de 95.000 lei, TVA 20%. 
 #In luna urmatoare, se intocmeste factura fiscala care se deconteaza in numerar. Costul de productie al produselor finite este de 82.000 lei. 
#Contabilitatea firmei ABC:
#livrarea produselor pe baza avizului:
#    418 = %          114.000
#          701        95.000
#          4428      19.000
#    descarcarea din gestiune:
#    711 = 345       82.000
#emiterea facturii:
#    4111 = 418      114.000
#    transformarea TVA neexigibil in TVA colectat:
#   4 428 = 4427     19.000
                acc_src = self.company_id.property_stock_picking_receivable_account_id.id  # 418
                acc_dest = accounts_data['income'].id
                if not acc_src:
                    raise UserError(_('Configuration error. Please configure property_stock_picking_receivable_account_id in romanian stock configuration.'))
                list_price = self.product_id.list_price #list_price=sales price taken from product filed lst_price  is the price from pricelist 
                taxes_ids = self.product_id.taxes_id.filtered(lambda r: r.company_id == self.company_id)
                if taxes_ids:
                    taxes = taxes_ids.compute_all(price_unit=list_price, quantity=qty, product=self.product_id)
                    stock_value = taxes['total_excluded']
                else:
                    stock_value = list_price * qty
                if abs(stock_value) <= abs(cost):  #??? and list_price != 0.0:
                    raise UserError(_(f"You cannot move a product '{self.product_id.name}' if price list is lower than cost price. Please update list price to suit to be higher than {stock_value}/{qty}"))
                self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
                account_move_lineS += [(acc_src, acc_dest, journal_id,qty, description, svl_id, stock_value)]
        
                # uneligible tax  | tva neexigibil
                uneligible_tax = taxes['total_included'] - taxes['total_excluded'] 
                if uneligible_tax:
                    acc_uneligibl_tax = self.company_id.property_uneligible_tax_account_id.id
                    if not acc_uneligibl_tax:
                        raise UserError(_(
                            'Configuration error. Please configure in romania company settings property_uneligible_tax_account_id .'))
                    self._valid_only_if_dif_credit_debit_account(acc_uneligibl_tax, acc_src)
                    account_move_lineS += [(acc_src, acc_uneligibl_tax, journal_id,qty, description, svl_id, uneligible_tax)]
    
        self._create_account_move_lineS(account_move_lineS)
        if consume:
            self._create_account_move_lineS([(acc_src1, acc_dest2, journal_id,qty, description, svl_id, cost)])
    
    
    def _is_dropshipped(self):        ### to verify
        stock_move_type = self.stock_move_type
        if stock_move_type and ("transfer" in stock_move_type or "transit" in stock_move_type):
            return True
        return super()._is_dropshipped()



    def _valid_only_if_dif_credit_debit_account( self, credit_account_id, debit_account_id, ):
        "raise error if debit and credit account are equal (must be called from transfers that are not internal)"
        if credit_account_id == debit_account_id :
            raise UserError("For this transfer, creidt_account_id=debit_account_id={debit_account_id.code} {debit_account_id.name}.\n Because is not a internal transfer something must be wrong configurated")
        