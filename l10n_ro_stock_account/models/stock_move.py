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


# is good to use from stock_account    ( functions of product
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

reception_notice", "Reception with notice"  # receptie pe baza de aviz
reception_refund_notice", "Reception refund with notice",  # rabursare receptie facuta cu aviz. face nota inversa ponderata la cantitate
            
reception_store", "Reception in store"  # receptie in magazin
reception_refund_store", "Reception regund in store"  # rambursare receptie in magazin. face nota inversa ponderata la cantitate

            
reception_store_notice", "Reception in store with notice"
reception_refund_store_notice", "Reception refund in store with notice",  # rabursare receptie in magazin facuta cu aviz. face nota inversa ponderata la cantitate

delivery  - nu face note contabile pentru ca se fac pe factura
delivery_refund", "Delivery refund"

delivery_notice,     # Create account moves for deliveries with notice (e.g. 418 = 707)
delivery_refund_notice", "Delivery refund with notice"  face nota inversa ponderata la cantitate

delivery_store", "Delivery from store"
delivery_refund_store", "Delivery refund in store"  face nota inversa ponderata la cantitate

delivery_store_notice", "Delivery from store with notice"
delivery_refund_store_notice", "Delivery refund in store with notice" face nota inversa ponderata la cantitate

consume", darea in folosinta # cheltuiala = stock_valuation & 8035=8035
            
inventory_plus", # cont stoc la cont de cheltuiala  # 758800 Alte venituri din exploatare ;  
                60X Cheltuieli privind stocurile    =    30X, 37X Conturi de stocuri    -Valoarea plusului
    *varianta aleasa         30X, 37X Conturi de stocuri    =    758 Alte venituri din exploatare    Valoarea plusului venitul este impozabil
inventory_plus_store", "Inventory plus in store"
inventory_minus",   # cont de cheltuiala la cont de stoc # 758800 Alte venituri din exploatare
inventory_minus_store", "Inventory minus in store"
            
production", "Reception from production" 345" Produse finite" =711 "Venituri aferente costurilor stocurilor de produse"
            
transfer", "Transfer"
transfer_store", "Transfer in Store"
transfer_in", "Transfer in"
transfer_out", "Transfer out"
            
consume_store", "Consume from Store"
production_store", "Reception in store from production"
""",
        default="")

#     def _action_cancel(self):  
#         """ # IS THIS NECESARY? WITHOUT IT IS NOT FUNCTIONING?  
#      I think that you do not have invoice notes before the move is done. 
#      if is done you can not cancel it 
#         """
#         for move in self:
#             if move.account_move_ids:
#                 move.account_move_ids.button_cancel()
#                 move.account_move_ids.unlink()
#         return super()._action_cancel()

#     def _is_out(self):
#         """override to make accounting moves also for internal-production = consume"""
#         self.ensure_one()
#         if  self.env.company.chart_template_id.id == self.env['ir.model.data'].get_object_reference('l10n_ro','ro_chart_template')[1] and \
#             not self.origin_returned_move_id and self.location_id.usage == "internal" and self.location_dest_id.usage == "production":
#             return True
#         return super()._is_out()

##################### generare note contabile suplimentare pentru micarea de stoc################################################################
##################### generare note contabile suplimentare pentru micarea de stoc################################################################
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

        company_from = self._is_out() and self.mapped('move_line_ids.location_id.company_id') or False
        company_to = self._is_in() and self.mapped('move_line_ids.location_dest_id.company_id') or False

        if self.origin_returned_move_id:     ############# is a refund   ############# is a refund  ############# is a refund ############# is a refund 
            _logger.info(f"is a returned move of this move {self.origin_returned_move_id}")
            if location_from.usage == "internal" and location_to.usage == "supplier":
                stock_move_type += "_reception_refund"
                if notice or store:
                    _logger.info( 'refund reception notice or store reversing accounting entries')
                    original_accounting_move = self.env['account.move'].search([('state','=','posted'),('stock_move_id','=', self.origin_returned_move_id.id)])
                    refund_accounting_values = {'stock_move_id':self.id, 'journal_id':original_accounting_move.journal_id.id}
                    if self.origin_returned_move_id.product_qty != -1 * qty:  # partial refund, we must modify the accounting move lines
                        orig_acc_lines = original_accounting_move.with_context(include_business_fields=True).copy_data()[0]['line_ids']
                        for orig_acc_line in orig_acc_lines :
                            orig_acc_line[2]['quantity'] = qty
                            orig_acc_line[2]['debit'] *= -1*qty/self.origin_returned_move_id.product_qty 
                            orig_acc_line[2]['credit'] *= -1*qty/self.origin_returned_move_id.product_qty
                        refund_accounting_values['line_ids'] = orig_acc_lines
                    reversed_account_move = original_accounting_move._reverse_moves(default_values_list=[refund_accounting_values])
                     # here i must change qty ..
                    reversed_account_move.post()
                else:
                    _logger.info('refund reception no accounting entries because no accounting entries were done')
            elif location_from.usage == "customer" and location_to.usage == "internal":
                stock_move_type += "_delivery_refund"
                if notice:
                    _logger.info("refund delivery with notice/aviz   reversed accouting entries")
                    self._create_account_delivery_14( qty=qty ,description=description, svl_id=svl_id, cost=cost, refund=True)
                elif store:
                    _logger.info("refund store delivery with notice/aviz reversed accountinf entries")
                else:
                    _logger.info('refund delivery NO accounting entries ')
                    
        elif location_from.usage == "supplier":  ############### is NOT refund 
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
                    _logger.info(f"Nici o nota contabila pe receptie pt ca e in factura 371+4426 = 401")
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
                    #?????
                    self._create_account_delivery_from_store(refund="refund" in stock_move_type, qty=qty ,description=description, svl_id=svl_id, cost=cost)
                else:
                    self.stock_move_type = stock_move_type
                    _logger.info(f"Nici o nota contabila delivery pt ca e in factura 371+4426 = 401")
                    return
#                     self._valid_only_if_dif_credit_debit_account
#                     self._create_account_delivery_14( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                
            elif location_to.usage == "production":
                stock_move_type += "_consume"
                self._create_consume(qty=qty ,description=description, svl_id=svl_id, cost=cost)
                 
            elif location_to.usage == "inventory":
                stock_move_type += "inventory_minus"
                self._create_inventory_minus( qty=qty ,description=description, svl_id=svl_id, cost=cost)

            
            elif location_to.usage == "internal":
                stock_move_type += "_transfer"
                self._create_account_transfer(qty=qty ,description=description, svl_id=svl_id, cost=cost)
                _logger.info(f"Nota contabila tranfser")
                
            elif location_to.usage == "transit":
                #Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations
                if ( self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id ):
                    stock_move_type += "_delivery"      ##############  delivery  
                    if store:
                        # la livrarea din magazin se va folosi contrul specificat in locatie!
                        if  self.location_id.valuation_out_account_id:  
                            # produsele sunt evaluate dupa contrul de evaluare din locatie
                            acc_valuation = self.location_id.valuation_out_account_id
                        
                else:
                    stock_move_type += "_transit_out"
                    self._create_account_transit_out( qty=qty ,description=description, svl_id=svl_id, cost=cost)

        elif location_from.usage == "inventory":
            if location_to.usage == "internal":
                stock_move_type += "_inventory_plus"
                if store:
                    if self.location_dest_id.valuation_in_account_id:
                        acc_valuation = self.location_dest_id.valuation_in_account_id
                    if self.location_dest_id.property_account_expense_location_id:
                        acc_dest = self.location_dest_id.property_account_expense_location_id
                        acc_src = acc_dest
                else:
                    self._create_inventory_plus( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                    
                
        elif location_from.usage == "production":
            if  location_to.usage == "internal":
                 stock_move_type += "_production"
                 self._create_production( qty=qty ,description=description, svl_id=svl_id, cost=cost)
                 
        elif location_from.usage == "transit":
            if location_to.usage == "internal":
                if self.picking_id.partner_id.commercial_partner_id != self.company_id.partner_id:
                    stock_move_type += "_reception"
                else:
                    stock_move_type += "_transit_in"
                    self._create_account_transit_out( qty=qty ,description=description, svl_id=svl_id, cost=cost)
        
        if stock_move_type == stock_move_type_initial:
            raise UserError(f"Something is wrong at creating stock_move account entries.\nUnknown operation for location_from={location_from.complete_name} location_to={location_to.complete_name};\nlocation_from.usage={location_from.usage} location_to.usage={location_to.usage} ")
        self.stock_move_type = stock_move_type
        return

    def _create_account_move_lineS(self, parameters):#  0credit_account_id, 1debit_account_id, 2journal_id, 3qty, 4description, 5svl_id, 6cost
        "original from stock_account.stock_move.py._create_account_move_line; but this is can create more move_lines"
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

    def _create_production(self, qty ,description, svl_id, cost, refund=False):
        """345 Produse finite" =711 Venituri aferente costurilor stocurilor de produse """
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_src = accounts_data['income'].id
        acc_dest = accounts_data['stock_valuation'].id
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines function in 
        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])


    def _create_consume(self, qty ,description, svl_id, cost, refund=False):
        """Darea in folosinta:
        603    Ch. privind materialele de natura ob. de inventar    =    303    Materiale de natura ob.de inventar    1,700
        c) Concomitent, sumele se pot inregistra extracontabil in contul 8035 Stocuri de natura obiectelor de inventar date în folosinta.
        8035 Stocuri de natura obiectelor de inventar date în folosinta 1,700 """
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_src = accounts_data['expense'].id
        acc_dest = accounts_data['stock_valuation'].id
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines function in 
        acc_src1 = acc_dest2 = self.company_id.property_stock_usage_giving_account_id.id
        if not acc_src1:
            raise UserError(f"Something is wrong at creating consume(darea in folosinta) stock_move account entries.\nYou have not selected a property_stock_picking_payable_account_id in settings on compnay.\n select 8035. ")
        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost),
        #  (acc_src1, acc_dest2, journal_id,qty, description, svl_id, cost)  # error If you want to use "Off-Balance Sheet" accounts. so we are going to do 2 account_moves
                                         ])
        self._create_account_move_lineS([(acc_src1, acc_dest2, journal_id,qty, description, svl_id, cost)])


    def _create_inventory_plus(self, qty ,description, svl_id, cost, refund=False):
        """     60X Cheltuieli privind stocurile    =    30X, 37X Conturi de stocuri    -Valoarea plusului
       varianta aleasa *        30X, 37X Conturi de stocuri    =    758 Alte venituri din exploatare    Valoarea plusului venitul este impozabil """
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data["stock_valuation"].id
        
        if self.location_id.valuation_out_account_id:
            acc_src = self.location_id.valuation_out_account_id.id
        else:
            raise UserError(f"Something is wrong at creating inventory_plus stock_move account entries.\nYou have not selected a valuation_out_account_id for location {self.location_id.complete_name}.\n Use account 7588. ")
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines function in 
        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])
                    
    def _create_inventory_minus(self, qty ,description, svl_id, cost, refund=False):
        """-    Inregistrare minus de inventar:
 * varianta aleasa       607 "Cheltuieli privind marfurile" =    371 "Marfuri" cu minusul constatat la valoarea de inventar
        
         - Colectare TVA aferenta valorii de inventar a marfurilor constatate in minus la inventar:
        635 "Cheltuieli cu alte impozite, taxe si varsaminte asimilate" =    4427 "TVA colectata" cu TVA aferenta
         
        Daca minusul de inventar este imputabil veti inregistra:
         
        -    Inregistarare minus de inventar:
        607 "Cheltuieli privind marfurile" =    371 "Marfuri" cu minusul constatat la valoarea de inlocuire
         
        - Imputarea stocului de produse disparut la valoarea de inlocuire:
        461 "Debitori diversi"       =          %
                                            7581 "Venituri din despagubiri, amenzi si penalitati"
                                            4427 "TVA colectata"
        
        """
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data["stock_valuation"].id
        
        if self.location_dest_id.valuation_in_account_id:
            acc_src = self.location_dest_id.valuation_in_account_id.id
        else:
            raise UserError(f"Something is wrong at creating inventory_minus stock_move account entries.\nYou have not selected a valuation_in_account_id for location {self.location_dest_id.complete_name}.\n Use account 607. ")
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines function in 
        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])

    
    def _create_account_delivery_14(self, qty ,description, svl_id, cost, refund=False):
        """  # Create account moves for deliveries with notice (e.g. 418 = 707)"""
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_src = self.company_id.property_stock_picking_receivable_account_id.id
        acc_dest = accounts_data['stock_valuation'].id
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines function in 
        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])

    def _create_account_reception_14(self, qty ,description, svl_id, cost,refund=False):
        "Primirea marfurilor pe baza de aviz de insotire: ex 371 = 408    "
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = accounts_data['stock_valuation'].id  
        acc_src = self.company_id.property_stock_picking_payable_account_id.id
        
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id

        self._create_account_move_lineS([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])
    
    
    
    
    
    
    ##################################Old functions to delete
    ##################################Old functions to delete
     ##################################Old functions to delete
      ##################################Old functions to delete 
    
    
    
    def _create_account_transit_out(self, qty ,description, svl_id, cost):
        "trasit_out   "
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        stock_transfer_account = move.company_id.property_stock_transfer_account_id 
        acc_dest = stock_transfer_account.id  
        acc_src = accounts_data['stock_valuation']
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines
        self._create_account_move_line([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])
    
    def _create_account_transit_in(self, qty ,description, svl_id, cost):
        "trasit_in     "
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        stock_transfer_account = move.company_id.property_stock_transfer_account_id 
        acc_src = stock_transfer_account.id  
        acc_dst = accounts_data['stock_valuation']
        self._valid_only_if_dif_credit_debit_account(acc_src, acc_dest)
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines
        self._create_account_move_line([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])
    
    def _create_account_transfer(self, qty ,description, svl_id, cost):
        """transfer   permit_same_account=True     
 O societate poate avea magazine diferite, evidentiate in contabilitate ca analitice diferite. 
 Transferul de la un magazin la altul se face cu notele contabile :
–iesirea din magazinul X:
                                 %                            =       371 Marfuri/analitic X
378 Diferente de pret la marfuri /analitic X
4428 TVA neexigibila /analitic X

– intrarea in magazinul Y:
 371 Marfuri/analytic  Y                  =                    %
                                                                  378 Diferente de pret la marfuri/analitic Y
                                                                4428 TVA neexigibila/analitic Y"""
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        stock_transfer_account = move.company_id.property_stock_transfer_account_id 
        acc_src = stock_transfer_account.id  
        acc_dst = accounts_data['stock_valuation']
        journal_id = accounts_data['stock_journal'].id
        # is creating a account_move type entry and  corresponding account_move_lines
        self._create_account_move_line([(acc_src, acc_dest, journal_id,qty, description, svl_id, cost)])
    
    
    def _create_account_reception_in_store_14(self, qty ,description, svl_id, cost, refund=False):
        '''
        Receptions in location with inventory kept at list price
        Create account move with the price difference one (3x8) to suit move: 3xx = 3x8
        Create account move with the uneligible vat one (442810) to suit move: 3xx = 442810
https://www.contzilla.ro/monografii-contabile-pentru-activitatea-unui-magazin-comert-cu-amanuntul/
b) Calcularea si inregistrarea diferentelor de pret la marfuri

Datorita faptului ca pentru evidentierea in contabilitate a marfurilor entitatea utilizeaza pretul cu amanuntul, ulterior inregistrarii stocurilor la cost de achizitie, se calculeaza si se inregistreaza diferentele de pret care vin sa corecteze valoarea de achizitie pana la nivelul pretului de vanzare cu amanuntul, astfel:

Adaosul comercial = 30% * pretul de achizitie = 30% * 100.000 lei = 30.000 lei

Tva neexigibila = ( cost de achizitie + adaos comercial) * 19 % = (100.000 lei +30.000 lei )*19 % = 24.700 lei

Pentru a se obtine pretul de vanzare cu amanuntul se utilizeaza urmatoarea formula:

Capture

***) Tva –ul se reflecta in pretul de vanzare cu amanuntul insa devine exigibil numai cand se realizeaza vanzarea marfurilor . Pana la acel moment se reflecta in contul 4428 Tva neexigibil, dupa care se reflecta in contul 4427 Tva colectata.

Prin urmare, pretul de vanzare cu amanuntul = 100.000 lei + 30.000 lei + 24.700 lei = 154.700 lei

Notele contabile prin care se reflecta in contabilitate diferentele de pret sunt :

371 Marfuri            =                             %                                              54.700

                                             378 Diferente de pret la marfuri           30.000

                                             4428 Tva neexigibila                                24.700
        '''   
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        acc_dest = self.location_dest_id.valuation_in_account_id.id or accounts_data["stock_valuation"]
        journal_id = accounts_data['stock_journal'].id
 
        if self.location_dest_id.valuation_in_account_id:
            acc_dest = self.location_dest_id.valuation_in_account_id.id
        else:
            if self.location_id.valuation_out_account_id:
                acc_dest = self.location_id.valuation_out_account_id.id
            else:
                acc_dest = accounts_data['stock_input'] 
 
        acc_src = move.location_dest_id.property_account_creditor_price_difference_location_id or self.product_id.property_account_creditor_price_difference or  self.product_id.categ_id.property_account_creditor_price_difference_categ
        if not acc_src:
            raise UserError(_(
                'Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
        
        taxes_ids = move.product_id.taxes_id.filtered(lambda r: r.company_id == self.company_id)
 
        list_price = move.product_id.list_price or 0.00
        if taxes_ids:
            taxes = taxes_ids.compute_all(list_price, product=move.product_id)
            list_price = taxes['total_excluded']

        if list_price <= cost and list_price != 0.0:
            raise UserError(_( "You cannot move a product if price list is lower than cost price. Please update list price to suit to be higher than %s" % cost))

        # the standard_price of the product may be in another decimal precision, or not compatible with the coinage of
        # the company currency... so we need to use round() before  creating the accounting entries.
        stock_value = self.company_id.currency_id.round(cost_price * abs(qty))
        valuation_amount = list_price * abs(qty) - stock_value
        uneligible_tax = 0

        if taxes_ids:
            # tva la valoarea de vanzare
            taxes = taxes_ids.compute_all(self.product_id.list_price, product=self.product_id, quantity=abs(qty))
            round_diff = taxes['total_excluded'] - valuation_amount - stock_value
            uneligible_tax = taxes['total_included'] - taxes['total_excluded'] + round_diff

        self = move.with_context(force_valuation_amount=valuation_amount, forced_quantity=0.0)
        if refund:
            acc_src, acc_dest = acc_dest, acc_src

        self._create_account_move_line(acc_src, acc_dest, journal_id,qty, description=description, svl_id=svl_id, cost=cost)
 
 
 
 # I think that are ok
    def _create_account_inventory_plus_in_store(self, qty, description, svl_id, cost):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store(refund=False,qty=qty, description=description, svl_id=svl_id, cost=cost)

    def _create_account_inventory_minus_in_store(self,qty, description, svl_id, cost):
        # inregistrare diferenta de pret
        # inregistrare taxa neexigibila
        self._create_account_reception_in_store(refund=True, qty=qty, description=description, svl_id=svl_id, cost=cost)



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
        