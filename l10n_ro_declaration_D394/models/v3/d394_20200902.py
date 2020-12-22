# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import re
import datetime
from collections import defaultdict
from odoo import fields, models


_logger = logging.getLogger(__name__)
dict_tags = {
             '11_1 - TVA': [5, "L", "TVA"],
             '11_1 - BAZA': (5, "L", "BAZA", '11_1 - TVA'),
             '09_1 - BAZA': (19, "L", "BAZA",'09_1 - TVA'),
             '09_1 - TVA': (19, "L", "TVA",'09_1 - BAZA'),
             '09_2 - BAZA': (19, "A", "BAZA",'09_2 - TVA',"%50?"),
             '09_2 - TVA': (19, "A", "TVA",'09_2 - BAZA',"%50?"),
             '10_1 - TVA': (9, "LS", "TVA",'10_1 - BAZA'),
             '10_1 - BAZA': (9, "LS", "BAZA",'10_1 - TVA'),
             '10_2 - TVA':(9, "A", "TVA",'10_2 - BAZA',"%50?"),
             '10_2 - BAZA':(9, "A", "BAZA",'10_2 - TVA',"%50?"),
             '11_1 - BAZA':(5, "LS", "BAZA", '11_1 - TVA'),
             '11_1 - TVA':(5, "LS", "TVA",'09_1 - BAZA'),
             '11_2 - TVA':(5, "A", "TVA",'11_2 - BAZA'),
             '12_1 - BAZA':(19, "V", "BAZA", '12_1 - TVA'),
             '12_1 - TVA':(19, "V", "BAZA", '12_1 - BAZA'),
             '12_2 - BAZA':(9, "V", "BAZA", '12_2 - TVA'),
             '12_2 - TVA':(9, "V", "TVA",'12_2 - BAZA'),
             '12_3 - BAZA':(5, "AS", "BAZA", '12_3 - TVA'),
             '12_3 - TVA':(5, "AS", "TVA",'12_3 - BAZA'),
              '01 - BAZA': (5, "A", "TVA",'01 - BAZA'),
              '01 - TVA': (5, "A", "TVA",'01 - BAZA'),
              '03 - TVA': (5, "A", "TVA",'01 - BAZA'),
              '03 - BAZA': (5, "A", "TVA",'01 - BAZA'),
              '05 - BAZA': (19, "L", "BAZA",'05 - TVA'),
              '05 - TVA': (19, "L", "TVA",'05 - BAZA'),
              '05_1 - BAZA': (9, "AS", "BAZA",'09_1 - TVA'),
              '05_1 - TVA' : (9, "AS", "TVA",'09_1 - BAZA'),
              '06 - BAZA' : (19, "L", "BAZA",'06 - TVA'),
              '06 - TVA'  : (19, "L", "TVA",'06 - BAZA'),
              '07 - BAZA' : (9, "AS", "BAZA",'07 - TVA'),
              '07 - TVA' : (9, "AS", "TVA",'07 - BAZA'),
              '07_1 - BAZA' : (9, "AS","BAZA",'07_1 - TVA'),
              '07_1 - TVA' : (9, "AS", "TVA",'07_1 - BAZA'),
             '08 - BAZA' : (19, "L", "BAZA",'08 - TVA'),
             '08 - TVA' : (19, "L", "TVA",'08 - BAZA'),
             '09 - BAZA' : (19, "L", "BAZA",'09 - TVA'),
             '09 - TVA' : (19, "L", "TVA",'09 - BAZA'),
             '10 - BAZA' : (19, "L", "BAZA",'10 - TVA'),
             '10 - TVA' : (19, "L", "TVA",'10 - BAZA'),
             '10_1 - BAZA' : (19, "L","BAZA",'10_1 - TVA'),
             '10_1 - TVA' : (19, "L", "TVA",'10_1 - BAZA'),
             '10_2 - BAZA' : (19, "L", "BAZA",'10_2 - TVA'),
             '10_2 - TVA' : (19, "L", "TVA",'10_2 - BAZA'),
             '13 - BAZA' : (0, "V", "BAZA",''),
             '14 - BAZA' : (0, "LS", "BAZA",''),
             '15 - BAZA' : (0, "LS", "BAZA",''),
             '16 - BAZA' : (19, "L", "BAZA",'16 - TVA'),
             '16 - TVA' : (19, "L", "TVA",'16 - BAZA'),
             '17 - BAZA' : (19, "L", "BAZA",'17 - BAZA'),
             '17 - TVA' : (19, "L", "TVA",'17 - BAZA'),
             '18 - BAZA' : (19, "L", "BAZA",'18 - TVA'),
             '18 - TVA' : (19, "L", "TVA",'18 - BAZA'),
             '20 - BAZA' : (19, "AS", "BAZA",'20 - TVA'),
             '20 - TVA' : (19, "AS", "TVA",'20 - BAZA'),
             '20_1 - BAZA' : (19, "L", "BAZA",'20_1 - TVA'),
             '20_1 - TVA' : (19, "L", "TVA",'20_1 - BAZA'),
             '21 - BAZA' : (19, "L", "BAZA",'21 - TVA'),
             '21 - TVA' : (19, "L", "TVA",'21 - BAZA'),
             '22 - BAZA' : (19, "AS", "BAZA",'22 - TVA'),
             '22 - TVA' : (19, "AS", "TVA",'22 - BAZA'),
             '22_1 - BAZA' : (19, "AS", "BAZA",'22_1 - TVA'),
             '22_1 - TVA' : (19, "AS", "TVA",'22_1 - BAZA'),
             '23 - BAZA' : (19, "L", "BAZA",'23 - TVA'),
             '23 - TVA' : (19, "L", "TVA",'23 - BAZA'),
             '24 - BAZA' : (19, "L", "BAZA",'24 - TVA'),
             '24 - TVA' : (19, "L", "TVA",'24 - BAZA'),
             '24.1 - BAZA' : (19, "A", "BAZA",'24_1 - TVA'),
             '24_1 - BAZA' : (19, "A", "BAZA",'24_1 - TVA'),
             '24_1 - TVA' : (19, "L", "TVA",'24_1 - BAZA'),
             '24_2 - BAZA' : (19, "L", "BAZA",'24_2 - TVA'),
             '24_2 - TVA' : (19, "L", "TVA",'24_2 - BAZA'),
             '25 - BAZA' : (19, "L", "BAZA",'25 - TVA'),
             '25 - TVA' : (19, "L", "TVA",'25 - BAZA'),
             '25_1 - BAZA' : (9, "AS", "BAZA",'25_1 - TVA'),
             '25_1 - TVA' : (9, "AS", "TVA",'25_1 - BAZA'),
             '25_2 - BAZA' : (19, "L", "BAZA",'25_2 - TVA'),
             '25_2 - TVA' : (19, "L", "TVA",'25_2 - BAZA'),
             '26 - BAZA' : (19, "L", "BAZA",'26 - TVA'),
             '26 - TVA' : (19, "L", "TVA",'26 - BAZA'),
             '26_1 - BAZA' : (5, "AS", "BAZA",'26_1 - TVA'),
             '26_1 - TVA' : (5, "AS", "TVA",'26_1 - BAZA'),
             '26_2 - BAZA' : (19, "L", "BAZA",'26_2 - TVA'),
             '26_2 - TVA' : (19, "L", "TVA",'26_2 - BAZA'),
             '27 - BAZA' : (19, "L", "BAZA",'27 - TVA'),
             '27 - TVA' : (19, "L", "TVA",'27 - BAZA'),
             '27_1 - BAZA' : (19, "V", "BAZA",'27_1 - TVA'),
             '27_1 - TVA' : (19, "V", "TVA",'27_1 - BAZA'),
             '27_2 - BAZA' : (9, "V", "BAZA",'27_2 - TVA'),
             '27_2 - TVA' : (9, "V", "TVA",'27_2 - BAZA'),
             '27_3 - BAZA' : (19, "L", "BAZA",'27_3 - TVA'),
             '27_3 - TVA' : (19, "L", "TVA",'27_3 - BAZA'),
             '28 - TVA' : (19, "L", "TVA",''),
             '29 - TVA' : (19, "L", "TVA",''),
             '30 - BAZA' : (0, "AS", "BAZA",''),
             '30_1 - BAZA' : (0, "AS", "BAZA",''),
             '33 - TVA' : (19, "L", "TVA",''),
             '34 - BAZA' : (19, "L", "BAZA",'34 - TVA'),
             '34 - TVA' : (19, "L", "TVA",'34 - BAZA'),
             '35 - TVA' : (19, "L", "TVA",'')
              }






class Declaratie394(models.TransientModel):
    _name = "anaf.d394.v30"
    _inherit = "anaf.d394"
    _description = "declaratie 394, v30"

    def build_file(self):
        year, month = self.get_year_month()
        months = self.get_months_number()
        tip_D394 = "L"
        if months == 3:
            tip_D394 = "T"
        elif months == 6:
            tip_D394 = "S"
        elif months == 12:
            tip_D394 = "A"
        obj_invoice = self.env['account.move']

        invoices = obj_invoice.search([
            ('state', 'in', ['posted']),
            ('move_type', '!=', 'out_receipt'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ])


        recipes = obj_invoice.search([
            ('state', 'in', ['posted']),
            ('move_type', '=', 'out_receipt'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ])
        recipes_months = self.get_montly_invoices_by_tags(recipes)
        data_file = """<?xml version="1.0" encoding="UTF-8"?>
            <declaratie394
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="mfp:anaf:dgti:d394:declaratie:v3 D394.xsd"
            xmlns="mfp:anaf:dgti:d394:declaratie:v3"
            """

        op1 = self._get_op1(invoices)
        op2 = []
        for recipes_month in recipes_months:
            op2 += self._get_op2(recipes_month)
        payments = self._get_payments()

        xmldict = {
            "luna": month,
            "an": year,
            "op_efectuate": 1,
            "optiune": int(self.optiune),
            "schimb_optiune": int(self.schimb_optiune),
            "prsAfiliat": int(self.prsAfiliat),
            'informatii':self._generate_informatii(invoices, payments, op1, op2),
            'rezumat1': self._generate_rezumat1(invoices,payments,op1,op2),
            'rezumat2': self._generate_rezumat2(recipes, payments, op1, op2),
            'serieFacturi': self._get_inv_series(invoices),
            'lista': self._generate_lista(),
            'facturi': self.generate_facturi(),
            'op1': op1,
            'op2': op2
        }
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)

        for key, val in xmldict.items():
            if key not in ('informatii', 'rezumat1', 'rezumat2',
                           'serieFacturi', 'lista',
                           'facturi', 'op1', 'op2'):
                data_file += """%s="%s" """ % (key, val)
        data_file += """>"""
        data_file += """
    <informatii """
        for key, val in xmldict['informatii'].items():
            data_file += """%s="%s" """ % (key, val)
        data_file += """
    />"""
        for client in xmldict['rezumat1']:
            data_file += """
    <rezumat1 """
            for key, val in client.items():
                if key != 'detaliu':
                    data_file += """%s="%s" """ % (key, val)
            if client['detaliu']:
                data_file += """>"""
                for line in client['detaliu']:
                    data_file += """
        <detaliu """
                    for det_key, det_val in line.items():
                        data_file += """%s="%s" """ % (det_key, det_val)
                    data_file += """/>"""
                data_file += """
    </rezumat1>"""
            else:
                data_file += """/>"""
        for client in xmldict['rezumat2']:
            data_file += """
    <rezumat2 """
            for key, val in client.items():
                data_file += """%s="%s" """ % (key, val)
            data_file += """/>"""
        for client in xmldict['serieFacturi']:
            data_file += """
    <serieFacturi """
            for key, val in client.items():
                data_file += """%s="%s" """ % (key, val)
            data_file += """/>"""
        for client in xmldict['lista']:
            data_file += """
    <lista """
            for key, val in client.items():
                data_file += """%s="%s" """ % (key, val)
            data_file += """/>"""
        for client in xmldict['facturi']:
            data_file += """
    <facturi """
            for key, val in client.items():
                data_file += """%s="%s" """ % (key, val)
            data_file += """/>"""
        for client in xmldict['op1']:
            data_file += """
    <op1 """
            for key, val in client.items():
                if key != 'op11':
                    data_file += """%s="%s" """ % (key, val)
            if client['op11']:
                data_file += """>"""
                for line in client['op11']:
                    data_file += """<op11 """
                    for key, val in line.items():
                        data_file += """%s="%s" """ % (key, val)
                    data_file += """/>"""
                data_file += """
    </op1>"""
            else:
                data_file += """/>"""
        for client in xmldict['op2']:
            data_file += """
    <op2 """
            for key, val in client.items():
                data_file += """%s="%s" """ % (key, val)
            data_file += """/>"""
        data_file += """
    </declaratie394>"""


        return data_file

    def generate_company_data(self):
        if self.company_id.partner_id.vat_number.find("RO") == 1:
            cui = int(self.company_id.partner_id.vat_number[2:])
        else :
            cui = int(self.company_id.partner_id.vat_number)


        data = {
            "cui": cui,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(
                without_company=True
            ).replace("\n", ","),
            "telefon": self.company_id.phone,
            "mail": self.company_id.email,
            "caen": self.company_id.caen_code,
            "sistemTVA": self.company_id.partner_id.with_context({'check_date': self.date_to})._check_vat_on_payment()
        }
        return data

    def generate_sign(self):
        signer = self.signature_id
        data = {
            "tip_intocmit": 1,
            "den_intocmit": signer.name,
            "Dcif_intocmit": signer.vat
        }
        if signer.type == 'company':
            data.update({"calitate_intocmit": signer.quality})
        else:
            data.update({"functie_intocmit ": signer.function})
        return data

    def generate_facturi(self):
        year, mounth = self.get_year_month()
        obj_invoice = self.env['account.move']
        comp_currency = self.company_id.currency_id
        facturi = []
        invoices1 = obj_invoice.search([
           # ('fiscal_receipt', '=', False),
            ('state', '!=', 'draft'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ])
        invoices = invoices1.filtered(
            lambda r:
            r.amount_total < 0 or r.state == 'cancel' or
            r.sequence_type in ('autoinv1', 'autoinv2'))

        for inv in invoices:

            baza24 = baza20 = baza19 = baza9 = baza5 = 0
            tva24 = tva20 = tva19 = tva9 = tva5 = 0
            inv_curr = inv.currency_id
            inv_date = inv.invoice_date
            inv_type = False
            if inv.move_type in ('out_invoice', 'out_refund'):
                if inv.state == 'cancel':
                    inv_type = 2
                elif inv.amount_total < 0:
                    inv_type = 1
                elif inv.sequence_type == 'autoinv1':
                    inv_type = 3
            elif inv.sequence_type == 'autoinv2':
                inv_type = 4
            if inv_type:
                for line in inv.invoice_line_ids:
                    cotas = [tax for tax in line.tax_line_id]
                    for cota in cotas:
                        cota_amount = 0
                        cota_amount = int(cota.amount)
                        if cota_amount in (5, 9, 19, 20, 24):
                            new_base = inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_subtotal, comp_currency)
                            new_taxes = inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_normal_taxes and
                                line.price_normal_taxes or
                                line.price_taxes, comp_currency)
                            if cota_amount == 24:
                                baza24 += new_base
                                tva24 += new_taxes
                            elif cota_amount == 20:
                                baza20 += new_base
                                tva20 += new_taxes
                            elif cota_amount == 19:
                                baza19 += new_base
                                tva19 += new_taxes
                            elif cota_amount == 9:
                                baza9 += new_base
                                tva9 += new_taxes
                            elif cota_amount == 5:
                                baza5 += new_base
                                tva5 += new_taxes
                new_dict = {
                    'tip_factura': inv_type,
                    'serie': inv.sequence_prefix,
                    'nr': inv.sequence_number,
                }
                if inv_type == 3:
                    new_dict.update({
                        'baza24': int(round(baza24)),
                        'baza20': int(round(baza20)),
                        'baza19': int(round(baza19)),
                        'baza9': int(round(baza9)),
                        'baza5': int(round(baza5)),
                        'tva5': int(round(tva20)),
                        'tva9': int(round(tva9)),
                        'tva19': int(round(tva19)),
                        'tva20': int(round(tva20)),
                        'tva24': int(round(tva24))
                    })
                facturi.append(new_dict)
        return facturi

    def get_months_period(self):
        month_end = fields.Date.from_string(self.date_to).month
        month_star = fields.Date.from_string(self.date_from).month
        year_end = fields.Date.from_string(self.date_to).year
        year_start = fields.Date.from_string(self.date_from).year
        if year_end == year_start:
            months = [(m, year_start) for m in range(month_star, month_end + 1)]
        else:
            months = [(m, year_start) for m in range(month_star, 13)]
            months.extend([(m, year_end) for m in range(1, month_end + 1)])
        return months

    def get_montly_invoices_by_tags(self, invoices):
        invoice_montly = []
        invoices_ids = invoices.mapped('id')
        months_year = self.get_months_period()
        for month, year in months_year:
            invoices = (
                self.env["account.move"]
                    .search(
                    [
                        ("state", "=", "posted"),
                        ("invoice_date", ">=", datetime.datetime(year, month, 1)),
                        ("invoice_date", "<", datetime.datetime(year, month + 1, 1)),
                        ("company_id", "=", self.company_id.id),
                        ("id", "in", invoices_ids),
                    ]))

            invoices.sorted(key=lambda r: r.invoice_date)
            invoice_montly.append(invoices)
        return invoice_montly

    def _get_payments(self):
        invoice_obj = self.env['account.move']

        company = self.company_id
        comp_curr = company.currency_id
        payments = []
        where = [
            ('state', 'in', ['open', 'paid']),
            ('invoice_date', '<=', self.date_to),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ]
        invoices = invoice_obj.search(where,
                                      order="move_type desc, invoice_date")
        for inv1 in invoices:
            ctx = {'date': inv1.invoice_date}
            if inv1.payment_ids:
                for payment in inv1.payment_ids:
                    if payment.date <= self.date_to:
                        pay = {}
                        pay['type'] = inv1.move_type
                        pay['vat_on_payment'] = inv1.vat_on_payment
                        pay['base_24'] = pay['base_20'] = pay['base_19'] = 0.00
                        pay['base_9'] = pay['base_5'] = 0.00
                        pay['tva_24'] = pay['tva_20'] = pay['tva_19'] = 0.00
                        pay['tva_9'] = pay['tva_5'] = 0.00
                        for line in payment.move_id.line_id:
                            if ('4427' in line.account_id.code) or \
                                    ('4426' in line.account_id.code):
                                if line.tax_code_id and \
                                        ' 24' in line.tax_code_id.name:
                                    pay['base_24'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit) / 0.24,
                                                         comp_curr)
                                    pay['tva_24'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit),
                                                         comp_curr)
                                if line.tax_code_id and \
                                        ' 20' in line.tax_code_id.name:
                                    pay['base_20'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit) / 0.20,
                                                         comp_curr)
                                    pay['tva_20'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit),
                                                         comp_curr)
                                if line.tax_code_id and \
                                        ' 19' in line.tax_code_id.name:
                                    pay['base_19'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit) / 0.09,
                                                         comp_curr)
                                    pay['tva_19'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit),
                                                         comp_curr)
                                if line.tax_code_id and \
                                        ' 9' in line.tax_code_id.name:
                                    pay['base_9'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit) / 0.09,
                                                         comp_curr)
                                    pay['tva_9'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit),
                                                         comp_curr)
                                if line.tax_code_id and \
                                        ' 5' in line.tax_code_id.name:
                                    pay['base_5'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit) / 0.05,
                                                         comp_curr)
                                    pay['tva_5'] += \
                                        inv1.currency_id.with_context(
                                            ctx).compute((line.credit or
                                                          line.debit),
                                                         comp_curr)
                        for field in ('base_24', 'base_20', 'base_19',
                                      'base_9', 'base_5',
                                      'tva_24', 'tva_20', 'tva_19',
                                      'tva_9', 'tva_5'):
                            pay[field] = int(round(pay[field]))
                        payments.append(pay)
            _logger.warning("PPPXXXPPPP")
            _logger.warning(payments)
        return payments

    def _get_op1(self, invoices):
        def compute_invoice_taxes_ammount(invoices):
            ''' Helper to get the taxes grouped according their account.tax.group.
            This method is only used when printing the invoice.
            '''
            ress =[]
            for move in invoices:
                lang_env = move.with_context(lang=move.partner_id.lang).env
                tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id)
                tax_balance_multiplicator = -1 if move.is_inbound(True) else 1
                res = {}
                # There are as many tax line as there are repartition lines
                done_taxes = set()
                for line in tax_lines:
                    res.setdefault(line.tax_line_id.tax_group_id, {'base': 0.0, 'amount': 0.0})
                    res[line.tax_line_id.tax_group_id]['amount'] += tax_balance_multiplicator * (
                        line.amount_currency if line.currency_id else line.balance)
                    tax_key_add_base = tuple(move._get_tax_key_for_group_add_base(line))
                    if tax_key_add_base not in done_taxes:
                        if line.currency_id and line.company_currency_id and line.currency_id != line.company_currency_id:
                            amount = line.company_currency_id._convert(line.tax_base_amount, line.currency_id,
                                                                       line.company_id,
                                                                       line.date or fields.Date.context_today(self))
                        else:
                            amount = line.tax_base_amount
                        res[line.tax_line_id.tax_group_id]['base'] += amount
                        # The base should be added ONCE
                        done_taxes.add(tax_key_add_base)

                # At this point we only want to keep the taxes with a zero amount since they do not
                # generate a tax line.
                for line in move.line_ids:
                    for tax in line.tax_ids.flatten_taxes_hierarchy():
                        if tax.tax_group_id not in res:
                            res.setdefault(tax.tax_group_id, {'base': 0.0, 'amount': 0.0})
                            res[tax.tax_group_id]['base'] += tax_balance_multiplicator * (
                                line.amount_currency if line.currency_id else line.balance)
                        re.findall(r'\d+', tax.tax_group_id.name)

                        _logger.warning(int(re.findall(r'\d+', tax.tax_group_id.name)[0]))

                res = sorted(res.items(), key=lambda l: l[0].sequence)
                if len(ress) == 0:
                    ress = res
                else:
                    for group in res:
                        found = False
                        for group_f in ress :
                            if group_f[0] == group[0]:
                                group_f[1]['base'] += group[1]['base']
                                group_f[1]['amount'] += group[1]['amount']
                                found = True
                        if not found:
                            ress.append(group)

                _logger.warning(res)
            _logger.warning(ress)
            return ress

        def _get_op11(invoices,partner_type,new_oper_type,cota, comp_curr ):
            op11_dicts =[]
            inv_lines =[]
            for inv in invoices :
                if inv.invoice_line_ids:
                     inv_lines.append(inv.invoice_line_ids)
                     _logger.warning("OP11OP11OPPPPPPPP11111")
                     _logger.warning(inv.invoice_line_ids.product_id)
            codes = inv.invoice_line_ids.mapped('product_id.anaf_code_id')
            _logger.warning(new_oper_type)
            _logger.warning(inv_lines)
            if (partner_type == '1' and new_oper_type in ('V', 'C'))\
            or (partner_type == '2' and new_oper_type == 'N'):
                _logger.warning(codes)

                for code in codes:
                    new_code = code
                    if code.parent_id:
                        new_code = code.parent_id
                        cod_lines = []
                        if partner_type == '1':
                            cod_lines = list(filter(lambda r: r.product_id.anaf_code_id == code and\
                                                              int(new_code.name) <= 31, inv_lines))
                        else:
                            cod_lines = list(filter(lambda r:r.product_id.anaf_code_id == code,inv_lines))
                    _logger.warning("NFACT_OP11")
                    _logger.warning(cod_lines)
                    if cod_lines:
                        nrFact = len(set(list(filter(lambda r: r.product_id.anaf_code_id == code,inv_lines))))
                        _logger.warning("NFACT_OP11")
                        _logger.warning(nrFact)
                        baza1 = 0
                        taxes1 = 0
                        for line in cod_lines:
                            inv_curr = line.move_id.currency_id
                            inv_date = line.move_id.invoice_date
                            baza1 += inv_curr.with_context({'date': inv_date})._convert(line.price_subtotal,\
                                                       comp_curr,line.company_id,inv_date)
                            new_taxes = inv_curr.with_context( {'date': inv_date})._convert(line.tax_base_amount,
                                                       comp_curr,line.company_id,inv_date)
                            if new_oper_type == 'C':
                                taxes1 += new_taxes
                        op11_dict = { 'codPR': code.name,
                                      'nrFactPR': nrFact,
                                      'bazaPR': int(round(baza1))
                                               }
                        if new_oper_type in ( 'A', 'L', 'C', 'AI'):
                                op11_dict['tvaPR'] = int(round(taxes1))

                        op11_dicts.append(op11_dict)

            return op11_dicts


        def _get_operation_type(invoices):
            ### Is used to determine the type of operation.
            ###   Input: more invoices
            ###   Return: a dictionary keys operation type and values are invoice lines for this operation type


            operation_type = {'A':[],
                              'L':[],
                              'C':[],
                              'V':[],
                              'AI':[],
                              'LS':[],
                              'AS':[],
                              'ASI':[],
                              'N':[]
                              }

            mv_line_obj = self.env["account.move.line"]
            invoices_id = []
            for invoice in invoices :
                #_logger.warning('Position Fiscal')
                #_logger.warning(invoice.name)
                #_logger.warning(invoice.fiscal_position_id.name)
                if invoice.fiscal_position_id.name =="Regim TVA la Incasare":
                    domain = [ ("move_id.id","=",invoice.id),
                                ("tax_exigible", "=", True),
                                ("tax_tag_ids", "!=", False),
                                ("move_id.state", "=", "posted"),
                            ]
                    move_lines = mv_line_obj.search(domain)
                    for record in move_lines:
                        operation_type["AI"].append(record)
                else:
                    invoices_id.append(invoice.id)

            domain = [("move_id.id","in",invoices_id),
                        ("tax_exigible", "=", True),
                        ("tax_tag_ids", "!=", False),
                        ("move_id.state", "=", "posted"),
                    ]

            move_lines = mv_line_obj.search(domain)
            for record in move_lines:
                for tag in record.tax_tag_ids:
                    tag_name = tag.name[1:]
                    type = dict_tags[tag_name][1]
                    if type in ["A","C","AS"] and record.move_id.partner_type == "2" :
                        operation_type["N"].append(record)
                    operation_type[type].append(record)
            #_logger.warning('Move Linesssss')
            #_logger.warning(operation_type)
            return operation_type

        def _get_vat_line(tax_move_lines):
            # Input lines invoices
            # Return dict whit key tags and the amount on the tag  and a dict  key tags and value a list of invoice number



            mv_line_obj = self.env["account.move.line"]
            vat_report = {}
            invoices_number = {}
            for record in tax_move_lines:

                for tag in record.tax_tag_ids:

                    if record.move_id.tax_cash_basis_rec_id:
                        # Cash basis entries are always treated as misc operations, applying the tag sign directly to the balance
                        type_multiplicator = 1
                        if record.tax_ids and record.tax_ids[0].type_tax_use == "sale":
                            type_multiplicator = -1
                    else:
                        type_multiplicator = (
                            record.journal_id.type == "sale" and -1 or 1
                        ) * (
                            mv_line_obj._get_refund_tax_audit_condition(record) and -1 or 1
                        )

                    tag_amount = type_multiplicator * record.balance
                    if tag.tax_report_line_ids:
                        # Then, the tag comes from a report line, and hence has a + or - sign (also in its name)
                        for report_line in tag.tax_report_line_ids:
                            tag_id = report_line.tag_name
                            if tag_id not in vat_report.keys():
                                vat_report[tag_id] = 0.0
                                invoices_number[tag_id] = []
                            vat_report[tag_id] += tag_amount
                            invoices_number[tag_id].append(record.move_id)
                    else:
                        # Then, it's a financial tag (sign is always +, and never shown in tag name)
                        tag_id = tag.name
                        if tag_id not in vat_report.keys():
                            vat_report[tag_id] = 0.0
                            invoices_number[tag_id] = []
                        vat_report[tag_id] += tag_amount
                        invoices_number[tag_id].append(record.move_id)

            return vat_report, invoices_number



        def _get_vat_data(part_invoices, partner, partner_type, doc_type) :
            denP = partner.name.replace('&', '-').replace('"', '')
            #  operation type
            line = _get_operation_type(part_invoices)
            res_dict =[]
            for oper_type,move_lines in line.items():

                if len(move_lines) > 0:


                    tags_line = _get_vat_line(move_lines)[0]
                    invoices_number = _get_vat_line(move_lines)[1]
                    _logger.warning("OOOOOOoooo0000")
                    _logger.warning(tags_line)
                    _logger.warning(oper_type)
                    _logger.warning(invoices_number)
                    # base_cota , tva_cota , invoices_number dicts it is used  for sort on cota TVA
                    base_cota = {}
                    tva_cota = {}
                    invoices_number_dict = {}
                    for key in tags_line.keys():
                        _logger.warning(key)

                        if dict_tags[key][2] == 'BAZA':
                            cota = dict_tags[key][0]
                            new_key = dict_tags[key][3]
                            if cota in base_cota.keys():
                                base_cota[cota] += tags_line[key]
                            else :
                                base_cota.update({cota:tags_line[key]})

                            if cota in tva_cota.keys():
                                 if new_key in tags_line.keys():
                                     tva_cota[cota] += tags_line[new_key]
                                 else:
                                      _logger.warning("{} key not found".format(new_key))
                            else:
                                 if new_key in tags_line.keys():
                                    tva_cota.update({cota:tags_line[new_key]})
                                 else:
                                    _logger.warning("{} key not found".format(new_key))
                                    tva_cota.update({cota:0 })

                            if cota in invoices_number_dict.keys():
                                invoices_number_dict[cota] += invoices_number[key]
                            else :
                                invoices_number_dict.update({cota:invoices_number[key]})

                           # _logger.warning(base_cota)
                           # _logger.warning(tva_cota)
                    for cota in base_cota.keys():
                        new_dict = {
                                'tip': oper_type,
                                'tip_partener': partner_type,
                                'cota': cota,
                                'denP': denP,
                                'nrFact': len(set(invoices_number_dict[cota])),
                                'baza': int(round(base_cota[cota])),
                                'tva' : int(round(tva_cota[cota])),
                                'tip_document': doc_type,
                                'op11': _get_op11(set(invoices_number_dict[cota]),partner_type,oper_type,cota,comp_curr)
                                }
                        if partner_type == '1':
                                new_dict['cuiP'] = partner._split_vat(partner.vat)[1]
                        elif partner_type == '2':
                            if partner.vat:
                                new_dict['cuiP'] = partner._split_vat(partner.vat)[1]
                            else :
                                    if partner.country_id:
                                        new_dict['taraP'] = \
                                        partner.country_id and \
                                        partner.country_id.code.upper()
                                    if partner.city:
                                        new_dict['locP'] = \
                                        partner.city

                                    if partner.state_id:
                                        new_dict['judP'] = \
                                        partner.state_id and \
                                        partner.state_id.order_code
                                    if partner.street:
                                        new_dict['strP'] = \
                                        partner.street
                                    if partner.street2:
                                        new_dict['strP'] += partner.street2
                                    if partner.street2:
                                        new_dict['detP'] = \
                                        partner.street2 and \
                                        partner.street2
                        else:
                            new_dict['cuiP'] = partner._split_vat(partner.vat)[1]

                        res_dict.append(new_dict)
                        #_logger.warning(new_dict)
            return res_dict

        def adauga_op1(op1, new):
            if op1:
                try:
                    found = next(
                        index for (index, old) in enumerate(op1) if
                        old.get('tip') == new['tip'] and
                        old.get('tip_partener') == new['tip_partener'] and
                        old.get('cota') == new['cota'] and
                        old.get('cuiP') == new['cuiP'])
                except:
                    found = None
                if found is not None:
                    old = op1[found]
                    old['nrFact'] += new['nrFact']
                    old['baza'] += new['baza']
                    if 'tva' in old.keys():
                        old['tva'] += new['tva']
                    if new['op11']:
                        if old['op11']:
                            for new11 in new['op11']:
                                try:
                                    found11 = next(
                                        index for (index, old11)
                                        in enumerate(old['op11']) if
                                        old11.get('codPR') == new11['codPR'])
                                except:
                                    found11 = None
                                if found11 is not None:
                                    old11 = old['op11'][found11]
                                    old11['nrFactPR'] += new11['nrFactPR']
                                    old11['bazaPR'] += new11['bazaPR']
                                    if 'tvaPR' in old11.keys():
                                        old11['tvaPR'] += new11['tvaPR']
                                else:
                                    old['op11'].append(new11)
                        else:
                            old['op11'].append(new['op11'])
                else:
                    op1.append(new)
            else:
                op1.append(new)
            return op1

        self.ensure_one()
        obj_inv_line = self.env['account.move.line']
        obj_partner = self.env['res.partner']
        obj_tax = self.env['account.tax']

        anaf = self.env["l10n.ro.account.report.journal"]

        comp_curr = self.company_id.currency_id
        op1 = []
        _logger.warning("Partener Oper Type ")
        partner_types = set([invoice.partner_type for invoice in invoices])
        _logger.warning(partner_types)
        for partner_type in partner_types:
            part_types_inv= invoices.filtered(
                lambda r: r.partner_type == partner_type)
            #_logger.warning("Partener Oper Type Inv")
            #_logger.warning(partner_type)
            #_logger.warning(part_types_inv)

            partner_ids = part_types_inv.mapped('partner_id.id')

            for partner in  obj_partner.browse(partner_ids):
                _logger.warning("Partener")
                _logger.warning(partner.name)
                #_logger.warning(part_types_inv.partner_id)
                part_invoices = part_types_inv.filtered(lambda r: r.partner_id.id == partner.id)
                if partner_type == '2':
                    doc_types = list(set([inv.invoice_origin_d394 for inv in part_invoices]))
                    _logger.warning(doc_types)
                    for doc_type in doc_types:
                        doctype_invoices = part_invoices.filtered( lambda r: r.invoice_origin_d394 == doc_type)
                        new_dictt = _get_vat_data(doctype_invoices,partner,partner_type,doc_type)
                        op1 += new_dictt
                else:
                    doctype_invoices = part_invoices
                    #_logger.warning(len(part_invoices))
                    doc_type = ''
                    new_dictt = _get_vat_data(doctype_invoices, partner, partner_type, doc_type)

                #_logger.warning(new_dictt)
                op1 += new_dictt
        _logger.warning(op1)
        return op1


    def compute_invoice_taxes_ammount(self,invoices):
        ''' Helper to get the taxes grouped according their account.tax.group.
        This method is only used when printing the invoice.
        '''
        ress = []
        for move in invoices:
            lang_env = move.with_context(lang=move.partner_id.lang).env
            tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id)
            tax_balance_multiplicator = -1 if move.is_inbound(True) else 1
            res = {}
            # There are as many tax line as there are repartition lines
            done_taxes = set()
            for line in tax_lines:
                res.setdefault(line.tax_line_id.tax_group_id, {'base': 0.0, 'amount': 0.0})
                res[line.tax_line_id.tax_group_id]['amount'] += tax_balance_multiplicator * (
                    line.amount_currency if line.currency_id else line.balance)
                tax_key_add_base = tuple(move._get_tax_key_for_group_add_base(line))
                if tax_key_add_base not in done_taxes:
                    if line.currency_id and line.company_currency_id and line.currency_id != line.company_currency_id:
                        amount = line.company_currency_id._convert(line.tax_base_amount, line.currency_id,
                                                                   line.company_id,
                                                                   line.date or fields.Date.context_today(self))
                    else:
                        amount = line.tax_base_amount
                    res[line.tax_line_id.tax_group_id]['base'] += amount
                    # The base should be added ONCE
                    done_taxes.add(tax_key_add_base)

            # At this point we only want to keep the taxes with a zero amount since they do not
            # generate a tax line.
            for line in move.line_ids:
                for tax in line.tax_ids.flatten_taxes_hierarchy():
                    if tax.tax_group_id not in res:
                        res.setdefault(tax.tax_group_id, {'base': 0.0, 'amount': 0.0})
                        res[tax.tax_group_id]['base'] += tax_balance_multiplicator * (
                            line.amount_currency if line.currency_id else line.balance)
                    re.findall(r'\d+', tax.tax_group_id.name)

                    _logger.warning(int(re.findall(r'\d+', tax.tax_group_id.name)[0]))

            res = sorted(res.items(), key=lambda l: l[0].sequence)
            if len(ress) == 0:
                ress = res
            else:
                for group in res:
                    found = False
                    for group_f in ress:
                        if group_f[0] == group[0]:
                            group_f[1]['base'] += group[1]['base']
                            group_f[1]['amount'] += group[1]['amount']
                            found = True
                    if not found:
                        ress.append(group)

            _logger.warning(res)
        _logger.warning(ress)
        return ress

    def _get_op2(self, receipts):
        self.ensure_one()

        obj_inv_line = self.env['account.move.line']

        #obj_period = self.env['account.period']
        comp_curr = self.company_id.currency_id
        op2 = []
        oper_type = 'I1'

        months = set([fields.Date.from_string(receipt.invoice_date).month for receipt in receipts])
        _logger.warning(f'Month{months}')
        nrAMEF = len(set([receipt.journal_id.id for receipt in receipts]))
        nrBF = len(receipts)
        total = 0
        baza20 = baza19 = baza9 = baza5 = 0
        tva20 = tva19 = tva9 = tva5 = 0
        cota_groups=self.compute_invoice_taxes_ammount(receipts)

        #domain = [('move_id', 'in', receipts.id)]
        #inv_lines = obj_inv_line.search(domain)
        # cotas = set([tax.id for tax in inv_lines.mapped(
        #         'invoice_line_tax_id')])
        #     cotas = [x for x in cotas if x]
        #     for cota in self.env['account.tax'].browse(cotas):
        #         cota_inv = period_inv.filtered(
        #             lambda r: cota.id in r.tax_ids.ids)
        #         cota_amount = 0
        #         if cota.type == 'percent':
        #             if cota.child_ids:
        #                 cota_amount = int(
        #                     abs(cota.child_ids[0].amount) * 100)
        #             else:
        #                 cota_amount = int(cota.amount * 100)
        #         elif cota.type == 'amount':
        #             cota_amount = int(cota.amount)
        #         if cota_amount in (5, 9, 19, 20):
        #             domain = [('invoice_id', 'in', cota_inv.ids)]
        #             inv_lines = obj_inv_line.search(domain)
        #             filtered_inv_lines = []
        #             for inv_line in inv_lines:
        #                 inv_type = inv_line.invoice_id.type
        #                 if inv_type in ('out_invoice',
        #                                 'out_refund'):
        #                     tax = inv_line.invoice_line_tax_id
        #                 if cota.id in tax.ids:
        #                     filtered_inv_lines.append(inv_line.id)
        #             inv_lines = obj_inv_line.browse(filtered_inv_lines)
        #             for line in inv_lines:
        #                 inv_curr = line.invoice_id.currency_id
        #                 inv_date = line.invoice_id.date_invoice
        #                 new_base = inv_curr.with_context(
        #                     {'date': inv_date}).compute(
        #                     line.price_subtotal, comp_curr)
        #                 new_taxes = inv_curr.with_context(
        #                     {'date': inv_date}).compute(
        #                     line.price_normal_taxes and
        #                     line.price_normal_taxes or
        #                     line.price_taxes, comp_curr)
        #                 if cota_amount == 20:
        #                     baza20 += new_base
        #                     tva20 += new_taxes
        #                 if cota_amount == 19:
        #                     baza19 += new_base
        #                     tva19 += new_taxes
        #                 elif cota_amount == 9:
        #                     baza9 += new_base
        #                     tva9 += new_taxes
        #                 elif cota_amount == 5:
        #                     baza5 += new_base
        #                     tva5 += new_taxes
        for cota_group in cota_groups:
            cota_group_dict = cota_group[1]
            if  cota_group[0].name== "TVA 19%":
                baza19 = cota_group_dict['base']
                tva19 = cota_group_dict['amount']
            if cota_group[0].name== "TVA 9%":
                baza9 = cota_group_dict['base']
                tva9 = cota_group_dict['amount']
            if cota_group[0].name== "TVA 5%":
                baza5 = cota_group_dict['base']
                tva5 = cota_group_dict['amount']

            _logger.warning(cota_group[1])
            op2.append({
                'tip_op2': oper_type,
                'luna': list(months)[0],
                'nrAMEF': int(round(nrAMEF)),
                'nrBF': int(round(nrBF)),
                'total': int(round(baza20 + baza19 + baza9 + baza5 + tva20 + tva19 + tva9 + tva5)),
                'baza20': int(round(baza20)),
                'baza19': int(round(baza19)),
                'baza9': int(round(baza9)),
                'baza5': int(round(baza5)),
                'TVA20': int(round(tva20)),
                'TVA19': int(round(tva19)),
                'TVA9': int(round(tva9)),
                'TVA5': int(round(tva5))})
        return op2


    def _generate_rezumat1(self, invoices, payments, op1, op2):
        self.ensure_one()
        rezumat1 = []
        partner_types = set([x['tip_partener'] for x in op1])
        for partner_type in partner_types:
            cotas = set([x['cota'] for x in op1
                         if x['tip_partener'] == partner_type])
            for cota in cotas:
                op1s = []
                if partner_type == '2':
                    doc_types = set([x['tip_document'] for
                                     x in op1 if x['tip_partener'] ==
                                     partner_type and
                                     x['tip'] == 'N'])
                    for doc_type in doc_types:
                        _logger.warning("RRRezumaTTTT")
                        op1s = [x for x in op1 if
                                x['tip_partener'] == partner_type and
                                x['cota'] == cota and
                                x['tip_document'] == doc_type]
                    if op1s:
                        rezumat1.append(self.generate_rezumat1(invoices, op1s))
                    op1s = [x for x in op1 if
                            x['tip_partener'] == partner_type and
                            x['cota'] == cota and
                            x['tip'] != 'N']
                else:
                    op1s = [x for x in op1 if
                            x['tip_partener'] == partner_type and
                            x['cota'] == cota]
                if op1s:
                    rezumat1.append(self.generate_rezumat1(invoices, op1s))
        return rezumat1

    def generate_rezumat1(self, invoices, op1s):
        self.ensure_one()
        obj_inv = self.env['account.move']
        obj_inv_line = self.env['account.move.line']
        obj_d394_code = self.env['anaf.product.code']
        partner_type = op1s[0]['tip_partener']
        oper_type = op1s[0]['tip']
        cota_amount = int(op1s[0]['cota'])
        rezumat1 = {}
        rezumat1['tip_partener'] = op1s[0]['tip_partener']
        rezumat1['cota'] = op1s[0]['cota']
        if cota_amount != 0:
            rezumat1['facturiL'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'L')))
            rezumat1['bazaL'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'L')))
            rezumat1['tvaL'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'L')))
        if partner_type == '1' and cota_amount == 0:
            rezumat1['facturiLS'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'LS')))
            rezumat1['bazaLS'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'LS')))
        if partner_type == '1' and cota_amount != 0:
            rezumat1['facturiA'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'A')))
            rezumat1['bazaA'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'A')))
            rezumat1['tvaA'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'A')))
        if partner_type == '1' and cota_amount != 0:
            rezumat1['facturiAI'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'AI')))
            rezumat1['bazaAI'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'AI')))
            rezumat1['tvaAI'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'AI')))
        if partner_type in ('1', '3', '4') and cota_amount == 0:
            rezumat1['facturiAS'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'AS')))
            rezumat1['bazaAS'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'AS')))
        if (partner_type == '1') and (cota_amount == 0):
            rezumat1['facturiV'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'V')))
            rezumat1['bazaV'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'V')))
            rezumat1['tvaV'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'V')))
        if (partner_type != '2') and (cota_amount != 0):
            rezumat1['facturiC'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'C')))
            rezumat1['bazaC'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'C')))
            rezumat1['tvaC'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'C')))
        if op1s[0]['tip_partener'] == '2' and ('tip_document' in op1s[0]):

           rezumat1['facturiN'] = int(round(sum(
               op['tva'] for op in op1s if op['tip'] == 'N')))
           rezumat1['document_N'] = op1s[0]['tip_document']
           _logger.warning(op1s)
           rezumat1['bazaN'] = int(round(sum(
                op['baza'] for op  in op1s if  op['tip'] == 'N')))
        rez_detaliu = []
        for op1 in op1s:
            if op1['op11']:
                for line in op1['op11']:
                    code = line['codPR']
                    new_code = obj_d394_code.search([('name', '=', code)])
                    if len(new_code) >= 2:
                        new_code = new_code[0]
                    if new_code and new_code.parent_id:
                        new_code = new_code.parent_id
                    if rez_detaliu:
                        found = False
                        for val in rez_detaliu:
                            if new_code.name == val['bun']:
                                found = True
                        if found:
                            for val in rez_detaliu:
                                if new_code.name == val['bun']:
                                    if op1['tip'] == 'L':
                                        val['nrLiv'] += int(
                                            round(line['nrFactPR']))
                                        val['bazaLiv'] += int(
                                            round(line['bazaPR']))
                                        val['tvaLiv'] += int(
                                            round(line['tvaPR']))
                                    if op1['tip'] == 'V' and op1['cota'] == 0:
                                        val['nrLivV'] += int(
                                            round(line['nrFactPR']))
                                        val['bazaLivV'] += int(
                                            round(line['bazaPR']))
                                    #    val['tvaLivV'] += int(
                                    #        round(line['tvaPR']))
                                    if op1['tip'] == 'A':
                                        val['nrAchiz'] += int(
                                            round(line['nrFactPR']))
                                        val['bazaAchiz'] += int(
                                            round(line['bazaPR']))
                                        val['tvaAchiz'] += int(
                                            round(line['tvaPR']))
                                    if op1['tip'] == 'AI':
                                        val['nrAchizAI'] += int(
                                            round(line['nrFactPR']))
                                        val['bazaAchizAI'] += int(
                                            round(line['bazaPR']))
                                        val['tvaAchizAI'] += int(
                                            round(line['tvaPR']))
                                    if op1['tip'] == 'C' and op1['cota'] != 0:
                                        val['nrAchizC'] += int(
                                            round(line['nrFactPR']))
                                        val['bazaAchizC'] += int(
                                            round(line['bazaPR']))
                                        val['tvaAchizC'] += int(
                                            round(line['tvaPR']))
                                    if op1['tip'] == 'N' and \
                                        partner_type == '2':
                                        val['nrN'] += int(
                                            round(line['nrFactPR']))
                                        val['valN'] += int(
                                            round(line['bazaPR']))
                        else:
                            val = {}
                            val['bun'] = new_code.name
                            if op1['tip'] == 'L':
                                val['nrLiv'] = val['bazaLiv'] = 0
                                val['tvaLiv'] = 0
                            if op1['tip'] == 'V' and op1['cota'] == 0:
                                val['nrLivV'] = val['bazaLivV'] = 0
                            #    val['tvaLivV'] = 0
                            if op1['tip'] == 'A':
                                val['nrAchiz'] = val['bazaAchiz'] = 0
                                val['tvaAchiz'] = 0
                            if op1['tip'] == 'AI':
                                val['nrAchizAI'] = val['bazaAchizAI'] = 0
                                val['tvaAchizAI'] = 0
                            if op1['tip'] == 'C' and op1['cota'] != 0:
                                val['nrAchizC'] = val['bazaAchizC'] = 0
                                val['tvaAchizC'] = 0
                            if partner_type == '2':
                                val['nrN'] = val['valN'] = 0
                            if op1['tip'] == 'L':
                                val['nrLiv'] += int(
                                    round(line['nrFactPR']))
                                val['bazaLiv'] += int(
                                    round(line['bazaPR']))
                                val['tvaLiv'] += int(
                                    round(line['tvaPR']))
                            if op1['tip'] == 'V' and op1['cota'] == 0:
                                val['nrLivV'] += int(
                                    round(line['nrFactPR']))
                                val['bazaLivV'] += int(
                                    round(line['bazaPR']))
                            #    val['tvaLivV'] += int(
                            #        round(line['tvaPR']))
                            if op1['tip'] == 'A':
                                val['nrAchiz'] += int(
                                    round(line['nrFactPR']))
                                val['bazaAchiz'] += int(
                                    round(line['bazaPR']))
                                val['tvaAchiz'] += int(
                                    round(line['tvaPR']))
                            if op1['tip'] == 'AI':
                                val['nrAchizAI'] += int(
                                    round(line['nrFactPR']))
                                val['bazaAchizAI'] += int(
                                    round(line['bazaPR']))
                                val['tvaAchizAI'] += int(
                                    round(line['tvaPR']))
                            if op1['tip'] == 'C' and op1['cota'] != 0:
                                val['nrAchizC'] += int(
                                    round(line['nrFactPR']))
                                val['bazaAchizC'] += int(
                                    round(line['bazaPR']))
                                val['tvaAchizC'] += int(
                                    round(line['tvaPR']))
                            if op1['tip'] == 'N' and partner_type == '2':
                                val['nrN'] += int(
                                    round(line['nrFactPR']))
                                val['valN'] += int(
                                    round(line['bazaPR']))
                            rez_detaliu.append(val)
                    else:
                        val = {}
                        val['bun'] = new_code.name
                        if op1['tip'] == 'L':
                            val['nrLiv'] = val['bazaLiv'] = 0
                            val['tvaLiv'] = 0
                        if op1['tip'] == 'V' and op1['cota'] == 0:
                            val['nrLivV'] = val['bazaLivV'] = 0
                        #    val['tvaLivV'] = 0
                        if op1['tip'] == 'A':
                            val['nrAchiz'] = val['bazaAchiz'] = 0
                            val['tvaAchiz'] = 0
                        if op1['tip'] == 'AI':
                            val['nrAchizAI'] = val['bazaAchizAI'] = 0
                            val['tvaAchizAI'] = 0
                        if op1['tip'] == 'C' and op1['cota'] != 0:
                            val['nrAchizC'] = val['bazaAchizC'] = 0
                            val['tvaAchizC'] = 0
                        if partner_type == '2':
                            val['nrN'] = val['valN'] = 0

                        if op1['tip'] == 'L':
                            val['nrLiv'] += int(round(line['nrFactPR']))
                            val['bazaLiv'] += int(round(line['bazaPR']))
                            val['tvaLiv'] += int(round(line['tvaPR']))
                        if op1['tip'] == 'V' and op1['cota'] == 0:
                            val['nrLivV'] += int(round(line['nrFactPR']))
                            val['bazaLivV'] += int(round(line['bazaPR']))
                        #    val['tvaLivV'] += int(round(line['tvaPR']))
                        if op1['tip'] == 'A':
                            val['nrAchiz'] += int(round(line['nrFactPR']))
                            val['bazaAchiz'] += int(round(line['bazaPR']))
                            val['tvaAchiz'] += int(round(line['tvaPR']))
                        if op1['tip'] == 'AI':
                            val['nrAchizAI'] += int(round(line['nrFactPR']))
                            val['bazaAchizAI'] += int(round(line['bazaPR']))
                            val['tvaAchizAI'] += int(round(line['tvaPR']))
                        if op1['tip'] == 'C' and op1['cota'] != 0:
                            val['nrAchizC'] += int(round(line['nrFactPR']))
                            val['bazaAchizC'] += int(round(line['bazaPR']))
                            val['tvaAchizC'] += int(round(line['tvaPR']))
                        if op1['tip'] == 'N' and partner_type == '2':
                            val['nrN'] += int(round(line['nrFactPR']))
                            val['valN'] += int(round(line['bazaPR']))
                        rez_detaliu.append(val)
        rezumat1['detaliu'] = rez_detaliu
        return rezumat1

    def _get_inv_lines(self, invoices, sel_cota, domain):
        obj_inv_line = self.env['account.move.line']
        inv_lines = False
        if invoices:
            invs = invoices.filtered(lambda r: domain)
            domain = [('move_id', 'in', invs.ids)]
            inv_lines = obj_inv_line.search(domain)
            cotas = []
            for inv_line in inv_lines:
                cotas += [tax for tax in inv_line.tax_ids]
            filtered_inv_lines = []
            cota_amount = 0
            for cota in cotas:
                cota_inv = inv_lines.filtered(
                    lambda r: cota.id in r.tax_ids.ids)
                cota_amount = 0
                if cota.amount_type == 'percent':
                    if cota.children_tax_ids:
                        cota_amount = int(abs(cota.children_tax_ids[0].amount) * 100)
                    else:
                        cota_amount = int(cota.amount * 100)
                elif cota.amount_type == 'amount':
                    cota_amount = int(cota.amount)
                if cota_amount == sel_cota:
                    filtered_inv_lines = []
                    for inv_line in inv_lines:
                        tax = inv_line.invoice_line_tax_id
                        if cota.id in tax.ids:
                            filtered_inv_lines.append(inv_line.id)
            inv_lines = obj_inv_line.browse(filtered_inv_lines)
        return inv_lines

    def generate_rezumat2(self, sel_cota, invoices, op1s, op2):
        self.ensure_one()
        obj_inv = self.env['account.move']
        obj_inv_line = self.env['account.move.line']
        rezumat2 = {}
        if op1s:
            oper_type = op1s[0]['tip']
            cota_amount = int(op1s[0]['cota'])
            rezumat2['cota'] = op1s[0]['cota']
            # To review
            rezumat2['bazaFSLcod'] = 0
            rezumat2['TVAFSLcod'] = 0
            rezumat2['bazaFSL'] = 0
            rezumat2['TVAFSL'] = 0
            rezumat2['bazaFSA'] = 0
            rezumat2['TVAFSA'] = 0
            rezumat2['bazaFSAI'] = 0
            rezumat2['TVAFSAI'] = 0

            rezumat2['bazaBFAI'] = 0
            rezumat2['TVABFAI'] = 0

            rezumat2['bazaL_PF'] = 0
            rezumat2['tvaL_PF'] = 0

            fr_inv = domain = "r.operation_type == 'L' and \
                r.fiscal_receipt is True"
            inv_lines = self._get_inv_lines(invoices, cota_amount, domain)
            if inv_lines:
                rezumat2['bazaBFAI'] = int(round(sum(
                    line.price_subtotal for line in inv_lines if
                    not line.invoice_id.journal_id.fiscal_receipt)))
                rezumat2['TVABFAI'] = int(round(sum(
                    line.price_normal_taxes and
                    line.price_normal_taxes or line.price_taxes
                    for line in inv_lines if
                    not line.invoice_id.journal_id.fiscal_receipt)))
            rezumat2['nrFacturiL'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'L')))
            rezumat2['bazaL'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'L')))
            rezumat2['tvaL'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'L')))
            rezumat2['nrFacturiA'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] in ('A', 'C'))))
            rezumat2['bazaA'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] in ('A', 'C'))))
            rezumat2['tvaA'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] in ('A', 'C'))))
            rezumat2['nrFacturiAI'] = int(round(sum(
                op['nrFact'] for op in op1s if op['tip'] == 'AI')))
            rezumat2['bazaAI'] = int(round(sum(
                op['baza'] for op in op1s if op['tip'] == 'AI')))
            rezumat2['tvaAI'] = int(round(sum(
                op['tva'] for op in op1s if op['tip'] == 'AI')))
            if cota_amount == 5:
                rezumat2['baza_incasari_i1'] = int(round(sum(
                    x['baza5'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['tva_incasari_i1'] = int(round(sum(
                    x['TVA5'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['baza_incasari_i2'] = int(round(sum(
                    x['baza5'] for x in op2 if
                    x['tip_op2'] == 'I2')))
                rezumat2['tva_incasari_i2'] = int(round(sum(
                    x['TVA5'] for x in op2 if
                    x['tip_op2'] == 'I2')))
            if cota_amount == 9:
                rezumat2['baza_incasari_i1'] = int(round(sum(
                    x['baza9'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['tva_incasari_i1'] = int(round(sum(
                    x['TVA9'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['baza_incasari_i2'] = int(round(sum(
                    x['baza9'] for x in op2 if
                    x['tip_op2'] == 'I2')))
                rezumat2['tva_incasari_i2'] = int(round(sum(
                    x['TVA9'] for x in op2 if
                    x['tip_op2'] == 'I2')))
            if cota_amount == 19:
                rezumat2['baza_incasari_i1'] = int(round(sum(
                    x['baza19'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['tva_incasari_i1'] = int(round(sum(
                    x['TVA19'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['baza_incasari_i2'] = int(round(sum(
                    x['baza19'] for x in op2 if
                    x['tip_op2'] == 'I2')))
                rezumat2['tva_incasari_i2'] = int(round(sum(
                    x['TVA19'] for x in op2 if
                    x['tip_op2'] == 'I2')))
            if cota_amount == 20:
                rezumat2['baza_incasari_i1'] = int(round(sum(
                    x['baza20'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['tva_incasari_i1'] = int(round(sum(
                    x['TVA20'] for x in op2 if
                    x['tip_op2'] == 'I1')))
                rezumat2['baza_incasari_i2'] = int(round(sum(
                    x['baza20'] for x in op2 if
                    x['tip_op2'] == 'I2')))
                rezumat2['tva_incasari_i2'] = int(round(sum(
                    x['TVA20'] for x in op2 if
                    x['tip_op2'] == 'I2')))
            domain = "r.operation_type == 'L' and \
                r.partner_type == '2' and r.amount_total <= 10000"
            inv_lines = self._get_inv_lines(invoices, cota_amount, domain)
        else:
            rezumat2['cota'] = sel_cota
            rezumat2['bazaFSLcod'] = 0
            rezumat2['TVAFSLcod'] = 0
            rezumat2['bazaFSL'] = 0
            rezumat2['TVAFSL'] = 0
            rezumat2['bazaFSA'] = 0
            rezumat2['TVAFSA'] = 0
            rezumat2['bazaFSAI'] = 0
            rezumat2['TVAFSAI'] = 0
            rezumat2['bazaBFAI'] = 0
            rezumat2['TVABFAI'] = 0
            rezumat2['nrFacturiL'] = 0
            rezumat2['bazaL'] = 0
            rezumat2['tvaL'] = 0
            rezumat2['nrFacturiA'] = 0
            rezumat2['bazaA'] = 0
            rezumat2['tvaA'] = 0
            rezumat2['nrFacturiAI'] = 0
            rezumat2['bazaAI'] = 0
            rezumat2['tvaAI'] = 0
            rezumat2['baza_incasari_i1'] = 0
            rezumat2['tva_incasari_i1'] = 0
            rezumat2['baza_incasari_i2'] = 0
            rezumat2['tva_incasari_i2'] = 0
            rezumat2['bazaL_PF'] = 0
            rezumat2['tvaL_PF'] = 0
        return rezumat2

    def _generate_rezumat2(self, invoices, payments, op1, op2):
        self.ensure_one()
        rezumat2 = []
        cotas = set([x['cota'] for x in op1 if
                     x['cota'] != 0] + [5, 9, 19, 20])
        for cota in cotas:
            op1s = [x for x in op1 if x['cota'] == cota]
            rezumat2.append(self.generate_rezumat2(cota, invoices, op1s, op2))
        return rezumat2


    def _generate_lista(self):
        self.ensure_one()
        obj_tax = self.env['account.tax']
        obj_invoice = self.env['account.move']
        obj_inv_line = self.env['account.move.line']
        comp_curr = self.company_id.currency_id
        caens = ['1071', '4520', '4730', '47761', '47762', '4932', '55101',
                 '55102', '55103', '5630', '0812', '9313', '9602', '9603']
        lista = []
        invoices = obj_invoice.search([
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', 'in', ['open', 'paid']),

            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('move_type', '!=', 'out_receipt'),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ])

        companies = set(invoices.mapped('company_id.id'))
        for company in self.env['res.company'].browse(companies):
            if company.codcaen.code.zfill(4) in caens:
                comp_inv = invoices.filtered(
                    lambda r: r.company_id.id == company.id)
                cotas = []
                for invoice in comp_inv:
                    cotas += set([tax.id for tax in invoice.tax_ids])
                cotas = set(cotas)
                for cota in obj_tax.browse(cotas):
                    cota_amount = 0
                    if cota.type == 'percent':
                        if cota.child_ids:
                            cota_amount = int(
                                abs(cota.child_ids[0].amount) * 100)
                        else:
                            cota_amount = int(cota.amount * 100)
                    elif cota.type == 'amount':
                        cota_amount = int(cota.amount)
                    cota_inv = comp_inv.filtered(
                        lambda r: cota.id in r.tax_ids.ids)
                    inv_lines = obj_inv_line.search([
                        ('invoice_id', 'in', cota_inv.ids)])
                    bazab = bazas = tvab = tvas = 0
                    for line in inv_lines:
                        inv_curr = line.invoice_id.currency_id
                        inv_date = line.invoice_id.date_invoice
                        if line.product_id.type in ('product', 'consumables'):
                            bazab += inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_subtotal, comp_curr)
                            tvab += inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_normal_taxes and
                                line.price_normal_taxes or
                                line.price_taxes, comp_curr)
                        else:
                            bazas += inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_subtotal, comp_curr)
                            tvas += inv_curr.with_context(
                                {'date': inv_date}).compute(
                                line.price_normal_taxes and
                                line.price_normal_taxes or
                                line.price_taxes, comp_curr)
                    if bazab != 0:
                        bdict = {
                            'caen': company.codcaen.code.zfill(4),
                            'cota': cota_amount,
                            'operat': 1,
                            'valoare': int(round(bazab)),
                            'tva': int(round(tvab))
                        }
                        lista.append(bdict)
                    if bazas != 0:
                        sdict = {
                            'caen': company.codcaen.code.zfill(4),
                            'cota': cota_amount,
                            'operat': 2,
                            'valoare': int(round(bazas)),
                            'tva': int(round(tvas))
                        }
                        lista.append(sdict)
        return lista

    def _get_inv_series(self, invoices):






        regex = re.compile('[^a-zA-Z]')
        ctx = self._context.copy()
        year, month = self.get_year_month()
        ctx['fiscalyear_id'] = year
        #invoices = obj_invoice.search([
        #    ('state', '!=', 'draft'),
        #    ('invoice_date', '>=', self.date_from),
        #    ('invoice_date', '<=', self.date_to),
        #    '|',
        #    ('company_id', '=', self.company_id.id),
        #    ('company_id', 'in', self.company_id.child_ids.ids),
        #    '|',
        #    ('move_type', 'in', ('out_invoice', 'out_refund')),
        #    ('journal_id.sequence_type', 'in', ('autoinv1', 'autoinv2'))
        #])

        journals = self.env['account.journal']
        journal_ids = set(invoices.mapped('journal_id.id'))
        seq_dict = []
        _logger.warning(journal_ids)
        for journal in journals.browse(journal_ids):

            journal_invoices = invoices.filtered(lambda r: r.journal_id.id == journal.id)
            first_name = min(journal_invoices._origin.mapped('name'))
            _logger.warning(journal_invoices)
            _logger.warning(journal_invoices._origin.mapped('name'))
            record_first_name =  journal_invoices.filtered(lambda r :r.name==first_name)
            _logger.warning(record_first_name[0])
            formatt, format_values = journal_invoices._get_sequence_format_param(first_name)
            type_reset = journal_invoices._deduce_sequence_number_reset(first_name)
            _logger.warning(str(formatt).split("{seq:")[0].format(**format_values))

            no_digit = format_values['seq_length']
            nr_init = 0
            nr_last = 10^no_digit -1
            tip = 1
            partner = journal.partner_id
            if journal.sequence_type == 'autoinv1':
                tip = 3
            elif journal.sequence_type != 'normal':
                tip = 4

            seria = str(formatt).split("{seq:")[0].format(**format_values)
            dict_serie = {
                'tip': tip,
                'serieI': seria,
                'nrI': str(nr_init),
                'nrF': str(nr_last)
            }
            if partner:
                dict_serie['den'] = partner.name
                dict_serie['cui'] = partner._split_vat(partner.vat)[1]


            seq_dict.append(dict_serie)
            if journal.sequence_type == 'normal':
                tip = 2
            elif journal.sequence_type == 'autoinv1':
                tip = 3
            else:
                tip = 4
            dict_series1 = {
                "tip": tip,
                "serieI": seria
            }

            if type_reset == "month":
                dict_series1.update({'nrI':0,
                                     'nrF' :format_values['seq']})
            else :
                dict_series1.update({'nrI':str(format_values['seq']- len(journal_invoices)),
                                     'nrF': format_values['seq'] })
            seq_dict.append(dict_series1)

        return seq_dict

    def _generate_informatii(self, invoices, payments, op1, op2):
        informatii = {}
        informatii['nrCui1'] = len(
            set(op['cuiP'] for op in op1 if op['tip_partener'] == '1'))
        informatii['nrCui2'] = len(
            [op for op in op1 if op['tip_partener'] == '2'])
        informatii['nrCui3'] = len(
            set(op['cuiP'] for op in op1 if op['tip_partener'] == '3'))
        informatii['nrCui4'] = len(
            set(op['cuiP'] for op in op1 if op['tip_partener'] == '4'))
        informatii['nr_BF_i1'] = sum(
            op['nrBF'] for op in op2 if op['tip_op2'] == 'I1')
        informatii['incasari_i1'] = sum(
            op['total'] for op in op2 if op['tip_op2'] == 'I1')
        informatii['incasari_i2'] = sum(
            op['total'] for op in op2 if op['tip_op2'] == 'I2')
        informatii['nrFacturi_terti'] = len(
            set(invoices.filtered(lambda r: r.sequence_type == 'autoinv2')))
        informatii['nrFacturi_benef'] = len(
            set(invoices.filtered(lambda r: r.sequence_type == 'autoinv1')))
        informatii['nrFacturi'] = len(
            set(invoices.filtered(lambda r: r.move_type in ('out_invoice', 'out_refund'))))
        informatii['nrFacturiL_PF'] = 0
        informatii['nrFacturiLS_PF'] = len(
            set(invoices.filtered(lambda r: r.operation_type == 'LS' and
                                            r.partner_type == '2' and
                                            r.amount_total <= 10000)))
        informatii['val_LS_PF'] = int(round(sum(
            inv.amount_total for inv in invoices.filtered(
                lambda r: r.operation_type == 'LS' and
                          r.partner_type == '2' and
                          r.amount_total <= 10000))))
        informatii['tvaDedAI24'] = int(
            round(sum(op['tva_24'] for op in payments if
                      op['type'] in ('in_invoice', 'in_refund') and
                      op['vat_on_payment'] is True)))
        informatii['tvaDedAI20'] = int(round(sum(
            op['tva_20'] for op in payments if
            op['type'] in ('in_invoice', 'in_refund') and
            op['vat_on_payment'] is True)))
        informatii['tvaDedAI19'] = int(round(sum(
            op['tva_19'] for op in payments if
            op['type'] in ('in_invoice', 'in_refund') and
            op['vat_on_payment'] is True)))
        informatii['tvaDedAI9'] = int(round(sum(
            op['tva_9'] for op in payments if
            op['type'] in ('in_invoice', 'in_refund') and
            op['vat_on_payment'] is True)))
        informatii['tvaDedAI5'] = int(round(sum(
            op['tva_5'] for op in payments if
            op['type'] in ('in_invoice', 'in_refund') and
            op['vat_on_payment'] is True)))

        comm_partner = self.company_id.partner_id.commercial_partner_id
        ctx = dict(self._context)
        ctx.update({'check_date': self.date_to})

        if comm_partner.with_context(ctx)._check_vat_on_payment():
            informatii['tvaDed24'] = int(round(sum(
                op['tva_24'] for op in payments if
                op['type'] in ('in_invoice', 'in_refund') and
                op['vat_on_payment'] is False)))
            informatii['tvaDed20'] = int(round(sum(
                op['tva_20'] for op in payments if
                op['type'] in ('in_invoice', 'in_refund') and
                op['vat_on_payment'] is False)))
            informatii['tvaDed19'] = int(round(sum(
                op['tva_19'] for op in payments if
                op['type'] in ('in_invoice', 'in_refund') and
                op['vat_on_payment'] is False)))
            informatii['tvaDed9'] = int(round(sum(
                op['tva_9'] for op in payments if
                op['type'] in ('in_invoice', 'in_refund') and
                op['vat_on_payment'] is False)))
            informatii['tvaDed5'] = int(round(sum(
                op['tva_5'] for op in payments if
                op['type'] in ('in_invoice', 'in_refund') and
                op['vat_on_payment'] is False)))
            informatii['tvaCol24'] = int(round(sum(
                op['tva_24'] for op in payments if
                op['type'] in ('out_invoice', 'out_refund') and
                op['vat_on_payment'] is True)))
            informatii['tvaCol20'] = int(round(sum(
                op['tva_20'] for op in payments if
                op['type'] in ('out_invoice', 'out_refund') and
                op['vat_on_payment'] is True)))
            informatii['tvaCol19'] = int(round(sum(
                op['tva_19'] for op in payments if
                op['type'] in ('out_invoice', 'out_refund') and
                op['vat_on_payment'] is True)))
            informatii['tvaCol9'] = int(round(sum(
                op['tva_9'] for op in payments if
                op['type'] in ('out_invoice', 'out_refund') and
                op['vat_on_payment'] is True)))
            informatii['tvaCol5'] = int(round(sum(
                op['tva_5'] for op in payments if
                op['type'] in ('out_invoice', 'out_refund') and
                op['vat_on_payment'] is True)))
        informatii['incasari_ag'] = 0
        informatii['costuri_ag'] = 0
        informatii['marja_ag'] = 0
        informatii['tva_ag'] = 0
        informatii['pret_vanzare'] = 0
        informatii['pret_cumparare'] = 0
        informatii['marja_antic'] = 0
        informatii['tva_antic'] = 0
        informatii['solicit'] = int(self.solicit)
        if self.solicit:
            informatii['achizitiiPE'] = int(self.achizitiiPE)
            informatii['achizitiiCR'] = int(self.achizitiiCR)
            informatii['achizitiiCB'] = int(self.achizitiiCB)
            informatii['achizitiiCI'] = int(self.achizitiiCI)
            informatii['achizitiiA'] = int(self.achizitiiA)
            informatii['achizitiiB24'] = int(self.achizitiiB24)
            informatii['achizitiiB20'] = int(self.achizitiiB20)
            informatii['achizitiiB19'] = int(self.achizitiiB19)
            informatii['achizitiiB9'] = int(self.achizitiiB9)
            informatii['achizitiiB5'] = int(self.achizitiiB5)
            informatii['achizitiiS24'] = int(self.achizitiiS24)
            informatii['achizitiiS20'] = int(self.achizitiiS20)
            informatii['achizitiiS19'] = int(self.achizitiiS19)
            informatii['achizitiiS9'] = int(self.achizitiiS9)
            informatii['achizitiiS5'] = int(self.achizitiiS5)
            informatii['importB'] = int(self.importB)
            informatii['acINecorp'] = int(self.acINecorp)
            informatii['livrariBI'] = int(self.livrariBI)
            informatii['BUN24'] = int(self.BUN24)
            informatii['BUN20'] = int(self.BUN20)
            informatii['BUN19'] = int(self.BUN19)
            informatii['BUN9'] = int(self.BUN9)
            informatii['BUN5'] = int(self.BUN5)
            informatii['valoareScutit'] = int(self.valoareScutit)
            informatii['BunTI'] = int(self.BunTI)
            informatii['Prest24'] = int(self.Prest24)
            informatii['Prest20'] = int(self.Prest20)
            informatii['Prest19'] = int(self.Prest19)
            informatii['Prest9'] = int(self.Prest9)
            informatii['Prest5'] = int(self.Prest5)
            informatii['PrestScutit'] = int(self.PrestScutit)
            informatii['LIntra'] = int(self.LIntra)
            informatii['PrestIntra'] = int(self.PrestIntra)
            informatii['Export'] = int(self.Export)
            informatii['livINecorp'] = int(self.livINecorp)
            informatii['efectuat'] = int(self.solicit)
        return informatii
