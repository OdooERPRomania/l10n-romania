# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Sun Oct 18 11:13:02 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Declaratie394(models.AbstractModel):
    _name = "anaf.d394.v30"
    _inherit = "anaf.mixin"
    _description = "declaratie394"

    luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    D39430_an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    tip_D394 = fields.Char( string="tip_D394", xsd_required=True,xsd_type="string" )
    sistemTVA = fields.Integer(string="sistemTVA", xsd_required=True, xsd_type="integer")
    op_efectuate = fields.Integer(string="op_efectuate", xsd_required=True, xsd_type="integer")
    cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    caen = fields.Char( string="caen", xsd_required=True)
    den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    telefon = fields.Char(string="telefon", xsd_required=True, xsd_type="string")
    fax = fields.Char(string="fax", xsd_type="string")
    mail = fields.Char(string="mail", xsd_type="string")
    totalPlata_A = fields.Integer(string="totalPlata_A", xsd_required=True, xsd_type="integer")
    cifR = fields.Char(string="cifR", xsd_type="token")
    denR = fields.Char(string="denR", xsd_required=True, xsd_type="string")
    functie_reprez = fields.Char(string="functie_reprez", xsd_required=True,  xsd_type="string")
    adresaR = fields.Char(string="adresaR", xsd_required=True, xsd_type="string")
    telefonR = fields.Char(string="telefonR", xsd_type="string")
    faxR = fields.Char(string="faxR", xsd_type="string")
    mailR = fields.Char(string="mailR", xsd_type="string")
    tip_intocmit = fields.Integer(string="tip_intocmit", xsd_required=True, xsd_type="integer")
    den_intocmit = fields.Char(string="den_intocmit", xsd_required=True, xsd_type="string")
    cif_intocmit = fields.Integer(string="cif_intocmit", xsd_required=True,xsd_type="integer")
    calitate_intocmit = fields.Char(string="calitate_intocmit", xsd_type="string")
    functie_intocmit = fields.Char(string="functie_intocmit", xsd_type="string")
    optiune = fields.Integer(string="optiune", xsd_required=True, xsd_type="integer")
    schimb_optiune = fields.Integer( string="schimb_optiune",xsd_required=True, xsd_type="integer")
    prsAfiliat = fields.Char(string="prsAfiliat", xsd_required=True, xsd_type="string")
    informatii = fields.Many2one(
        "informatii", string="informatii", xsd_required=True
    )
    rezumat1 = fields.One2many(
        "d394.30.rezumat1", "rezumat1_Declaratie394_id", string="rezumat1"
    )
    rezumat2 = fields.One2many(
        "d394.30.rezumat2", "rezumat2_Declaratie394_id", string="rezumat2"
    )
    serieFacturi = fields.One2many(
        "d394.30.seriefacturi",
        "serieFacturi_Declaratie394_id",
        string="serieFacturi",
    )
    lista = fields.One2many(
        "lista", "lista_Declaratie394_id", string="lista"
    )
    facturi = fields.One2many(
        "facturi", "facturi_Declaratie394_id", string="facturi"
    )
    op1 = fields.One2many(
        "d394.30.op1", "op1_Declaratie394_id", string="op1"
    )
    op2 = fields.One2many(
        "d394.30.op2", "op2_Declaratie394_id", string="op2"
    )
    def generate_facturi(self):
        year, mounth = self.get_year_month()
        obj_invoice = self.env['account.move']
        obj_period = self.env['account.period']
        comp_currency = self.company_id.currency_id
        facturi = []
        invoices1 = obj_invoice.search([
            ('fiscal_receipt', '=', False),
            ('state', '!=', 'draft'),
            ('period_id', '=', self.period_id.id),
            ('date_invoice', '>=', self.date_from),
            ('date_invoice', '<=', self.date_to),
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
                    'serie': inv.inv_serie,
                    'nr': inv.inv_number,
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
                    factura = self.env['facturi'].create(new_dict)
                facturi.append(new_dict)
        return facturi


    def _get_op1(self, invoices):
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
        comp_curr = self.company_id.currency_id
        op1 = []
        oper_types = set([invoice.operation_type for invoice in invoices])
        for oper_type in oper_types:
            oper_type_inv = invoices.filtered(
                lambda r: r.operation_type == oper_type)
            partner_types = set([
                invoice.partner_type for invoice in oper_type_inv])
            for partner_type in partner_types:
                part_type_inv = oper_type_inv.filtered(
                    lambda r: r.partner_type == partner_type)
                cotas = []
                for invoice in part_type_inv:
                    cotas += set([tax.id for tax in invoice.tax_ids])
                cotas = set(cotas)
                for cota in obj_tax.browse(cotas):
                    cota_inv = part_type_inv.filtered(
                        lambda r: cota.id in r.tax_ids.ids)
                    partners = cota_inv.mapped('partner_id.id')
                    for partner in obj_partner.browse(partners):
                        new_oper_type = oper_type
                        part_invoices = cota_inv.filtered(
                            lambda r: r.partner_id.id == partner.id)
                        cota_amount = 0
                        if cota.amount_type == 'percent':
                            if cota.child_ids:
                                cota_amount = int(
                                    abs(cota.child_ids[0].amount) * 100)
                            else:
                                cota_amount = int(cota.amount * 100)
                        elif cota.amount_type == 'amount':
                            cota_amount = int(cota.amount)
                        if new_oper_type == 'A' and \
                            'Ti-ach' in cota.description:
                            new_oper_type = 'C'
                        if new_oper_type == 'L' and \
                            'Ti-livr' in cota.description:
                            new_oper_type = 'V'
                        inv_lines = []
                        if partner_type == '2':
                            if new_oper_type == 'N':
                                doc_types = [
                                    inv.origin_type for inv in part_invoices]
                                for doc_type in doc_types:
                                    domain = [('invoice_id',
                                               'in',
                                               part_invoices.ids),
                                              ('invoice_id.origin_type',
                                               '=',
                                               doc_type)]
                                    inv_lines = obj_inv_line.search(domain)
                                    filtered_inv_lines = []
                                    for inv_line in inv_lines:
                                        invoice = inv_line.invoice_id
                                        product = inv_line.product_id
                                        fp = invoice.fiscal_position_id
                                        tax = product.supplier_taxes_id
                                        if not fp or (
                                            ('Regim National' in fp.name) or
                                            ('Regim Taxare Inversa' in fp.name) or
                                            ('Regim Intra-Comunitar Scutit' in fp.name)):
                                            tax = inv_line.invoice_line_tax_id
                                            if cota.id in tax.ids:
                                                filtered_inv_lines.append(
                                                    inv_line.id)
                                        else:
                                            inv_type = inv_line.invoice_id.type
                                            if inv_type in ('out_invoice',
                                                            'out_refund'):
                                                tax = product.taxes_id
                                            if cota.id in tax.ids:
                                                filtered_inv_lines.append(
                                                    inv_line.id)
                                    inv_lines = obj_inv_line.browse(
                                        filtered_inv_lines)
                                    op1= Op1()
                                    op1.baza = 0
                                    for line in inv_lines:
                                        inv_curr = line.invoice_id.currency_id
                                        inv_date = line.invoice_id.date_invoice
                                        op1.baza += inv_curr.with_context(
                                            {'date': inv_date}).compute(
                                            line.price_subtotal, comp_curr)
                                    op1.taxes = 0
                                    op1.tip = new_oper_type
                                    op1.tip_partener = partner_types
                                    op1.cota_amount = cota_amount
                                    op1.denP=partner.name.replace(
                                            '&', '-').replace('"', '')
                                    op1.nrFact = len(set(
                                            [line.invoice_id.id for
                                             line in inv_lines]))
                                    op1.baza = int(round(op1.baza))
                                    op1.tip_document = doc_type
                                    new_dict = {
                                        'tip': new_oper_type,
                                        'tip_partener': partner_type,
                                        'cota': cota_amount,
                                        'denP': op1.denP,
                                        'nrFact': op1.nrFact,
                                        'baza': op1.baza,
                                        'tip_document': op1.tip_document,
                                    }
                            else:
                                domain = [('invoice_id',
                                           'in',
                                           part_invoices.ids)]
                                inv_lines = obj_inv_line.search(domain)
                                filtered_inv_lines = []
                                for inv_line in inv_lines:
                                    fp = inv_line.invoice_id.fiscal_position_id
                                    tax = inv_line.product_id.supplier_taxes_id
                                    inv = inv_line.invoice_id
                                    if not fp or  (
                                        ('Regim National' in fp.name) or
                                        ('Regim Taxare Inversa' in fp.name) or
                                        (('Regim Intra-Comunitar Scutit' in
                                          inv.fiscal_position_id.name) and
                                         inv.partner_type in ('1', '2'))):
                                        tax = inv_line.invoice_line_tax_id
                                        if cota.id in tax.ids:
                                            filtered_inv_lines.append(
                                                inv_line.id)
                                    else:
                                        inv_type = inv_line.invoice_id.type
                                        if inv_type in ('out_invoice',
                                                        'out_refund'):
                                            tax = inv_line.product_id.taxes_id
                                        if cota.id in tax.ids:
                                            filtered_inv_lines.append(
                                                inv_line.id)
                                inv_lines = obj_inv_line.browse(
                                    filtered_inv_lines)
                                op1.baza = 0
                                op1.taxes = 0
                                for line in inv_lines:
                                    inv_curr = line.invoice_id.currency_id
                                    inv_date = line.invoice_id.date_invoice
                                    op1.baza += inv_curr.with_context(
                                        {'date': inv_date}).compute(
                                        line.price_subtotal, comp_curr)
                                    op1.taxes += inv_curr.with_context(
                                        {'date': inv_date}).compute(
                                        line.price_normal_taxes and
                                        line.price_normal_taxes or
                                        line.price_taxes, comp_curr)
                                new_dict = {
                                    'tip': new_oper_type,
                                    'tip_partener': partner_type,
                                    'cota': cota_amount,
                                    'denP': partner.name.replace(
                                        '&', '-').replace('"', ''),
                                    'nrFact': len(set([
                                        line.invoice_id.id for
                                        line in inv_lines])),
                                    'baza': int(round(baza)),
                                    'tva': int(round(taxes)),
                                }
                            if not partner.is_company:
                                if partner.vat:
                                    new_dict['cuiP'] = partner._split_vat(
                                        partner.vat)[1]
                                else:
                                    if partner.country_id:
                                        new_dict['taraP'] = \
                                            partner.country_id and \
                                            partner.country_id.code.upper()
                                    if partner.city_id:
                                        new_dict['locP'] = \
                                            partner.city_id and \
                                            partner.city_id.name
                                    if partner.state_id:
                                        new_dict['judP'] = \
                                            partner.state_id and \
                                            partner.state_id.order_code
                                    if partner.street:
                                        new_dict['strP'] = \
                                            partner.add_street and \
                                            partner.add_street
                                    if partner.add_number:
                                        new_dict['nrP'] = \
                                            partner.add_number and \
                                            partner.add_number
                                    if partner.add_block:
                                        new_dict['blP'] = \
                                            partner.add_block and \
                                            partner.add_block
                                    if partner.add_flat:
                                        new_dict['apP'] = \
                                            partner.add_flat and \
                                            partner.add_flat
                                    if partner.street2:
                                        new_dict['detP'] = \
                                            partner.street2 and \
                                            partner.street2
                            else:
                                if partner.vat:
                                    new_dict['cuiP'] = partner._split_vat(
                                        partner.vat)[1]
                        else:
                            domain = [('invoice_id', 'in', part_invoices.ids)]
                            inv_lines = obj_inv_line.search(domain)
                            filtered_inv_lines = []
                            for inv_line in inv_lines:
                                fp = inv_line.invoice_id.fiscal_position_id
                                tax = inv_line.product_id.supplier_taxes_id
                                inv = inv_line.invoice_id
                                if not fp or (
                                    ('National' in fp.name) or
                                    ('Invers' in fp.name) or
                                    (('Scutit' in
                                      inv.fiscal_position_id.name) and
                                     inv.partner_type == '2')):
                                    tax = inv_line.invoice_line_tax_id
                                    if cota.id in tax.ids:
                                        filtered_inv_lines.append(
                                            inv_line.id)
                                elif not fp or ('Scutit' not in
                                                inv.fiscal_position_id.name):
                                    inv_type = inv_line.invoice_id.type
                                    if inv_type in ('out_invoice',
                                                    'out_refund'):
                                        tax = inv_line.product_id.taxes_id
                                    if cota.id in tax.ids:
                                        filtered_inv_lines.append(
                                            inv_line.id)
                            inv_lines = obj_inv_line.browse(filtered_inv_lines)
                            baza = 0
                            taxes = 0
                            for line in inv_lines:
                                inv_curr = line.invoice_id.currency_id
                                inv_date = line.invoice_id.date_invoice
                                baza += inv_curr.with_context(
                                    {'date': inv_date}).compute(
                                    line.price_subtotal, comp_curr)
                                if new_oper_type in \
                                    ('L', 'A', 'AI'):
                                    taxes += inv_curr.with_context(
                                        {'date': inv_date}).compute(
                                        line.price_taxes, comp_curr)
                                if (new_oper_type == 'C') or \
                                    ((new_oper_type == 'L') and
                                     (line.invoice_id.partner_type in
                                      ('3', '4'))):
                                    taxes += inv_curr.with_context(
                                        {'date': inv_date}).compute(
                                        line.price_normal_taxes and
                                        line.price_normal_taxes or
                                        line.price_taxes, comp_curr)

                            new_dict = {
                                'tip': new_oper_type,
                                'tip_partener': partner_type,
                                'cota': cota_amount,
                                'cuiP': partner.vat and partner._split_vat(
                                    partner.vat)[1] or '-',
                                'denP': partner.name.replace(
                                    '&', '-').replace('"', ''),
                                'nrFact': len(part_invoices),
                                'baza': int(round(baza)),
                                'op11': []
                            }
                            if new_oper_type in ('A', 'L', 'C', 'AI'):
                                new_dict['tva'] = int(round(taxes))

                        if inv_lines:
                            codes = inv_lines.mapped('product_id.d394_id')
                            op11 = []
                            if (partner_type == '1' and new_oper_type in (
                                'V', 'C')) or (partner_type == '2' and
                                               new_oper_type == 'N'):
                                for code in codes:
                                    new_code = code
                                    if code.parent_id:
                                        new_code = code.parent_id
                                    cod_lines = []
                                    if partner_type == '1':
                                        cod_lines = [
                                            line for line in
                                            inv_lines.filtered(
                                                lambda r:
                                                r.product_id.d394_id.id ==
                                                code.id and
                                                new_code.name <= '31')
                                        ]
                                    else:
                                        cod_lines = [
                                            line for line in
                                            inv_lines.filtered(
                                                lambda r:
                                                r.product_id.d394_id.id ==
                                                code.id)
                                        ]
                                    if cod_lines:
                                        nrFact = len(set([
                                            line.invoice_id.id for line in
                                            inv_lines.filtered(
                                                lambda r:
                                                r.product_id.d394_id.id ==
                                                code.id)]))
                                        baza1 = 0
                                        taxes1 = 0
                                        for line in cod_lines:
                                            inv_curr = \
                                                line.invoice_id.currency_id
                                            inv_date = \
                                                line.invoice_id.date_invoice
                                            baza1 += inv_curr.with_context(
                                                {'date': inv_date}).compute(
                                                line.price_subtotal,
                                                comp_curr)
                                            new_taxes = inv_curr.with_context(
                                                {'date': inv_date}).compute(
                                                line.price_normal_taxes and
                                                line.price_normal_taxes or
                                                line.price_taxes,
                                                comp_curr)
                                            if new_oper_type == 'C':
                                                taxes1 += new_taxes
                                        op11_dict = {
                                            'codPR': code.name,
                                            'nrFactPR': nrFact,
                                            'bazaPR': int(round(baza1))
                                        }
                                        if new_oper_type in (
                                            'A', 'L', 'C', 'AI'):
                                            op11_dict['tvaPR'] = \
                                                int(round(taxes1))
                                        op11.append(op11_dict)
                            new_dict['op11'] = op11
                            op1 = adauga_op1(op1, new_dict)
        return op1


    def _get_op2(self, invoices):
        self.ensure_one()
        if fields.Date.from_string(self.date_from) < \
            fields.Date.from_string('2016-10-01'):
            return []
        obj_inv_line = self.env['account.move.line']

        obj_period = self.env['account.period']
        comp_curr = self.company_id.currency_id
        op2 = []
        oper_type = 'I1'
        periods = set([invoice.period_id.id for invoice in invoices])
        for period in obj_period.browse(periods):
            period_inv = invoices.filtered(
                lambda r: r.period_id.id == period.id)
            nrAMEF = \
                len(set([invoice.journal_id.id for invoice in period_inv]))
            nrBF = len(period_inv)
            total = 0
            baza20 = baza19 = baza9 = baza5 = 0
            tva20 = tva19 = tva9 = tva5 = 0
            domain = [('invoice_id', 'in', period_inv.ids)]
            inv_lines = obj_inv_line.search(domain)
            cotas = set([tax.id for tax in inv_lines.mapped(
                'invoice_line_tax_id')])
            cotas = [x for x in cotas if x]
            for cota in self.env['account.tax'].browse(cotas):
                cota_inv = period_inv.filtered(
                    lambda r: cota.id in r.tax_ids.ids)
                cota_amount = 0
                if cota.type == 'percent':
                    if cota.child_ids:
                        cota_amount = int(
                            abs(cota.child_ids[0].amount) * 100)
                    else:
                        cota_amount = int(cota.amount * 100)
                elif cota.type == 'amount':
                    cota_amount = int(cota.amount)
                if cota_amount in (5, 9, 19, 20):
                    domain = [('invoice_id', 'in', cota_inv.ids)]
                    inv_lines = obj_inv_line.search(domain)
                    filtered_inv_lines = []
                    for inv_line in inv_lines:
                        inv_type = inv_line.invoice_id.type
                        if inv_type in ('out_invoice',
                                        'out_refund'):
                            tax = inv_line.invoice_line_tax_id
                        if cota.id in tax.ids:
                            filtered_inv_lines.append(inv_line.id)
                    inv_lines = obj_inv_line.browse(filtered_inv_lines)
                    for line in inv_lines:
                        inv_curr = line.invoice_id.currency_id
                        inv_date = line.invoice_id.date_invoice
                        new_base = inv_curr.with_context(
                            {'date': inv_date}).compute(
                            line.price_subtotal, comp_curr)
                        new_taxes = inv_curr.with_context(
                            {'date': inv_date}).compute(
                            line.price_normal_taxes and
                            line.price_normal_taxes or
                            line.price_taxes, comp_curr)
                        if cota_amount == 20:
                            baza20 += new_base
                            tva20 += new_taxes
                        if cota_amount == 19:
                            baza19 += new_base
                            tva19 += new_taxes
                        elif cota_amount == 9:
                            baza9 += new_base
                            tva9 += new_taxes
                        elif cota_amount == 5:
                            baza5 += new_base
                            tva5 += new_taxes
            op2.append({
                'tip_op2': oper_type,
                'luna': int(period.code[:2]),
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


    def build_file(self):
        year, month = self.get_year_month()
        data_file = """
        <?xml version="1.0" encoding="UTF-8"?>
        <declaratie394 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="mfp:anaf:dgti:d394:declaratie:v3 D394.xsd"
        xmlns="mfp:anaf:dgti:d394:declaratie:v3" """

        xmldict = {
            "luna": month,
            "an": year,
            "sistemTVA": self.company_id.partner_id.vat_on_payment,
            "op_efectuate" : 1,
            "cui": self.company_id.partner_id.vat_number,
            "caen": self.company_id.caen_code,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(without_company=False).replace("\n", ","),
            "telefon": self.company_id.phone,
            "fax": self.company_id.fax,
            "mail": self.company_id.email,
            "totalPlata_A": 0,
            "tip_intocmit" : 1,
            "den_intocmit":self.user.partner_id.commercial_partner_id,
            "Dcif_intocmit" : self.user.partner_id.commercial_partner_id.vat_number}

        if self.user.partner_id.comercial_partener_id:
            xmldict.update({"calitate_intocmit" : self.user.partner_id.functie})
        else:
            xmldict.update({"functie_intocmit " : self.user.partner_id.vat and self.user.partner_id.vat[2:] or ''})

        xmldict.update({"optiune":1,
                        "schimb_optiune":1,
                        "prsAfiliat":1})
        obj_invoice = self.env['account.move']
        invoices = obj_invoice.search([
            ('state', 'in', ['open', 'paid']),
            #('period_id', '=', period.id),
            ('fiscal_receipt', '=', False),
            ('date_invoice', '>=', self.date_from),
            ('date_invoice', '<=', self.date_to),
            '|',
            ('company_id', '=', self.company_id.id),
            ('company_id', 'in', self.company_id.child_ids.ids)
        ])
        xmldict.update({'informatii': [],
                        'rezumat1': [],
                        'rezumat2': [],
                        'serieFacturi': [],
                        'lista': [],
                        'facturi': self.generate_facturi(),
                        'op1': self._get_op1(invoices),
                        'op2': []})




        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)



class Detaliu(models.AbstractModel):
    _description = "detaliu"
    _name = "detaliu"
    #_inherit = "anaf.mixin"
    _generateds_type = "DetaliuType"
    _concrete_rec_name = "bun"

    detaliu_Rezumat1_id = fields.Many2one("d394.30.rezumat1")
    bun = fields.Many2one(
        "D394.30.int_nomenclatorbunuristype", string="bun", xsd_required=True
    )
    nrLivV = fields.Integer( string="nrLivV",xsd_type="integer",)
    bazaLivV = fields.Integer(string="bazaLivV", xsd_type="integer")
    nrAchizC = fields.Integer( string="nrAchizC",  xsd_type="integer")
    bazaAchizC = fields.Integer(string="bazaAchizC", xsd_type="integer")
    tvaAchizC = fields.Integer(string="tvaAchizC", xsd_type="integer")
    nrN = fields.Integer(xsd_type="integer", string="nrN")
    valN = fields.Integer(string="valN", xsd_type="integer")




class Facturi(models.AbstractModel):
    _description = "facturi"
    _name = "facturi"
    _inherit = "anaf.mixin"
    _generateds_type = "FacturiType"
    _concrete_rec_name = "tip_factura"

    facturi_Declaratie394_id = fields.Many2one("anaf.d394.v30")
    tip_factura = fields.Char( string="tip_factura", xsd_required=True,xsd_type="string" )
    serie = fields.Char( string="serie", xsd_required=True, xsd_type="string")
    nr = fields.Char(string="nr", xsd_required=True,xsd_type="string")
    baza24 = fields.Integer(string="baza24", xsd_type="integer")
    baza20 = fields.Integer(string="baza20", xsd_type="integer")
    baza19 = fields.Integer(string="baza19", xsd_type="integer")
    baza9 = fields.Integer(string="baza9", xsd_type="integer")
    baza5 = fields.Integer(string="baza5", xsd_type="integer")
    tva5 = fields.Integer(string="tva5", xsd_type="integer")
    tva19 = fields.Integer(string="tva19", xsd_type="integer")
    tva9 = fields.Integer(string="tva9", xsd_type="integer")
    tva20 = fields.Integer(string="tva20", xsd_type="integer")
    tva24 = fields.Integer(string="tva24", xsd_type="integer")





class Informatii(models.AbstractModel):
    _description = "informatii"
    _name = "informatii"
    _inherit = "anaf.mixin"
    _generateds_type = "InformatiiType"
    _concrete_rec_name = "nrCui1"

    nrCui1 = fields.Integer( string="nrCui1", xsd_required=True, xsd_type="integer" )
    nrCui2 = fields.Integer( string="nrCui2", xsd_required=True,xsd_type="integer")
    nrCui3 = fields.Integer(string="nrCui3", xsd_required=True, xsd_type="integer")
    nrCui4 = fields.Integer(string="nrCui4", xsd_required=True, xsd_type="integer")
    nr_BF_i1 = fields.Integer( string="nr_BF_i1", xsd_required=True,xsd_type="integer")
    incasari_i1 = fields.Integer(string="incasari_i1", xsd_required=True, xsd_type="integer")
    incasari_i2 = fields.Integer(string="incasari_i2", xsd_required=True, xsd_type="integer"
    )
    nrFacturi_terti = fields.Integer( string="nrFacturi_terti", xsd_required=True,xsd_type="integer")
    nrFacturi_benef = fields.Integer( string="nrFacturi_benef", xsd_required=True, xsd_type="integer")
    nrFacturi = fields.Integer( string="nrFacturi", xsd_required=True, xsd_type="integer")
    nrFacturiL_PF = fields.Integer( string="nrFacturiL_PF", xsd_required=True,xsd_type="integer")
    nrFacturiLS_PF = fields.Integer( string="nrFacturiLS_PF", xsd_required=True, xsd_type="integer")
    val_LS_PF = fields.Integer(
        string="val_LS_PF", xsd_required=True, xsd_type="integer"
    )
    tvaDed24 = fields.Integer(string="tvaDed24", xsd_type="integer")
    tvaDed20 = fields.Integer(string="tvaDed20", xsd_type="integer")
    tvaDed19 = fields.Integer(string="tvaDed19", xsd_type="integer")
    tvaDed9 = fields.Integer(string="tvaDed9", xsd_type="integer")
    tvaDed5 = fields.Integer(string="tvaDed5", xsd_type="integer")
    tvaDedAI24 = fields.Integer(
        string="tvaDedAI24", xsd_required=True, xsd_type="integer"
    )
    tvaDedAI20 = fields.Integer(
        string="tvaDedAI20", xsd_required=True, xsd_type="integer"
    )
    tvaDedAI19 = fields.Integer(
        string="tvaDedAI19", xsd_required=True, xsd_type="integer"
    )
    tvaDedAI9 = fields.Integer(
        string="tvaDedAI9", xsd_required=True, xsd_type="integer"
    )
    tvaDedAI5 = fields.Integer(
        string="tvaDedAI5", xsd_required=True, xsd_type="integer"
    )
    tvaCol24 = fields.Integer(string="tvaCol24", xsd_type="integer")
    tvaCol20 = fields.Integer(string="tvaCol20", xsd_type="integer")
    tvaCol19 = fields.Integer(string="tvaCol19", xsd_type="integer")
    tvaCol9 = fields.Integer(string="tvaCol9", xsd_type="integer")
    tvaCol5 = fields.Integer(string="tvaCol5", xsd_type="integer")
    incasari_ag = fields.Integer(string="incasari_ag", xsd_type="integer")
    costuri_ag = fields.Integer(string="costuri_ag", xsd_type="integer")
    marja_ag = fields.Integer(string="marja_ag", xsd_type="integer")
    tva_ag = fields.Integer(string="tva_ag", xsd_type="integer")
    pret_vanzare = fields.Integer(string="pret_vanzare", xsd_type="integer")
    pret_cumparare = fields.Integer(string="pret_cumparare", xsd_type="integer")
    marja_antic = fields.Integer(string="marja_antic", xsd_type="integer")
    tva_antic = fields.Integer(string="tva_antic", xsd_type="integer")
    solicit = fields.Integer(string="solicit", xsd_required=True, xsd_type="integer")
    achizitiiPE = fields.Integer(string="achizitiiPE", xsd_type="integer")
    achizitiiCR = fields.Integer(string="achizitiiCR", xsd_type="integer")
    achizitiiCB = fields.Integer(string="achizitiiCB", xsd_type="integer")
    achizitiiCI = fields.Integer(string="achizitiiCI", xsd_type="integer")
    achizitiiA = fields.Integer(string="achizitiiA", xsd_type="integer")
    achizitiiB24 = fields.Integer(string="achizitiiB24", xsd_type="integer")
    achizitiiB20 = fields.Integer(string="achizitiiB20", xsd_type="integer")
    achizitiiB19 = fields.Integer(string="achizitiiB19", xsd_type="integer")
    achizitiiB9 = fields.Integer(string="achizitiiB9", xsd_type="integer")
    achizitiiB5 = fields.Integer(string="achizitiiB5", xsd_type="integer")
    achizitiiS24 = fields.Integer(string="achizitiiS24", xsd_type="integer")
    achizitiiS20 = fields.Integer(string="achizitiiS20", xsd_type="integer")
    achizitiiS19 = fields.Integer(string="achizitiiS19", xsd_type="integer")
    achizitiiS9 = fields.Integer(string="achizitiiS9", xsd_type="integer")
    achizitiiS5 = fields.Integer(string="achizitiiS5", xsd_type="integer")
    importB = fields.Integer(string="importB", xsd_type="integer")
    acINecorp = fields.Integer(string="acINecorp", xsd_type="integer")
    livrariBI = fields.Integer(string="livrariBI", xsd_type="integer")
    BUN24 = fields.Integer(string="BUN24", xsd_type="integer")
    BUN20 = fields.Integer(string="BUN20", xsd_type="integer")
    BUN19 = fields.Integer(string="BUN19", xsd_type="integer")
    BUN9 = fields.Integer(string="BUN9", xsd_type="integer")
    BUN5 = fields.Integer(string="BUN5", xsd_type="integer")
    valoareScutit = fields.Integer(string="valoareScutit", xsd_type="integer")
    BunTI = fields.Integer(string="BunTI", xsd_type="integer")
    Prest24 = fields.Integer(string="Prest24", xsd_type="integer")
    Prest20 = fields.Integer(string="Prest20", xsd_type="integer")
    Prest19 = fields.Integer(string="Prest19", xsd_type="integer")
    Prest9 = fields.Integer(string="Prest9", xsd_type="integer")
    Prest5 = fields.Integer(string="Prest5", xsd_type="integer")
    PrestScutit = fields.Integer(string="PrestScutit", xsd_type="integer")
    LIntra = fields.Integer(string="LIntra", xsd_type="integer")
    PrestIntra = fields.Integer(string="PrestIntra", xsd_type="integer")
    Export = fields.Integer(string="Export", xsd_type="integer")
    livINecorp = fields.Integer(string="livINecorp", xsd_type="integer")
    efectuat = fields.Integer(string="efectuat", xsd_type="integer")




class Lista(models.AbstractModel):
    _description = "lista"
    _name = "lista"
    _inherit = "anaf.mixin"
    _generateds_type = "ListaType"
    _concrete_rec_name = "caen"

    lista_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    caen = fields.Integer(string="caen", xsd_required=True, xsd_type="integer")
    cota = fields.Integer( string="cota", xsd_required=True, xsd_type="integer"  )
    operat = fields.Integer(string="operat", xsd_required=True, xsd_type="integer")
    valoare = fields.Integer(string="valoare", xsd_required=True, xsd_type="integer")
    tva = fields.Integer(string="tva", xsd_required=True, xsd_type="integer")




class Op11(models.AbstractModel):
    _description = "op11"
    _name = "d394.30.op11"
    _inherit = "anaf.mixin"
    _generateds_type = "Op11Type"
    _concrete_rec_name = "nrFactPR"

    op11_Op1_id = fields.Many2one("d394.30.op1")
    nrFactPR = fields.Integer(string="nrFactPR", xsd_required=True, xsd_type="integer")
    codPR = fields.Char( string="codPR", xsd_required=True, xsd_type="string")
    bazaPR = fields.Integer(string="bazaPR", xsd_required=True, xsd_type="integer")
    tvaPR = fields.Integer(string="tvaPR", xsd_type="integer")


class Op1(models.AbstractModel):
    _description = "op1"
    _name = "d394.30.op1"
    _inherit = "anaf.mixin"
    _generateds_type = "Op1Type"
    _concrete_rec_name = "tip"

    op1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip = fields.Char(string="tip", xsd_required=True, xsd_type="string")
    tip_partener = fields.Integer(string="tip_partener", xsd_required=True, xsd_type="integer")
    cota = fields.Integer(string="cota", xsd_required=True, xsd_type="integer")
    cuiP = fields.Char(string="cuiP", xsd_type="string")
    denP = fields.Char(string="denP", xsd_required=True, xsd_type="string")
    taraP = fields.Char(xsd_required=True, xsd_type="string", string="taraP")
    locP = fields.Char(string="locP", xsd_type="string")
    judP = fields.Char(xsd_required=True, xsd_type="string", string="judP")
    strP = fields.Char(string="strP", xsd_type="string")
    nrP = fields.Char(string="nrP", xsd_type="string")
    blP = fields.Char(string="blP", xsd_type="string")
    apP = fields.Char(string="apP", xsd_type="string")
    detP = fields.Integer(xsd_required=True, xsd_type="string", string="detP")
    tip_document = fields.Char(xsd_required=True, xsd_type="string", string="tip_document")
    nrFact = fields.Integer(xsd_required=True, xsd_type="string", string="nrFact")
    baza = fields.Integer(string="baza", xsd_required=True, xsd_type="integer")
    tva = fields.Integer(string="tva", xsd_type="integer")
    op11 = fields.One2many("d394.30.op11", "op11_Op1_id", string="op11")


class Op2(models.AbstractModel):
    _description = "op2"
    _name = "d394.30.op2"
    _inherit = "anaf.mixin"
    _generateds_type = "Op2Type"
    _concrete_rec_name = "tip_op2"

    op2_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip_op2 = fields.Many2one(
        "D394.30.str_tipoperatiestype", string="tip_op2", xsd_required=True
    )
    luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    nrAMEF = fields.Integer( string="nrAMEF",  xsd_required=True, xsd_type="integer")
    nrBF = fields.Integer(string="nrBF",  xsd_required=True, xsd_type="integer")
    total = fields.Integer( string="total", xsd_required=True, xsd_type="integer")
    baza20 = fields.Integer( string="baza20", xsd_required=True, xsd_type="integer")
    baza9 = fields.Integer( string="baza9", xsd_required=True, xsd_type="integer")
    baza5 = fields.Integer( string="baza5", xsd_required=True, xsd_type="integer")
    TVA20 = fields.Integer( string="TVA20", xsd_required=True, xsd_type="integer")
    TVA9 = fields.Integer( string="TVA9", xsd_required=True, xsd_type="integer")
    TVA5 = fields.Integer( string="TVA5", xsd_required=True, xsd_type="integer")
    baza19 = fields.Integer( string="baza19", xsd_required=True, xsd_type="integer")
    TVA19 = fields.Integer( string="TVA19", xsd_required=True, xsd_type="integer")


class Rezumat1(models.AbstractModel):
    _description = "rezumat1"
    _name = "d394.30.rezumat1"
    _inherit = "anaf.mixin"
    _generateds_type = "Rezumat1Type"
    _concrete_rec_name = "tip_partener"

    rezumat1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip_partener = fields.Many2one(
        "D394.30.int_tippartenerstype", string="tip_partener", xsd_required=True
    )
    cota = fields.Integer( string="cota", xsd_required=True)
    facturiL = fields.Integer( string="facturiL",xsd_type="integer")
    bazaL = fields.Integer(string="bazaL", xsd_type="integer")
    tvaL = fields.Integer(string="tvaL", xsd_type="integer")
    facturiLS = fields.Integer( string="facturiLS", xsd_type="integer")
    bazaLS = fields.Integer(string="bazaLS", xsd_type="integer")
    facturiA = fields.Integer(string="facturiA",xsd_type="integer")
    bazaA = fields.Integer(string="bazaA", xsd_type="integer")
    tvaA = fields.Integer(string="tvaA", xsd_type="integer")
    facturiAI = fields.Integer(string="facturiAI", xsd_type="integer")
    bazaAI = fields.Integer(string="bazaAI", xsd_type="integer")
    tvaAI = fields.Integer(string="tvaAI", xsd_type="integer")
    facturiAS = fields.Integer( string="facturiAS",xsd_type="integer" )
    bazaAS = fields.Integer(string="bazaAS", xsd_type="integer")
    facturiV = fields.Integer(xsd_type="integer", string="facturiV")
    bazaV = fields.Integer(string="bazaV", xsd_type="integer")
    facturiC = fields.Integer( string="facturiC", xsd_type="integer")
    bazaC = fields.Integer(string="bazaC", xsd_type="integer")
    tvaC = fields.Integer(string="tvaC", xsd_type="integer")
    facturiN = fields.Integer(string="facturiN", xsd_type="integer")
    document_N = fields.Integer(string="document_N", xsd_type="integer")
    bazaN = fields.Integer(string="bazaN", xsd_type="integer")
    detaliu = fields.One2many(
        "detaliu", "detaliu_Rezumat1_id", string="detaliu"
    )


class Rezumat2(models.AbstractModel):
    _description = "rezumat2"
    _name = "d394.30.rezumat2"
    _inherit = "anaf.mixin"
    _generateds_type = "Rezumat2Type"
    _concrete_rec_name = "cota"

    rezumat2_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    cota = fields.Many2one("D394.30.int_cotetva2stype", string="cota")
    bazaFSLcod = fields.Integer(
        string="bazaFSLcod", xsd_required=True, xsd_type="integer"
    )
    TVAFSLcod = fields.Integer(
        string="TVAFSLcod", xsd_required=True, xsd_type="integer"
    )
    bazaFSL = fields.Integer(
        string="bazaFSL", xsd_required=True, xsd_type="integer"
    )
    TVAFSL = fields.Integer(
        string="TVAFSL", xsd_required=True, xsd_type="integer"
    )
    bazaFSA = fields.Integer(
        string="bazaFSA", xsd_required=True, xsd_type="integer"
    )
    TVAFSA = fields.Integer(
        string="TVAFSA", xsd_required=True, xsd_type="integer"
    )
    bazaFSAI = fields.Integer(
        string="bazaFSAI", xsd_required=True, xsd_type="integer"
    )
    TVAFSAI = fields.Integer(
        string="TVAFSAI", xsd_required=True, xsd_type="integer"
    )
    bazaBFAI = fields.Integer(
        string="bazaBFAI", xsd_required=True, xsd_type="integer"
    )
    TVABFAI = fields.Integer(
        string="TVABFAI", xsd_required=True, xsd_type="integer"
    )
    nrFacturiL = fields.Integer(xsd_type="integer", string="nrFacturiL", xsd_required=True)
    bazaL = fields.Integer(string="bazaL", xsd_required=True, xsd_type="integer")
    tvaL = fields.Integer(string="tvaL", xsd_required=True, xsd_type="integer")
    nrFacturiA = fields.Integer( string="nrFacturiA", xsd_required=True)
    bazaA = fields.Integer(string="bazaA", xsd_required=True, xsd_type="integer")
    tvaA = fields.Integer(string="tvaA", xsd_required=True, xsd_type="integer")
    nrFacturiAI = fields.Integer( string="nrFacturiAI", xsd_required=True)
    bazaAI = fields.Integer(string="bazaAI", xsd_required=True, xsd_type="integer")
    tvaAI = fields.Integer(string="tvaAI", xsd_required=True, xsd_type="integer")
    baza_incasari_i1 = fields.Integer(
        string="baza_incasari_i1", xsd_type="integer"
    )
    tva_incasari_i1 = fields.Integer(
        string="tva_incasari_i1", xsd_type="integer"
    )
    baza_incasari_i2 = fields.Integer(
        string="baza_incasari_i2", xsd_type="integer"
    )
    tva_incasari_i2 = fields.Integer(
        string="tva_incasari_i2", xsd_type="integer"
    )
    bazaL_PF = fields.Integer(
        string="bazaL_PF", xsd_required=True, xsd_type="integer"
    )
    tvaL_PF = fields.Integer(
        string="tvaL_PF", xsd_required=True, xsd_type="integer"
    )


class SerieFacturi(models.AbstractModel):
    _description = "seriefacturi"
    _name = "d394.30.seriefacturi"
    _inherit = "anaf.mixin"
    _generateds_type = "SerieFacturiType"
    _concrete_rec_name = "tip"

    serieFacturi_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip = fields.Many2one(
        "D394.30.intint1_4stype", string="tip", xsd_required=True
    )
    serieI = fields.Char( string="serieI", xsd_type="string")
    nrI = fields.Char( string="nrI", xsd_required=True)
    nrF = fields.Char( string="nrF", xsd_type="string" )
    den = fields.Char( string="den", xsd_type="string")
    cui = fields.Char(string="cui", xsd_type="token")
