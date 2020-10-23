# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Sun Oct 18 11:10:42 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Declaratie300(models.TransientModel):
    _name = "anaf.d300.v60"
    _inherit = "anaf.mixin"
    _description = "Declaratie D300, versiunea 6"

    luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    bifa_interne = fields.Integer(
        string="bifa_interne", xsd_required=True, xsd_type="integer"
    )
    temei = fields.Integer(string="temei", xsd_required=True, xsd_type="integer")
    nume_declar = fields.Char(
        string="nume_declar", xsd_required=True, xsd_type="string"
    )
    prenume_declar = fields.Char(
        string="prenume_declar", xsd_required=True, xsd_type="string"
    )
    functie_declar = fields.Char(
        string="functie_declar", xsd_required=True, xsd_type="string"
    )
    cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    telefon = fields.Char(string="telefon", xsd_type="string")
    fax = fields.Char(string="fax", xsd_type="string")
    mail = fields.Char(string="mail", xsd_type="token")
    banca = fields.Char(string="banca", xsd_required=True, xsd_type="string")
    cont = fields.Char(string="cont", xsd_required=True, xsd_type="string")
    caen = fields.Char(string="caen", xsd_required=True, xsd_type="string")
    tip_decont = fields.Char(
        string="tip_decont", xsd_required=True, xsd_type="string"
    )
    pro_rata = fields.Float(
        string="pro_rata", xsd_required=True, xsd_type="double"
    )
    bifa_cereale = fields.Char(
        string="bifa_cereale", xsd_required=True, xsd_type="string"
    )
    bifa_mob = fields.Char(
        string="bifa_mob", xsd_required=True, xsd_type="string"
    )
    bifa_disp = fields.Char(
        string="bifa_disp", xsd_required=True, xsd_type="string"
    )
    bifa_cons = fields.Char(
        string="bifa_cons", xsd_required=True, xsd_type="string"
    )
    solicit_ramb = fields.Char(
        string="solicit_ramb", xsd_required=True, xsd_type="string"
    )
    nr_evid = fields.Integer(
        string="nr_evid", xsd_required=True, xsd_type="integer"
    )
    totalPlata_A = fields.Integer(
        string="totalPlata_A", xsd_required=True, xsd_type="integer"
    )
    R1_1 = fields.Integer(string="R1_1", xsd_type="integer")
    R2_1 = fields.Integer(string="R2_1", xsd_type="integer")
    R3_1 = fields.Integer(string="R3_1", xsd_type="integer")
    R3_1_1 = fields.Integer(string="R3_1_1", xsd_type="integer")
    R4_1 = fields.Integer(string="R4_1", xsd_type="integer")
    R5_1 = fields.Integer(string="R5_1", xsd_type="integer")
    R5_2 = fields.Integer(string="R5_2", xsd_type="integer")
    R5_1_1 = fields.Integer(string="R5_1_1", xsd_type="integer")
    R5_1_2 = fields.Integer(string="R5_1_2", xsd_type="integer")
    R6_1 = fields.Integer(string="R6_1", xsd_type="integer")
    R6_2 = fields.Integer(string="R6_2", xsd_type="integer")
    R7_1 = fields.Integer(string="R7_1", xsd_type="integer")
    R7_2 = fields.Integer(string="R7_2", xsd_type="integer")
    R7_1_1 = fields.Integer(string="R7_1_1", xsd_type="integer")
    R7_1_2 = fields.Integer(string="R7_1_2", xsd_type="integer")
    R8_1 = fields.Integer(string="R8_1", xsd_type="integer")
    R8_2 = fields.Integer(string="R8_2", xsd_type="integer")
    R9_1 = fields.Integer(string="R9_1", xsd_type="integer")
    R9_2 = fields.Integer(string="R9_2", xsd_type="integer")
    R10_1 = fields.Integer(string="R10_1", xsd_type="integer")
    R10_2 = fields.Integer(string="R10_2", xsd_type="integer")
    R11_1 = fields.Integer(string="R11_1", xsd_type="integer")
    R11_2 = fields.Integer(string="R11_2", xsd_type="integer")
    R12_1 = fields.Integer(string="R12_1", xsd_type="integer")
    R12_2 = fields.Integer(string="R12_2", xsd_type="integer")
    R12_1_1 = fields.Integer(string="R12_1_1", xsd_type="integer")
    R12_1_2 = fields.Integer(string="R12_1_2", xsd_type="integer")
    R12_2_1 = fields.Integer(string="R12_2_1", xsd_type="integer")
    R12_2_2 = fields.Integer(string="R12_2_2", xsd_type="integer")
    R12_3_1 = fields.Integer(string="R12_3_1", xsd_type="integer")
    R12_3_2 = fields.Integer(string="R12_3_2", xsd_type="integer")
    R13_1 = fields.Integer(string="R13_1", xsd_type="integer")
    R14_1 = fields.Integer(string="R14_1", xsd_type="integer")
    R15_1 = fields.Integer(string="R15_1", xsd_type="integer")
    R16_1 = fields.Integer(string="R16_1", xsd_type="integer")
    R16_2 = fields.Integer(string="R16_2", xsd_type="integer")
    R17_1 = fields.Integer(string="R17_1", xsd_type="integer")
    R17_2 = fields.Integer(string="R17_2", xsd_type="integer")
    R18_1 = fields.Integer(string="R18_1", xsd_type="integer")
    R18_2 = fields.Integer(string="R18_2", xsd_type="integer")
    R18_1_1 = fields.Integer(string="R18_1_1", xsd_type="integer")
    R18_1_2 = fields.Integer(string="R18_1_2", xsd_type="integer")
    R19_1 = fields.Integer(string="R19_1", xsd_type="integer")
    R19_2 = fields.Integer(string="R19_2", xsd_type="integer")
    R20_1 = fields.Integer(string="R20_1", xsd_type="integer")
    R20_2 = fields.Integer(string="R20_2", xsd_type="integer")
    R20_1_1 = fields.Integer(string="R20_1_1", xsd_type="integer")
    R20_1_2 = fields.Integer(string="R20_1_2", xsd_type="integer")
    R21_1 = fields.Integer(string="R21_1", xsd_type="integer")
    R21_2 = fields.Integer(string="R21_2", xsd_type="integer")
    R22_1 = fields.Integer(string="R22_1", xsd_type="integer")
    R22_2 = fields.Integer(string="R22_2", xsd_type="integer")
    R23_1 = fields.Integer(string="R23_1", xsd_type="integer")
    R23_2 = fields.Integer(string="R23_2", xsd_type="integer")
    R24_1 = fields.Integer(string="R24_1", xsd_type="integer")
    R24_2 = fields.Integer(string="R24_2", xsd_type="integer")
    R25_1 = fields.Integer(string="R25_1", xsd_type="integer")
    R25_2 = fields.Integer(string="R25_2", xsd_type="integer")
    R25_1_1 = fields.Integer(string="R25_1_1", xsd_type="integer")
    R25_1_2 = fields.Integer(string="R25_1_2", xsd_type="integer")
    R25_2_1 = fields.Integer(string="R25_2_1", xsd_type="integer")
    R25_2_2 = fields.Integer(string="R25_2_2", xsd_type="integer")
    R25_3_1 = fields.Integer(string="R25_3_1", xsd_type="integer")
    R25_3_2 = fields.Integer(string="R25_3_2", xsd_type="integer")
    R43_2 = fields.Integer(string="R43_2", xsd_type="integer")
    R44_2 = fields.Integer(string="R44_2", xsd_type="integer")
    R26_1 = fields.Integer(string="R26_1", xsd_type="integer")
    R26_1_1 = fields.Integer(string="R26_1_1", xsd_type="integer")
    R27_1 = fields.Integer(string="R27_1", xsd_type="integer")
    R27_2 = fields.Integer(string="R27_2", xsd_type="integer")
    R29_2 = fields.Integer(string="R29_2", xsd_type="integer")
    R30_1 = fields.Integer(string="R30_1", xsd_type="integer")
    R30_2 = fields.Integer(string="R30_2", xsd_type="integer")
    R31_2 = fields.Integer(string="R31_2", xsd_type="integer")
    R32_2 = fields.Integer(string="R32_2", xsd_type="integer")
    R33_2 = fields.Integer(string="R33_2", xsd_type="integer")
    R34_2 = fields.Integer(string="R34_2", xsd_type="integer")
    R35_2 = fields.Integer(string="R35_2", xsd_type="integer")
    R37_2 = fields.Integer(string="R37_2", xsd_type="integer")
    R38_2 = fields.Integer(string="R38_2", xsd_type="integer")
    R40_2 = fields.Integer(string="R40_2", xsd_type="integer")
    R41_2 = fields.Integer(string="R41_2", xsd_type="integer")
    R42_2 = fields.Integer(string="R42_2", xsd_type="integer")
    nr_facturi = fields.Integer(string="nr_facturi", xsd_type="integer")
    baza = fields.Integer(string="baza", xsd_type="integer")
    tva = fields.Integer(string="tva", xsd_type="integer")
    nr_facturi_primite = fields.Integer(
        string="nr_facturi_primite", xsd_type="integer"
    )
    baza_primite = fields.Integer(string="baza_primite", xsd_type="integer")
    tva_primite = fields.Integer(string="tva_primite", xsd_type="integer")
    valoare_a = fields.Integer(string="valoare_a", xsd_type="integer")
    valoare_a1 = fields.Integer(string="valoare_a1", xsd_type="integer")
    tva_a = fields.Integer(string="tva_a", xsd_type="integer")
    tva_a1 = fields.Integer(string="tva_a1", xsd_type="integer")
    valoare_b = fields.Integer(string="valoare_b", xsd_type="integer")
    valoare_b1 = fields.Integer(string="valoare_b1", xsd_type="integer")
    tva_b = fields.Integer(string="tva_b", xsd_type="integer")
    tva_b1 = fields.Integer(string="tva_b1", xsd_type="integer")
    nr_fact_emise = fields.Integer(string="nr_fact_emise", xsd_type="integer")
    total_baza = fields.Integer(string="total_baza", xsd_type="integer")
    total_tva = fields.Integer(string="total_tva", xsd_type="integer")
    cuiSuccesor = fields.Char(string="cuiSuccesor", xsd_type="token")
    R64_1 = fields.Integer(string="R64_1", xsd_type="integer")
    R64_2 = fields.Integer(string="R64_2", xsd_type="integer")
    R65_1 = fields.Integer(string="R65_1", xsd_type="integer")
    R65_2 = fields.Integer(string="R65_2", xsd_type="integer")
    total_precedent = fields.Integer(
        string="total_precedent", xsd_type="integer"
    )
    total_curent = fields.Integer(string="total_curent", xsd_type="integer")

    # New fields not from schema
    nr_evid = fields.Char()
    succesor_id = fields.Many2one(
        "res.partner",
        string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din "
        "Legea nr.207/2015 privind Codul de procedură fiscală",
    )
    R28_2 = fields.Integer(string="R28_2")
    R35_2_old = fields.Integer(string="Previous R35_2")
    R42_2_old = fields.Integer(string="Previous R42_2")
    R36_2 = fields.Integer(string="R36_2")
    R39_2 = fields.Integer(string="R39_2")

    def build_file(self):
        year, month = self.get_year_month()
        data_file = """<?xml version="1.0" encoding="UTF-8"?>
        <declaratie300 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="mfp:anaf:dgti:d300:declaratie:v6 D300.xsd"
        xmlns="mfp:anaf:dgti:d300:declaratie:v6" """
        xmldict = {
            "luna": month,
            "an": year,
            "nr_evid": self.nr_evid,
            "cuiSuccesor": self.succesor_id.vat_number,
        }
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)

        # vat_report_totals = self.generate_total(vat_report)
        # xmldict.update(vat_report_totals)
        for key, val in xmldict.items():
            data_file += """%s="%s" """ % (key, val)
        data_file += """ />"""
        return data_file

    def generate_company_data(self):
        data = {
            "cui": self.company_id.partner_id.vat_number,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(
                without_company=False).replace("\n", ","),
            "telefon": self.company_id.phone,
            "mail": self.company_id.email,
            "banca": self.bank_account_id.bank_id.name,
            "cont": self.bank_account_id.acc_number,
            "caen": self.company_id.caen_code,
        }
        return data

    def generate_sign(self):
        signer = self.signature_id
        data = {
            "nume_declar": signer.first_name,
            "prenume_declar": signer.last_name,
            "functie_declar": signer.function,
        }
        return data

    def get_amount(self, vat_report, tag, value):
        tag = filter(lambda entry: entry['name'] == tag, vat_report)
        sign = 1
        for key, value in tag.items():
            if type(key) == int:
                if value.get("type_tax_use", "purchase") == "sale":
                    sign = -1
                    continue
        return sign * tag.get(value, 0)

    def generate_data(self):
        self.ensure_one()
        report_obj = self.env["report.account_financial_report.vat_report"]
        vat_report_data, tax_data = report_obj._get_vat_report_data(
            self.company_id.id, self.date_from, self.date_to, True
        )
        vat_report = report_obj._get_vat_report_tag_data(
            vat_report_data, tax_data, False
        )
        print(vat_report)
        data = {
            "R1_1": self.get_amount(vat_report, "+01 - BAZA", "net"),
            "R2_1": self.get_amount(vat_report, "+02 - BAZA", "net"),
            "R3_1": self.get_amount(vat_report, "+03 - BAZA", "net"),
            "R3_1_1": self.get_amount(vat_report, "+03_1 - BAZA", "net"),
            "R4_1": self.get_amount(vat_report, "+04 - BAZA", "net"),
            "R5_1": self.get_amount(vat_report, "+05 - BAZA", "net"),
            "R5_2": self.get_amount(vat_report, "+05 - TVA", "tax"),
            "R5_1_1": self.get_amount(vat_report, "+05_1 - BAZA", "net"),
            "R5_1_2": self.get_amount(vat_report, "+05_1 - TVA", "tax"),
            "R6_1": self.get_amount(vat_report, "+06 - BAZA", "net"),
            "R6_2": self.get_amount(vat_report, "+06 - TVA", "tax"),
            "R7_1": self.get_amount(vat_report, "+07 - BAZA", "net"),
            "R7_2": self.get_amount(vat_report, "+07 - TVA", "tax"),
            "R7_1_1": self.get_amount(vat_report, "+07_1 - BAZA", "net"),
            "R7_1_2": self.get_amount(vat_report, "+07_1 - TVA", "tax"),
            "R8_1": self.get_amount(vat_report, "+08 - BAZA", "net"),
            "R8_2": self.get_amount(vat_report, "+08 - TVA", "tax"),
            "R9_1": self.get_amount(vat_report, "+09_1 - BAZA", "net") +
                    self.get_amount(vat_report, "+09_2 - BAZA", "net"),
            "R9_2": self.get_amount(vat_report, "+09_1 - TVA", "tax") +
                    self.get_amount(vat_report, "+09_2 - TVA", "tax"),
            "R10_1": self.get_amount(vat_report, "+10_1 - BAZA", "net") +
                     self.get_amount(vat_report, "+10_2 - BAZA", "net"),
            "R10_2": self.get_amount(vat_report, "+10_1 - TVA", "tax") +
                     self.get_amount(vat_report, "+10_2 - TVA", "tax"),
            "R11_1": self.get_amount(vat_report, "+11_1 - BAZA", "net") +
                     self.get_amount(vat_report, "+11_2 - BAZA", "net"),
            "R11_2": self.get_amount(vat_report, "+11_1 - TVA", "tax") +
                     self.get_amount(vat_report, "+11_2 - TVA", "tax"),
            "R12_1": self.get_amount(vat_report, "+12 - BAZA", "net"),
            "R12_2": self.get_amount(vat_report, "+12 - TVA", "tax"),
            "R12_1_1": self.get_amount(vat_report, "+12_1 - BAZA", "net"),
            "R12_1_2": self.get_amount(vat_report, "+12_1 - TVA", "tax"),
            "R12_2_1": self.get_amount(vat_report, "+12_2 - BAZA", "net"),
            "R12_2_2": self.get_amount(vat_report, "+12_2 - TVA", "tax"),
            "R12_3_1": self.get_amount(vat_report, "+12_3 - BAZA", "net"),
            "R12_3_2": self.get_amount(vat_report, "+12_3 - TVA", "tax"),
            "R13_1": self.get_amount(vat_report, "+13 - BAZA", "net"),
            "R14_1": self.get_amount(vat_report, "+14 - BAZA", "net"),
            "R15_1": self.get_amount(vat_report, "+15 - BAZA", "net"),
            "R16_1": self.get_amount(vat_report, "+16 - BAZA", "net"),
            "R16_2": self.get_amount(vat_report, "+16 - TVA", "tax"),
            "R64_1": self.get_amount(vat_report, "+17 - BAZA", "net"),
            "R64_2": self.get_amount(vat_report, "+17 - TVA", "tax"),
            "R65_1": self.get_amount(vat_report, "+18 - BAZA", "net"),
            "R65_2": self.get_amount(vat_report, "+18 - TVA", "tax"),
            # Purchases
            "R18_1": self.get_amount(vat_report, "+20 - BAZA", "net"),
            "R18_2": self.get_amount(vat_report, "+20 - TVA", "tax"),
            "R18_1_1": self.get_amount(vat_report, "+20_1 - BAZA", "net"),
            "R18_1_2": self.get_amount(vat_report, "+20_1 - TVA", "tax"),
            "R19_1": self.get_amount(vat_report, "+21 - BAZA", "net"),
            "R19_2": self.get_amount(vat_report, "+21 - TVA", "tax"),
            "R20_1": self.get_amount(vat_report, "+22 - BAZA", "net"),
            "R20_2": self.get_amount(vat_report, "+22 - TVA", "tax"),
            "R20_1_1": self.get_amount(vat_report, "+22_1 - BAZA", "net"),
            "R20_1_2": self.get_amount(vat_report, "+22_1 - TVA", "tax"),
            "R21_1": self.get_amount(vat_report, "+23 - BAZA", "net"),
            "R21_2": self.get_amount(vat_report, "+23 - TVA", "tax"),
            "R22_1": self.get_amount(vat_report, "+24 - BAZA", "net"),
            "R22_2": self.get_amount(vat_report, "+24 - TVA", "tax"),
            "R23_1": self.get_amount(vat_report, "+25 - BAZA", "net"),
            "R23_2": self.get_amount(vat_report, "+25 - TVA", "net"),
            "R24_1": self.get_amount(vat_report, "+26 - BAZA", "net"),
            "R24_2": self.get_amount(vat_report, "+26 - TVA", "tax"),
            "R25_1": self.get_amount(vat_report, "+27 - BAZA", "net") ,
            "R25_2": self.get_amount(vat_report, "+27 - TVA", "tax") ,
            "R25_1_1": self.get_amount(vat_report, "+27_1 - BAZA", "net"),
            "R25_1_2": self.get_amount(vat_report, "+27_1 - TVA", "tax"),
            "R25_2_1": self.get_amount(vat_report, "+27_2 - BAZA", "net"),
            "R25_2_2": self.get_amount(vat_report, "+27_2 - TVA", "tax"),
            "R25_3_1": self.get_amount(vat_report, "+27_3 - BAZA", "net"),
            "R25_3_2": self.get_amount(vat_report, "+27_3 - TVA", "tax"),
            "R26_1": self.get_amount(vat_report, "+30 - BAZA", "net"),
            "R26_1_1": self.get_amount(vat_report, "+30_1 - BAZA", "net"),
            "R29_2": self.get_amount(vat_report, "+33 - TVA", "tax"),
            # Regularization
            "R30_1": self.get_amount(vat_report, "+34 - BAZA", "net"),
            "R30_2": self.get_amount(vat_report, "+34 - TVA", "tax"),
            "R31_2": self.get_amount(vat_report, "+35 - TVA", "tax"),
        }
        data["R17_1"] = \
            data.get("R1_1") + data.get("R2_1") + data.get("R3_1") +\
            data.get("R4_1") + data.get("R5_1") + data.get("R6_1") +\
            data.get("R7_1") + data.get("R8_1") + data.get("R9_1") +\
            data.get("R10_1") + data.get("R11_1") + data.get("R12_1") +\
            data.get("R13_1") + data.get("R14_1") + data.get("R15_1") +\
            data.get("R16_1")
        data["R17_2"] = \
            data.get("R5_2") + data.get("R6_2") + data.get("R7_2") +\
            data.get("R8_2") + data.get("R9_2") + data.get("R10_2") +\
            data.get("R11_2") + data.get("R12_2") + data.get("R16_2")
        data["R27_1"] = \
            data.get("R18_1") + data.get("R19_1") + data.get("R20_1") + \
            data.get("R21_1") + data.get("R22_1") + data.get("R23_1") + \
            data.get("R24_1") + data.get("R25_1") + data.get("R26_1")
        data["R27_2"] = \
            data.get("R18_2") + data.get("R19_2") + data.get("R20_2") +\
            data.get("R21_2") + data.get("R22_2") + data.get("R23_2") +\
            data.get("R24_2") + data.get("R25_2") + data.get("R43_2") +\
            data.get("R44_2")
        data["R28_2"] = self.R28_2
        data["R32_2"] = data.get("R28_2") + data.get("R29_2") +\
                        data.get("R30_2") + data.get("R31_2")
        vat = data["R32_2"] - data["R17_2"]
        data["R33_2"] = vat if vat < 0 else 0
        data["R34_2"] = vat if vat > 0 else 0
        data["R35_2"] = 0 if self.R42_2_old > 0 else self.R35_2_old
        data["R36_2"] = self.R36_2
        data["R37_2"] = \
            data.get("R34_2") + data.get("R35_2") + data.get("R36_2")
        data["R38_2"] = 0 if self.R35_2_old > 0 else self.R42_2_old
        data["R39_2"] = self.R39_2
        data["R40_2"] = \
            data.get("R33_2") + data.get("R38_2") + data.get("R39_2")
        vat_result = data.get("R37_2") - data.get("R40_2")
        data["R41_2"] = vat_result if vat_result > 0 else 0
        data["R42_2"] = -1 * vat_result if vat_result < 0 else 0
        return data

    def generate_total(self):
        self.ensure_one()
        data = {}
        # data = {
        #     "nr_facturi":
        #     "baza":
        #     "tva":
        #     "nr_facturi_primite":
        #     "baza_primite":
        #     "tva_primite":
        #     "valoare_a":
        #     "valoare_a1":
        #     "tva_a":
        #     "tva_a1":
        #     "valoare_b":
        #     "valoare_b1":
        #     "tva_b":
        #     "tva_b1":
        #     "nr_fact_emise":
        #     "total_baza":
        #     "total_tva":
        # }
        return data
