# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Declaratie394(models.AbstractModel):
    _name = "anaf.d394.v30"
    _inherit = "anaf.d394"
    _description = "declaratie394"

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

        data_file = """
            <?xml version="1.0" encoding="UTF-8"?>
            <declaratie394 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="mfp:anaf:dgti:d394:declaratie:v3 D394.xsd"
            xmlns="mfp:anaf:dgti:d394:declaratie:v3" """

        xmldict = {
            "luna": month,
            "an": year,
            "op_efectuate": 1,
            "optiune": int(self.optiune),
            "schimb_optiune": int(self.schimb_optiune),
            "prsAfiliat": int(self.prsAfiliat),
            'informatii': [],
            'rezumat1': [],
            'rezumat2': [],
            'serieFacturi': [],
            'lista': [],
            'facturi': [],
            'op1': [],
            'op2': []
        }
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        month_data = self.generate_data()
        xmldict.update(month_data)
        for key, val in xmldict.items():
            data_file += """{}={} """.format(key, self.value_to_string(val))
        data_file += """ />"""
        return data_file

    def generate_company_data(self):
        data = {
            "cui": int(self.company_id.partner_id.vat_number),
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
                                    op1 = Op1()
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
                                    op1.denP = partner.name.replace(
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
                                    if not fp or (
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
