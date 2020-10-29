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
        "D394.30.informatii", string="informatii", xsd_required=True
    )
    rezumat1 = fields.One2many(
        "D394.30.rezumat1", "rezumat1_Declaratie394_id", string="rezumat1"
    )
    rezumat2 = fields.One2many(
        "D394.30.rezumat2", "rezumat2_Declaratie394_id", string="rezumat2"
    )
    serieFacturi = fields.One2many(
        "D394.30.seriefacturi",
        "serieFacturi_Declaratie394_id",
        string="serieFacturi",
    )
    lista = fields.One2many(
        "D394.30.lista", "lista_Declaratie394_id", string="lista"
    )
    facturi = fields.One2many(
        "D394.30.facturi", "facturi_Declaratie394_id", string="facturi"
    )
    op1 = fields.One2many(
        "D394.30.op1", "op1_Declaratie394_id", string="op1"
    )
    op2 = fields.One2many(
        "D394.30.op2", "op2_Declaratie394_id", string="op2"
    )

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

        xmldict.update({'informatii': [],
                        'rezumat1': [],
                        'rezumat2': [],
                        'serieFacturi': [],
                        'lista': [],
                        'facturi': [],
                        'op1': [],
                        'op2': []})




        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)



class Detaliu(models.AbstractModel):
    _description = "detaliu"
    _name = "D394.30.detaliu"
    _inherit = "anaf.mixin"
    _generateds_type = "DetaliuType"
    _concrete_rec_name = "bun"

    detaliu_Rezumat1_id = fields.Many2one("D394.30.rezumat1")
    bun = fields.Many2one(
        "D394.30.int_nomenclatorbunuristype", string="bun", xsd_required=True
    )
    nrLivV = fields.Many2one("D394.30.intpoz15stype", string="nrLivV")
    bazaLivV = fields.Integer(string="bazaLivV", xsd_type="integer")
    nrAchizC = fields.Many2one("D394.30.intpoz15stype", string="nrAchizC")
    bazaAchizC = fields.Integer(string="bazaAchizC", xsd_type="integer")
    tvaAchizC = fields.Integer(string="tvaAchizC", xsd_type="integer")
    nrN = fields.Many2one("D394.30.intpoz15stype", string="nrN")
    valN = fields.Integer(string="valN", xsd_type="integer")




class Facturi(models.AbstractModel):
    _description = "facturi"
    _name = "D394.30.facturi"
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
            if inv.type in ('out_invoice', 'out_refund'):
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
                facturi.append(new_dict)
        return facturi



class Informatii(models.AbstractModel):
    _description = "informatii"
    _name = "D394.30.informatii"
    _inherit = "anaf.mixin"
    _generateds_type = "InformatiiType"
    _concrete_rec_name = "nrCui1"

    nrCui1 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui1", xsd_required=True
    )
    nrCui2 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui2", xsd_required=True
    )
    nrCui3 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui3", xsd_required=True
    )
    nrCui4 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui4", xsd_required=True
    )
    nr_BF_i1 = fields.Many2one(
        "D394.30.intpoz15stype", string="nr_BF_i1", xsd_required=True
    )
    incasari_i1 = fields.Integer(
        string="incasari_i1", xsd_required=True, xsd_type="integer"
    )
    incasari_i2 = fields.Integer(
        string="incasari_i2", xsd_required=True, xsd_type="integer"
    )
    nrFacturi_terti = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi_terti", xsd_required=True
    )
    nrFacturi_benef = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi_benef", xsd_required=True
    )
    nrFacturi = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi", xsd_required=True
    )
    nrFacturiL_PF = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiL_PF", xsd_required=True
    )
    nrFacturiLS_PF = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiLS_PF", xsd_required=True
    )
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
    solicit = fields.Integer(
        string="solicit", xsd_required=True, xsd_type="integer"
    )
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

    def generate_informatii(self):
        pass


class Lista(models.AbstractModel):
    _description = "lista"
    _name = "D394.30.lista"
    _inherit = "anaf.mixin"
    _generateds_type = "ListaType"
    _concrete_rec_name = "caen"

    lista_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    caen = fields.Many2one(
        "D394.30.int_listacaenstype", string="caen", xsd_required=True
    )
    cota = fields.Many2one(
        "D394.30.int_cotetva2stype", string="cota", xsd_required=True
    )
    operat = fields.Many2one(
        "D394.30.intint1_2stype", string="operat", xsd_required=True
    )
    valoare = fields.Integer(
        string="valoare", xsd_required=True, xsd_type="integer"
    )
    tva = fields.Integer(string="tva", xsd_required=True, xsd_type="integer")




class Op11(models.AbstractModel):
    _description = "op11"
    _name = "D394.30.op11"
    _inherit = "anaf.mixin"
    _generateds_type = "Op11Type"
    _concrete_rec_name = "nrFactPR"

    op11_Op1_id = fields.Many2one("D394.30.op1")
    nrFactPR = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFactPR", xsd_required=True
    )
    codPR = fields.Many2one(
        "D394.30.str_listacodprstype", string="codPR", xsd_required=True
    )
    bazaPR = fields.Integer(
        string="bazaPR", xsd_required=True, xsd_type="integer"
    )
    tvaPR = fields.Integer(string="tvaPR", xsd_type="integer")


class Op1(models.AbstractModel):
    _description = "op1"
    _name = "D394.30.op1"
    _inherit = "anaf.mixin"
    _generateds_type = "Op1Type"
    _concrete_rec_name = "tip"

    op1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip = fields.Many2one(
        "D394.30.str_listatipoperatiestype", string="tip", xsd_required=True
    )
    tip_partener = fields.Many2one(
        "D394.30.int_tippartenerop1stype", string="tip_partener", xsd_required=True
    )
    cota = fields.Many2one(
        "D394.30.int_cotetvastype", string="cota", xsd_required=True
    )
    cuiP = fields.Char(string="cuiP", xsd_type="string")
    denP = fields.Char(string="denP", xsd_required=True, xsd_type="string")
    taraP = fields.Many2one("D394.30.str_listataristype", string="taraP")
    locP = fields.Char(string="locP", xsd_type="string")
    judP = fields.Many2one("D394.30.str_listajudstype", string="judP")
    strP = fields.Char(string="strP", xsd_type="string")
    nrP = fields.Char(string="nrP", xsd_type="string")
    blP = fields.Char(string="blP", xsd_type="string")
    apP = fields.Char(string="apP", xsd_type="string")
    detP = fields.Many2one("D394.30.str100", string="detP")
    tip_document = fields.Many2one(
        "D394.30.intint1_5stype", string="tip_document"
    )
    nrFact = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFact", xsd_required=True
    )
    baza = fields.Integer(string="baza", xsd_required=True, xsd_type="integer")
    tva = fields.Integer(string="tva", xsd_type="integer")
    op11 = fields.One2many("D394.30.op11", "op11_Op1_id", string="op11")


class Op2(models.AbstractModel):
    _description = "op2"
    _name = "D394.30.op2"
    _inherit = "anaf.mixin"
    _generateds_type = "Op2Type"
    _concrete_rec_name = "tip_op2"

    op2_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip_op2 = fields.Many2one(
        "D394.30.str_tipoperatiestype", string="tip_op2", xsd_required=True
    )
    luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    nrAMEF = fields.Many2one("D394.30.intpoz4stype", string="nrAMEF")
    nrBF = fields.Many2one("D394.30.intpoz15stype", string="nrBF")
    total = fields.Many2one(
        "D394.30.intpoz15stype", string="total", xsd_required=True
    )
    baza20 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza20", xsd_required=True
    )
    baza9 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza9", xsd_required=True
    )
    baza5 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza5", xsd_required=True
    )
    TVA20 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA20", xsd_required=True
    )
    TVA9 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA9", xsd_required=True
    )
    TVA5 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA5", xsd_required=True
    )
    baza19 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza19", xsd_required=True
    )
    TVA19 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA19", xsd_required=True
    )


class Rezumat1(models.AbstractModel):
    _description = "rezumat1"
    _name = "D394.30.rezumat1"
    _inherit = "anaf.mixin"
    _generateds_type = "Rezumat1Type"
    _concrete_rec_name = "tip_partener"

    rezumat1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip_partener = fields.Many2one(
        "D394.30.int_tippartenerstype", string="tip_partener", xsd_required=True
    )
    cota = fields.Many2one(
        "D394.30.int_cotetvastype", string="cota", xsd_required=True
    )
    facturiL = fields.Many2one("D394.30.intpoz15stype", string="facturiL")
    bazaL = fields.Integer(string="bazaL", xsd_type="integer")
    tvaL = fields.Integer(string="tvaL", xsd_type="integer")
    facturiLS = fields.Many2one("D394.30.intpoz15stype", string="facturiLS")
    bazaLS = fields.Integer(string="bazaLS", xsd_type="integer")
    facturiA = fields.Many2one("D394.30.intpoz15stype", string="facturiA")
    bazaA = fields.Integer(string="bazaA", xsd_type="integer")
    tvaA = fields.Integer(string="tvaA", xsd_type="integer")
    facturiAI = fields.Many2one("D394.30.intpoz15stype", string="facturiAI")
    bazaAI = fields.Integer(string="bazaAI", xsd_type="integer")
    tvaAI = fields.Integer(string="tvaAI", xsd_type="integer")
    facturiAS = fields.Many2one("D394.30.intpoz15stype", string="facturiAS")
    bazaAS = fields.Integer(string="bazaAS", xsd_type="integer")
    facturiV = fields.Many2one("D394.30.intpoz15stype", string="facturiV")
    bazaV = fields.Integer(string="bazaV", xsd_type="integer")
    facturiC = fields.Many2one("D394.30.intpoz15stype", string="facturiC")
    bazaC = fields.Integer(string="bazaC", xsd_type="integer")
    tvaC = fields.Integer(string="tvaC", xsd_type="integer")
    facturiN = fields.Many2one("D394.30.intpoz15stype", string="facturiN")
    document_N = fields.Many2one("D394.30.intint1_5stype", string="document_N")
    bazaN = fields.Integer(string="bazaN", xsd_type="integer")
    detaliu = fields.One2many(
        "D394.30.detaliu", "detaliu_Rezumat1_id", string="detaliu"
    )


class Rezumat2(models.AbstractModel):
    _description = "rezumat2"
    _name = "D394.30.rezumat2"
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
    nrFacturiL = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiL", xsd_required=True
    )
    bazaL = fields.Integer(string="bazaL", xsd_required=True, xsd_type="integer")
    tvaL = fields.Integer(string="tvaL", xsd_required=True, xsd_type="integer")
    nrFacturiA = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiA", xsd_required=True
    )
    bazaA = fields.Integer(string="bazaA", xsd_required=True, xsd_type="integer")
    tvaA = fields.Integer(string="tvaA", xsd_required=True, xsd_type="integer")
    nrFacturiAI = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiAI", xsd_required=True
    )
    bazaAI = fields.Integer(
        string="bazaAI", xsd_required=True, xsd_type="integer"
    )
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
    _name = "D394.30.seriefacturi"
    _inherit = "anaf.mixin"
    _generateds_type = "SerieFacturiType"
    _concrete_rec_name = "tip"

    serieFacturi_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    tip = fields.Many2one(
        "D394.30.intint1_4stype", string="tip", xsd_required=True
    )
    serieI = fields.Many2one("D394.30.str20", string="serieI")
    nrI = fields.Many2one("D394.30.str20", string="nrI", xsd_required=True)
    nrF = fields.Many2one("D394.30.str20", string="nrF")
    den = fields.Many2one("D394.30.str100", string="den")
    cui = fields.Char(string="cui", xsd_type="token")
