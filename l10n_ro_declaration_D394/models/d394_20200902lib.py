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

    D39430_luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    D39430_an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    D39430_tip_D394 = fields.Many2one(
        "D394.30.str_listatipd394stype", string="tip_D394", xsd_required=True
    )
    D39430_sistemTVA = fields.Integer(
        string="sistemTVA", xsd_required=True, xsd_type="integer"
    )
    D39430_op_efectuate = fields.Integer(
        string="op_efectuate", xsd_required=True, xsd_type="integer"
    )
    D39430_cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    D39430_caen = fields.Many2one(
        "D394.30.str_coduricaenstype", string="caen", xsd_required=True
    )
    D39430_den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    D39430_adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    D39430_telefon = fields.Char(string="telefon", xsd_required=True, xsd_type="string")
    D39430_fax = fields.Char(string="fax", xsd_type="string")
    D39430_mail = fields.Char(string="mail", xsd_type="string")
    D39430_totalPlata_A = fields.Integer(
        string="totalPlata_A", xsd_required=True, xsd_type="integer"
    )
    D39430_cifR = fields.Char(string="cifR", xsd_type="token")
    D39430_denR = fields.Char(string="denR", xsd_required=True, xsd_type="string")
    D39430_functie_reprez = fields.Many2one(
        "D394.30.str100", string="functie_reprez", xsd_required=True
    )
    D39430_adresaR = fields.Char(string="adresaR", xsd_required=True, xsd_type="string")
    D39430_telefonR = fields.Char(string="telefonR", xsd_type="string")
    D39430_faxR = fields.Char(string="faxR", xsd_type="string")
    D39430_mailR = fields.Char(string="mailR", xsd_type="string")
    D39430_tip_intocmit = fields.Integer(
        string="tip_intocmit", xsd_required=True, xsd_type="integer"
    )
    D39430_den_intocmit = fields.Char(
        string="den_intocmit", xsd_required=True, xsd_type="string"
    )
    D39430_cif_intocmit = fields.Many2one(
        "D394.30.intpoz13stype", string="cif_intocmit", xsd_required=True
    )
    D39430_calitate_intocmit = fields.Char(
        string="calitate_intocmit", xsd_type="string"
    )
    D39430_functie_intocmit = fields.Char(string="functie_intocmit", xsd_type="string")
    D39430_optiune = fields.Integer(
        string="optiune", xsd_required=True, xsd_type="integer"
    )
    D39430_schimb_optiune = fields.Many2one(
        "D394.30.intint1_1stype", string="schimb_optiune"
    )
    D39430_prsAfiliat = fields.Char(
        string="prsAfiliat", xsd_required=True, xsd_type="string"
    )
    D39430_informatii = fields.Many2one(
        "D394.30.informatii", string="informatii", xsd_required=True
    )
    D39430_rezumat1 = fields.One2many(
        "D394.30.rezumat1", "D39430_rezumat1_Declaratie394_id", string="rezumat1"
    )
    D39430_rezumat2 = fields.One2many(
        "D394.30.rezumat2", "D39430_rezumat2_Declaratie394_id", string="rezumat2"
    )
    D39430_serieFacturi = fields.One2many(
        "D394.30.seriefacturi",
        "D39430_serieFacturi_Declaratie394_id",
        string="serieFacturi",
    )
    D39430_lista = fields.One2many(
        "D394.30.lista", "D39430_lista_Declaratie394_id", string="lista"
    )
    D39430_facturi = fields.One2many(
        "D394.30.facturi", "D39430_facturi_Declaratie394_id", string="facturi"
    )
    D39430_op1 = fields.One2many(
        "D394.30.op1", "D39430_op1_Declaratie394_id", string="op1"
    )
    D39430_op2 = fields.One2many(
        "D394.30.op2", "D39430_op2_Declaratie394_id", string="op2"
    )

    def build_file(self):
        year, month = self.get_year_month()
        data_file = """
        <?xml version="1.0" encoding="UTF-8"?>
        <declaratie394 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="mfp:anaf:dgti:d394:declaratie:v3 D394.xsd"
        xmlns="mfp:anaf:dgti:d394:declaratie:v3" """

        xmldict = {
            "D39430_luna": month,
            "D39430_an": year,
            "D39430_sistemTVA": self.company_id.partner_id.vat_on_payment,
            "D39430_op_efectuate" : 1,
            "D39430_cui": self.company_id.partner_id.vat_number,
            "D39430_caen": self.company_id.caen_code,
            "D39430_den": self.company_id.name,
            "D39430_adresa": self.company_id.partner_id._display_address(without_company=False).replace("\n", ","),
            "D39430_telefon": self.company_id.phone,
            "D39430_fax": self.company_id.fax,
            "D39430_mail": self.company_id.email,
            "D39430_totalPlata_A": 0,
            "D39430_tip_intocmit" : 1,
            "D39430_den_intocmit":self.user.partner_id.commercial_partner_id,
            "DD39430_cif_intocmit" : self.user.partner_id.commercial_partner_id.vat_number}

        if self.user.partner_id.comercial_partener_id:
            xmldict.update({"D39430_calitate_intocmit" : self.user.partner_id.functie})
        else:
            xmldict.update({"D39430_functie_intocmit " : self.user.partner_id.vat and self.user.partner_id.vat[2:] or ''})

        xmldict.update({"D39430_optiune":1,
                        "D39430_schimb_optiune":1,
                        "D39430_prsAfiliat":1})

        xmldict.update({'D39430_informatii': [],
                        'D39430_rezumat1': [],
                        'D39430_rezumat2': [],
                        'D39430_serieFacturi': [],
                        'D39430_lista': [],
                        'D39430_facturi': [],
                        'D39430_op1': [],
                        'D39430_op2': []})




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
    _concrete_rec_name = "D39430_bun"

    D39430_detaliu_Rezumat1_id = fields.Many2one("D394.30.rezumat1")
    D39430_bun = fields.Many2one(
        "D394.30.int_nomenclatorbunuristype", string="bun", xsd_required=True
    )
    D39430_nrLivV = fields.Many2one("D394.30.intpoz15stype", string="nrLivV")
    D39430_bazaLivV = fields.Integer(string="bazaLivV", xsd_type="integer")
    D39430_nrAchizC = fields.Many2one("D394.30.intpoz15stype", string="nrAchizC")
    D39430_bazaAchizC = fields.Integer(string="bazaAchizC", xsd_type="integer")
    D39430_tvaAchizC = fields.Integer(string="tvaAchizC", xsd_type="integer")
    D39430_nrN = fields.Many2one("D394.30.intpoz15stype", string="nrN")
    D39430_valN = fields.Integer(string="valN", xsd_type="integer")




class Facturi(models.AbstractModel):
    _description = "facturi"
    _name = "D394.30.facturi"
    _inherit = "anaf.mixin"
    _generateds_type = "FacturiType"
    _concrete_rec_name = "D39430_tip_factura"

    D39430_facturi_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_tip_factura = fields.Many2one(
        "D394.30.intint1_4stype", string="tip_factura", xsd_required=True
    )
    D39430_serie = fields.Many2one("D394.30.str20", string="serie")
    D39430_nr = fields.Many2one("D394.30.str20", string="nr", xsd_required=True)
    D39430_baza24 = fields.Integer(string="baza24", xsd_type="integer")
    D39430_baza20 = fields.Integer(string="baza20", xsd_type="integer")
    D39430_baza19 = fields.Integer(string="baza19", xsd_type="integer")
    D39430_baza9 = fields.Integer(string="baza9", xsd_type="integer")
    D39430_baza5 = fields.Integer(string="baza5", xsd_type="integer")
    D39430_tva5 = fields.Integer(string="tva5", xsd_type="integer")
    D39430_tva19 = fields.Integer(string="tva19", xsd_type="integer")
    D39430_tva9 = fields.Integer(string="tva9", xsd_type="integer")
    D39430_tva20 = fields.Integer(string="tva20", xsd_type="integer")
    D39430_tva24 = fields.Integer(string="tva24", xsd_type="integer")

    def generate_facturi(self):
        obj_inv_line = self.env['account.invoice.line']
        obj_invoice = self.env['account.invoice']
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
            r.journal_id.sequence_type in ('autoinv1', 'autoinv2'))
        for inv in invoices:
            baza24 = baza20 = baza19 = baza9 = baza5 = 0
            tva24 = tva20 = tva19 = tva9 = tva5 = 0
            inv_curr = inv.currency_id
            inv_date = inv.date_invoice
            inv_type = False
            if inv.type in ('out_invoice', 'out_refund'):
                if inv.state == 'cancel':
                    inv_type = 2
                elif inv.amount_total < 0:
                    inv_type = 1
                elif inv.journal_id.sequence_type == 'autoinv1':
                    inv_type = 3
            elif inv.journal_id.sequence_type == 'autoinv2':
                inv_type = 4
            if inv_type:
                for line in inv.invoice_line:
                    cotas = [tax for tax in line.invoice_line_tax_id]
                    for cota in cotas:
                        cota_amount = 0
                        if cota.type == 'percent':
                            if cota.child_ids:
                                cota_amount = int(
                                    abs(cota.child_ids[0].amount) * 100)
                            else:
                                cota_amount = int(cota.amount * 100)
                        elif cota.type == 'amount':
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
        pass


class Informatii(models.AbstractModel):
    _description = "informatii"
    _name = "D394.30.informatii"
    _inherit = "anaf.mixin"
    _generateds_type = "InformatiiType"
    _concrete_rec_name = "D39430_nrCui1"

    D39430_nrCui1 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui1", xsd_required=True
    )
    D39430_nrCui2 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui2", xsd_required=True
    )
    D39430_nrCui3 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui3", xsd_required=True
    )
    D39430_nrCui4 = fields.Many2one(
        "D394.30.intpoz15stype", string="nrCui4", xsd_required=True
    )
    D39430_nr_BF_i1 = fields.Many2one(
        "D394.30.intpoz15stype", string="nr_BF_i1", xsd_required=True
    )
    D39430_incasari_i1 = fields.Integer(
        string="incasari_i1", xsd_required=True, xsd_type="integer"
    )
    D39430_incasari_i2 = fields.Integer(
        string="incasari_i2", xsd_required=True, xsd_type="integer"
    )
    D39430_nrFacturi_terti = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi_terti", xsd_required=True
    )
    D39430_nrFacturi_benef = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi_benef", xsd_required=True
    )
    D39430_nrFacturi = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturi", xsd_required=True
    )
    D39430_nrFacturiL_PF = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiL_PF", xsd_required=True
    )
    D39430_nrFacturiLS_PF = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiLS_PF", xsd_required=True
    )
    D39430_val_LS_PF = fields.Integer(
        string="val_LS_PF", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaDed24 = fields.Integer(string="tvaDed24", xsd_type="integer")
    D39430_tvaDed20 = fields.Integer(string="tvaDed20", xsd_type="integer")
    D39430_tvaDed19 = fields.Integer(string="tvaDed19", xsd_type="integer")
    D39430_tvaDed9 = fields.Integer(string="tvaDed9", xsd_type="integer")
    D39430_tvaDed5 = fields.Integer(string="tvaDed5", xsd_type="integer")
    D39430_tvaDedAI24 = fields.Integer(
        string="tvaDedAI24", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaDedAI20 = fields.Integer(
        string="tvaDedAI20", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaDedAI19 = fields.Integer(
        string="tvaDedAI19", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaDedAI9 = fields.Integer(
        string="tvaDedAI9", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaDedAI5 = fields.Integer(
        string="tvaDedAI5", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaCol24 = fields.Integer(string="tvaCol24", xsd_type="integer")
    D39430_tvaCol20 = fields.Integer(string="tvaCol20", xsd_type="integer")
    D39430_tvaCol19 = fields.Integer(string="tvaCol19", xsd_type="integer")
    D39430_tvaCol9 = fields.Integer(string="tvaCol9", xsd_type="integer")
    D39430_tvaCol5 = fields.Integer(string="tvaCol5", xsd_type="integer")
    D39430_incasari_ag = fields.Integer(string="incasari_ag", xsd_type="integer")
    D39430_costuri_ag = fields.Integer(string="costuri_ag", xsd_type="integer")
    D39430_marja_ag = fields.Integer(string="marja_ag", xsd_type="integer")
    D39430_tva_ag = fields.Integer(string="tva_ag", xsd_type="integer")
    D39430_pret_vanzare = fields.Integer(string="pret_vanzare", xsd_type="integer")
    D39430_pret_cumparare = fields.Integer(string="pret_cumparare", xsd_type="integer")
    D39430_marja_antic = fields.Integer(string="marja_antic", xsd_type="integer")
    D39430_tva_antic = fields.Integer(string="tva_antic", xsd_type="integer")
    D39430_solicit = fields.Integer(
        string="solicit", xsd_required=True, xsd_type="integer"
    )
    D39430_achizitiiPE = fields.Integer(string="achizitiiPE", xsd_type="integer")
    D39430_achizitiiCR = fields.Integer(string="achizitiiCR", xsd_type="integer")
    D39430_achizitiiCB = fields.Integer(string="achizitiiCB", xsd_type="integer")
    D39430_achizitiiCI = fields.Integer(string="achizitiiCI", xsd_type="integer")
    D39430_achizitiiA = fields.Integer(string="achizitiiA", xsd_type="integer")
    D39430_achizitiiB24 = fields.Integer(string="achizitiiB24", xsd_type="integer")
    D39430_achizitiiB20 = fields.Integer(string="achizitiiB20", xsd_type="integer")
    D39430_achizitiiB19 = fields.Integer(string="achizitiiB19", xsd_type="integer")
    D39430_achizitiiB9 = fields.Integer(string="achizitiiB9", xsd_type="integer")
    D39430_achizitiiB5 = fields.Integer(string="achizitiiB5", xsd_type="integer")
    D39430_achizitiiS24 = fields.Integer(string="achizitiiS24", xsd_type="integer")
    D39430_achizitiiS20 = fields.Integer(string="achizitiiS20", xsd_type="integer")
    D39430_achizitiiS19 = fields.Integer(string="achizitiiS19", xsd_type="integer")
    D39430_achizitiiS9 = fields.Integer(string="achizitiiS9", xsd_type="integer")
    D39430_achizitiiS5 = fields.Integer(string="achizitiiS5", xsd_type="integer")
    D39430_importB = fields.Integer(string="importB", xsd_type="integer")
    D39430_acINecorp = fields.Integer(string="acINecorp", xsd_type="integer")
    D39430_livrariBI = fields.Integer(string="livrariBI", xsd_type="integer")
    D39430_BUN24 = fields.Integer(string="BUN24", xsd_type="integer")
    D39430_BUN20 = fields.Integer(string="BUN20", xsd_type="integer")
    D39430_BUN19 = fields.Integer(string="BUN19", xsd_type="integer")
    D39430_BUN9 = fields.Integer(string="BUN9", xsd_type="integer")
    D39430_BUN5 = fields.Integer(string="BUN5", xsd_type="integer")
    D39430_valoareScutit = fields.Integer(string="valoareScutit", xsd_type="integer")
    D39430_BunTI = fields.Integer(string="BunTI", xsd_type="integer")
    D39430_Prest24 = fields.Integer(string="Prest24", xsd_type="integer")
    D39430_Prest20 = fields.Integer(string="Prest20", xsd_type="integer")
    D39430_Prest19 = fields.Integer(string="Prest19", xsd_type="integer")
    D39430_Prest9 = fields.Integer(string="Prest9", xsd_type="integer")
    D39430_Prest5 = fields.Integer(string="Prest5", xsd_type="integer")
    D39430_PrestScutit = fields.Integer(string="PrestScutit", xsd_type="integer")
    D39430_LIntra = fields.Integer(string="LIntra", xsd_type="integer")
    D39430_PrestIntra = fields.Integer(string="PrestIntra", xsd_type="integer")
    D39430_Export = fields.Integer(string="Export", xsd_type="integer")
    D39430_livINecorp = fields.Integer(string="livINecorp", xsd_type="integer")
    D39430_efectuat = fields.Integer(string="efectuat", xsd_type="integer")

    def generate_informatii(self):
        pass


class Lista(models.AbstractModel):
    _description = "lista"
    _name = "D394.30.lista"
    _inherit = "anaf.mixin"
    _generateds_type = "ListaType"
    _concrete_rec_name = "D39430_caen"

    D39430_lista_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_caen = fields.Many2one(
        "D394.30.int_listacaenstype", string="caen", xsd_required=True
    )
    D39430_cota = fields.Many2one(
        "D394.30.int_cotetva2stype", string="cota", xsd_required=True
    )
    D39430_operat = fields.Many2one(
        "D394.30.intint1_2stype", string="operat", xsd_required=True
    )
    D39430_valoare = fields.Integer(
        string="valoare", xsd_required=True, xsd_type="integer"
    )
    D39430_tva = fields.Integer(string="tva", xsd_required=True, xsd_type="integer")




class Op11(models.AbstractModel):
    _description = "op11"
    _name = "D394.30.op11"
    _inherit = "anaf.mixin"
    _generateds_type = "Op11Type"
    _concrete_rec_name = "D39430_nrFactPR"

    D39430_op11_Op1_id = fields.Many2one("D394.30.op1")
    D39430_nrFactPR = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFactPR", xsd_required=True
    )
    D39430_codPR = fields.Many2one(
        "D394.30.str_listacodprstype", string="codPR", xsd_required=True
    )
    D39430_bazaPR = fields.Integer(
        string="bazaPR", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaPR = fields.Integer(string="tvaPR", xsd_type="integer")


class Op1(models.AbstractModel):
    _description = "op1"
    _name = "D394.30.op1"
    _inherit = "anaf.mixin"
    _generateds_type = "Op1Type"
    _concrete_rec_name = "D39430_tip"

    D39430_op1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_tip = fields.Many2one(
        "D394.30.str_listatipoperatiestype", string="tip", xsd_required=True
    )
    D39430_tip_partener = fields.Many2one(
        "D394.30.int_tippartenerop1stype", string="tip_partener", xsd_required=True
    )
    D39430_cota = fields.Many2one(
        "D394.30.int_cotetvastype", string="cota", xsd_required=True
    )
    D39430_cuiP = fields.Char(string="cuiP", xsd_type="string")
    D39430_denP = fields.Char(string="denP", xsd_required=True, xsd_type="string")
    D39430_taraP = fields.Many2one("D394.30.str_listataristype", string="taraP")
    D39430_locP = fields.Char(string="locP", xsd_type="string")
    D39430_judP = fields.Many2one("D394.30.str_listajudstype", string="judP")
    D39430_strP = fields.Char(string="strP", xsd_type="string")
    D39430_nrP = fields.Char(string="nrP", xsd_type="string")
    D39430_blP = fields.Char(string="blP", xsd_type="string")
    D39430_apP = fields.Char(string="apP", xsd_type="string")
    D39430_detP = fields.Many2one("D394.30.str100", string="detP")
    D39430_tip_document = fields.Many2one(
        "D394.30.intint1_5stype", string="tip_document"
    )
    D39430_nrFact = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFact", xsd_required=True
    )
    D39430_baza = fields.Integer(string="baza", xsd_required=True, xsd_type="integer")
    D39430_tva = fields.Integer(string="tva", xsd_type="integer")
    D39430_op11 = fields.One2many("D394.30.op11", "D39430_op11_Op1_id", string="op11")


class Op2(models.AbstractModel):
    _description = "op2"
    _name = "D394.30.op2"
    _inherit = "anaf.mixin"
    _generateds_type = "Op2Type"
    _concrete_rec_name = "D39430_tip_op2"

    D39430_op2_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_tip_op2 = fields.Many2one(
        "D394.30.str_tipoperatiestype", string="tip_op2", xsd_required=True
    )
    D39430_luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    D39430_nrAMEF = fields.Many2one("D394.30.intpoz4stype", string="nrAMEF")
    D39430_nrBF = fields.Many2one("D394.30.intpoz15stype", string="nrBF")
    D39430_total = fields.Many2one(
        "D394.30.intpoz15stype", string="total", xsd_required=True
    )
    D39430_baza20 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza20", xsd_required=True
    )
    D39430_baza9 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza9", xsd_required=True
    )
    D39430_baza5 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza5", xsd_required=True
    )
    D39430_TVA20 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA20", xsd_required=True
    )
    D39430_TVA9 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA9", xsd_required=True
    )
    D39430_TVA5 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA5", xsd_required=True
    )
    D39430_baza19 = fields.Many2one(
        "D394.30.intpoz15stype", string="baza19", xsd_required=True
    )
    D39430_TVA19 = fields.Many2one(
        "D394.30.intpoz15stype", string="TVA19", xsd_required=True
    )


class Rezumat1(models.AbstractModel):
    _description = "rezumat1"
    _name = "D394.30.rezumat1"
    _inherit = "anaf.mixin"
    _generateds_type = "Rezumat1Type"
    _concrete_rec_name = "D39430_tip_partener"

    D39430_rezumat1_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_tip_partener = fields.Many2one(
        "D394.30.int_tippartenerstype", string="tip_partener", xsd_required=True
    )
    D39430_cota = fields.Many2one(
        "D394.30.int_cotetvastype", string="cota", xsd_required=True
    )
    D39430_facturiL = fields.Many2one("D394.30.intpoz15stype", string="facturiL")
    D39430_bazaL = fields.Integer(string="bazaL", xsd_type="integer")
    D39430_tvaL = fields.Integer(string="tvaL", xsd_type="integer")
    D39430_facturiLS = fields.Many2one("D394.30.intpoz15stype", string="facturiLS")
    D39430_bazaLS = fields.Integer(string="bazaLS", xsd_type="integer")
    D39430_facturiA = fields.Many2one("D394.30.intpoz15stype", string="facturiA")
    D39430_bazaA = fields.Integer(string="bazaA", xsd_type="integer")
    D39430_tvaA = fields.Integer(string="tvaA", xsd_type="integer")
    D39430_facturiAI = fields.Many2one("D394.30.intpoz15stype", string="facturiAI")
    D39430_bazaAI = fields.Integer(string="bazaAI", xsd_type="integer")
    D39430_tvaAI = fields.Integer(string="tvaAI", xsd_type="integer")
    D39430_facturiAS = fields.Many2one("D394.30.intpoz15stype", string="facturiAS")
    D39430_bazaAS = fields.Integer(string="bazaAS", xsd_type="integer")
    D39430_facturiV = fields.Many2one("D394.30.intpoz15stype", string="facturiV")
    D39430_bazaV = fields.Integer(string="bazaV", xsd_type="integer")
    D39430_facturiC = fields.Many2one("D394.30.intpoz15stype", string="facturiC")
    D39430_bazaC = fields.Integer(string="bazaC", xsd_type="integer")
    D39430_tvaC = fields.Integer(string="tvaC", xsd_type="integer")
    D39430_facturiN = fields.Many2one("D394.30.intpoz15stype", string="facturiN")
    D39430_document_N = fields.Many2one("D394.30.intint1_5stype", string="document_N")
    D39430_bazaN = fields.Integer(string="bazaN", xsd_type="integer")
    D39430_detaliu = fields.One2many(
        "D394.30.detaliu", "D39430_detaliu_Rezumat1_id", string="detaliu"
    )


class Rezumat2(models.AbstractModel):
    _description = "rezumat2"
    _name = "D394.30.rezumat2"
    _inherit = "anaf.mixin"
    _generateds_type = "Rezumat2Type"
    _concrete_rec_name = "D39430_cota"

    D39430_rezumat2_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_cota = fields.Many2one("D394.30.int_cotetva2stype", string="cota")
    D39430_bazaFSLcod = fields.Integer(
        string="bazaFSLcod", xsd_required=True, xsd_type="integer"
    )
    D39430_TVAFSLcod = fields.Integer(
        string="TVAFSLcod", xsd_required=True, xsd_type="integer"
    )
    D39430_bazaFSL = fields.Integer(
        string="bazaFSL", xsd_required=True, xsd_type="integer"
    )
    D39430_TVAFSL = fields.Integer(
        string="TVAFSL", xsd_required=True, xsd_type="integer"
    )
    D39430_bazaFSA = fields.Integer(
        string="bazaFSA", xsd_required=True, xsd_type="integer"
    )
    D39430_TVAFSA = fields.Integer(
        string="TVAFSA", xsd_required=True, xsd_type="integer"
    )
    D39430_bazaFSAI = fields.Integer(
        string="bazaFSAI", xsd_required=True, xsd_type="integer"
    )
    D39430_TVAFSAI = fields.Integer(
        string="TVAFSAI", xsd_required=True, xsd_type="integer"
    )
    D39430_bazaBFAI = fields.Integer(
        string="bazaBFAI", xsd_required=True, xsd_type="integer"
    )
    D39430_TVABFAI = fields.Integer(
        string="TVABFAI", xsd_required=True, xsd_type="integer"
    )
    D39430_nrFacturiL = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiL", xsd_required=True
    )
    D39430_bazaL = fields.Integer(string="bazaL", xsd_required=True, xsd_type="integer")
    D39430_tvaL = fields.Integer(string="tvaL", xsd_required=True, xsd_type="integer")
    D39430_nrFacturiA = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiA", xsd_required=True
    )
    D39430_bazaA = fields.Integer(string="bazaA", xsd_required=True, xsd_type="integer")
    D39430_tvaA = fields.Integer(string="tvaA", xsd_required=True, xsd_type="integer")
    D39430_nrFacturiAI = fields.Many2one(
        "D394.30.intpoz15stype", string="nrFacturiAI", xsd_required=True
    )
    D39430_bazaAI = fields.Integer(
        string="bazaAI", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaAI = fields.Integer(string="tvaAI", xsd_required=True, xsd_type="integer")
    D39430_baza_incasari_i1 = fields.Integer(
        string="baza_incasari_i1", xsd_type="integer"
    )
    D39430_tva_incasari_i1 = fields.Integer(
        string="tva_incasari_i1", xsd_type="integer"
    )
    D39430_baza_incasari_i2 = fields.Integer(
        string="baza_incasari_i2", xsd_type="integer"
    )
    D39430_tva_incasari_i2 = fields.Integer(
        string="tva_incasari_i2", xsd_type="integer"
    )
    D39430_bazaL_PF = fields.Integer(
        string="bazaL_PF", xsd_required=True, xsd_type="integer"
    )
    D39430_tvaL_PF = fields.Integer(
        string="tvaL_PF", xsd_required=True, xsd_type="integer"
    )


class SerieFacturi(models.AbstractModel):
    _description = "seriefacturi"
    _name = "D394.30.seriefacturi"
    _inherit = "anaf.mixin"
    _generateds_type = "SerieFacturiType"
    _concrete_rec_name = "D39430_tip"

    D39430_serieFacturi_Declaratie394_id = fields.Many2one("D394.30.declaratie394")
    D39430_tip = fields.Many2one(
        "D394.30.intint1_4stype", string="tip", xsd_required=True
    )
    D39430_serieI = fields.Many2one("D394.30.str20", string="serieI")
    D39430_nrI = fields.Many2one("D394.30.str20", string="nrI", xsd_required=True)
    D39430_nrF = fields.Many2one("D394.30.str20", string="nrF")
    D39430_den = fields.Many2one("D394.30.str100", string="den")
    D39430_cui = fields.Char(string="cui", xsd_type="token")
