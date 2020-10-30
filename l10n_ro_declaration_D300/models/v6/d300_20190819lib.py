# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Sun Oct 18 11:10:42 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Declaratie300(models.TransientModel):
    _name = "anaf.d300.v60"
    _inherit = "anaf.mixin"
    _description = "Declaratie D300, versiunea 6"

    luna = fields.Integer(string="luna")
    an = fields.Integer(string="an")
    bifa_interne = fields.Integer(string="bifa_interne", default=1)
    temei = fields.Integer(string="temei", default=0)
    nume_declar = fields.Char(string="nume_declar")
    prenume_declar = fields.Char(string="prenume_declar")
    functie_declar = fields.Char(string="functie_declar")
    cui = fields.Char(string="cui")
    den = fields.Char(string="den")
    adresa = fields.Char(string="adresa")
    telefon = fields.Char(string="telefon")
    fax = fields.Char(string="fax")
    mail = fields.Char(string="mail")
    banca = fields.Char(string="banca")
    cont = fields.Char(string="cont")
    caen = fields.Char(string="caen")
    tip_decont = fields.Char(string="tip_decont", default="L")
    pro_rata = fields.Float(string="pro_rata")
    bifa_cereale = fields.Char(string="bifa_cereale", default="N")
    bifa_mob = fields.Char(string="bifa_mob", default="N")
    bifa_disp = fields.Char(string="bifa_disp", default="N")
    bifa_cons = fields.Char(string="bifa_cons", default="N")
    solicit_ramb = fields.Char(string="solicit_ramb", default="N")
    nr_evid = fields.Char(string="nr_evid", default="123456")
    totalPlata_A = fields.Integer(string="totalPlata_A", default=0)
    R1_1 = fields.Integer(string="R1_1", default=0)
    R2_1 = fields.Integer(string="R2_1", default=0)
    R3_1 = fields.Integer(string="R3_1", default=0)
    R3_1_1 = fields.Integer(string="R3_1_1", default=0)
    R4_1 = fields.Integer(string="R4_1", default=0)
    R5_1 = fields.Integer(string="R5_1", default=0)
    R5_2 = fields.Integer(string="R5_2", default=0)
    R5_1_1 = fields.Integer(string="R5_1_1", default=0)
    R5_1_2 = fields.Integer(string="R5_1_2", default=0)
    R6_1 = fields.Integer(string="R6_1", default=0)
    R6_2 = fields.Integer(string="R6_2", default=0)
    R7_1 = fields.Integer(string="R7_1", default=0)
    R7_2 = fields.Integer(string="R7_2", default=0)
    R7_1_1 = fields.Integer(string="R7_1_1", default=0)
    R7_1_2 = fields.Integer(string="R7_1_2", default=0)
    R8_1 = fields.Integer(string="R8_1", default=0)
    R8_2 = fields.Integer(string="R8_2", default=0)
    R9_1 = fields.Integer(string="R9_1", default=0)
    R9_2 = fields.Integer(string="R9_2", default=0)
    R10_1 = fields.Integer(string="R10_1", default=0)
    R10_2 = fields.Integer(string="R10_2", default=0)
    R11_1 = fields.Integer(string="R11_1", default=0)
    R11_2 = fields.Integer(string="R11_2", default=0)
    R12_1 = fields.Integer(string="R12_1", default=0)
    R12_2 = fields.Integer(string="R12_2", default=0)
    R12_1_1 = fields.Integer(string="R12_1_1", default=0)
    R12_1_2 = fields.Integer(string="R12_1_2", default=0)
    R12_2_1 = fields.Integer(string="R12_2_1", default=0)
    R12_2_2 = fields.Integer(string="R12_2_2", default=0)
    R12_3_1 = fields.Integer(string="R12_3_1", default=0)
    R12_3_2 = fields.Integer(string="R12_3_2", default=0)
    R13_1 = fields.Integer(string="R13_1", default=0)
    R14_1 = fields.Integer(string="R14_1", default=0)
    R15_1 = fields.Integer(string="R15_1", default=0)
    R16_1 = fields.Integer(string="R16_1", default=0)
    R16_2 = fields.Integer(string="R16_2", default=0)
    R17_1 = fields.Integer(string="R17_1", default=0)
    R17_2 = fields.Integer(string="R17_2", default=0)
    R18_1 = fields.Integer(string="R18_1", default=0)
    R18_2 = fields.Integer(string="R18_2", default=0)
    R18_1_1 = fields.Integer(string="R18_1_1", default=0)
    R18_1_2 = fields.Integer(string="R18_1_2", default=0)
    R19_1 = fields.Integer(string="R19_1", default=0)
    R19_2 = fields.Integer(string="R19_2", default=0)
    R20_1 = fields.Integer(string="R20_1", default=0)
    R20_2 = fields.Integer(string="R20_2", default=0)
    R20_1_1 = fields.Integer(string="R20_1_1", default=0)
    R20_1_2 = fields.Integer(string="R20_1_2", default=0)
    R21_1 = fields.Integer(string="R21_1", default=0)
    R21_2 = fields.Integer(string="R21_2", default=0)
    R22_1 = fields.Integer(string="R22_1", default=0)
    R22_2 = fields.Integer(string="R22_2", default=0)
    R23_1 = fields.Integer(string="R23_1", default=0)
    R23_2 = fields.Integer(string="R23_2", default=0)
    R24_1 = fields.Integer(string="R24_1", default=0)
    R24_2 = fields.Integer(string="R24_2", default=0)
    R25_1 = fields.Integer(string="R25_1", default=0)
    R25_2 = fields.Integer(string="R25_2", default=0)
    R25_1_1 = fields.Integer(string="R25_1_1", default=0)
    R25_1_2 = fields.Integer(string="R25_1_2", default=0)
    R25_2_1 = fields.Integer(string="R25_2_1", default=0)
    R25_2_2 = fields.Integer(string="R25_2_2", default=0)
    R25_3_1 = fields.Integer(string="R25_3_1", default=0)
    R25_3_2 = fields.Integer(string="R25_3_2", default=0)
    R26_1 = fields.Integer(string="R26_1", default=0)
    R26_1_1 = fields.Integer(string="R26_1_1", default=0)
    R27_1 = fields.Integer(string="R27_1", default=0)
    R27_2 = fields.Integer(string="R27_2", default=0)
    R29_2 = fields.Integer(string="R29_2", default=0)
    R30_1 = fields.Integer(string="R30_1", default=0)
    R30_2 = fields.Integer(string="R30_2", default=0)
    R31_2 = fields.Integer(string="R31_2", default=0)
    R32_2 = fields.Integer(string="R32_2", default=0)
    R33_2 = fields.Integer(string="R33_2", default=0)
    R34_2 = fields.Integer(string="R34_2", default=0)
    R35_2 = fields.Integer(string="R35_2", default=0)
    R37_2 = fields.Integer(string="R37_2", default=0)
    R38_2 = fields.Integer(string="R38_2", default=0)
    R40_2 = fields.Integer(string="R40_2", default=0)
    R41_2 = fields.Integer(string="R41_2", default=0)
    R42_2 = fields.Integer(string="R42_2", default=0)
    nr_facturi = fields.Integer(string="nr_facturi", default=0)
    baza = fields.Integer(string="baza", default=0)
    tva = fields.Integer(string="tva", default=0)
    nr_facturi_primite = fields.Integer(string="nr_facturi_primite", default=0)
    baza_primite = fields.Integer(string="baza_primite", default=0)
    tva_primite = fields.Integer(string="tva_primite", default=0)
    valoare_a = fields.Integer(string="valoare_a", default=0)
    valoare_a1 = fields.Integer(string="valoare_a1", default=0)
    tva_a = fields.Integer(string="tva_a", default=0)
    tva_a1 = fields.Integer(string="tva_a1", default=0)
    valoare_b = fields.Integer(string="valoare_b", default=0)
    valoare_b1 = fields.Integer(string="valoare_b1", default=0)
    tva_b = fields.Integer(string="tva_b", default=0)
    tva_b1 = fields.Integer(string="tva_b1", default=0)
    nr_fact_emise = fields.Integer(string="nr_fact_emise", default=0)
    total_baza = fields.Integer(string="total_baza", default=0)
    total_tva = fields.Integer(string="total_tva", default=0)
    cuiSuccesor = fields.Char(string="cuiSuccesor")
    R64_1 = fields.Integer(string="R64_1", default=0)
    R64_2 = fields.Integer(string="R64_2", default=0)
    R65_1 = fields.Integer(string="R65_1", default=0)
    R65_2 = fields.Integer(string="R65_2", default=0)
    total_precedent = fields.Integer(string="total_precedent", default=0)
    total_curent = fields.Integer(string="total_curent", default=0)

    # New fields not from schema
    succesor_id = fields.Many2one(
        "res.partner",
        string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din "
        "Legea nr.207/2015 privind Codul de procedură fiscală",
    )
    R28_2 = fields.Integer(string="R28_2", default=0)
    R35_2_old = fields.Integer(string="Previous R35_2", default=0)
    R42_2_old = fields.Integer(string="Previous R42_2", default=0)

    R36_2 = fields.Integer(string="R36_2", default=0)
    R39_2 = fields.Integer(string="R39_2", default=0)
    R43_2 = fields.Integer(string="R43_2", default=0)
    R44_2 = fields.Integer(string="R44_2", default=0)

    def build_file(self):
        year, month = self.get_year_month()
        months = self.get_months_number()
        tip_decont = "L"
        if months == 3:
            tip_decont = "T"
        elif months == 6:
            tip_decont = "S"
        elif months == 12:
            tip_decont = "A"

        data_file = """<?xml version="1.0" encoding="UTF-8"?>
        <declaratie300 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="mfp:anaf:dgti:d300:declaratie:v6 D300.xsd"
        xmlns="mfp:anaf:dgti:d300:declaratie:v6" """
        succ_vat = self.succesor_id.vat_number if self.succesor_id.vat_number else ""

        xmldict = {
            "luna": month,
            "an": year,
            "tip_decont": '"' + tip_decont + '"',
            "temei": self.temei,
            "bifa_interne": self.bifa_interne,
            "nr_evid": '"' + self.nr_evid + '"',
            "cuiSuccesor": int(39187746),
            "pro_rata": 0,
            "bifa_cereale": '"N"',
            "bifa_mob": '"N"',
            "bifa_disp": '"N"',
            "bifa_cons": '"N"',
            "solicit_ramb": '"N"',
        }
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)

        vat_report_totals = self.generate_total()
        xmldict.update(vat_report_totals)
        for key, val in xmldict.items():
            data_file += """%s=%s """ % (key, val)
        data_file += """ />"""
        return data_file

    def generate_company_data(self):
        bank = self.bank_account_id.bank_id.name
        account = self.bank_account_id.acc_number
        banca = bank if bank else ""
        cont = account if account else ""
        data = {
            "cui": int(self.company_id.partner_id.vat_number),
            "den": '"' + self.company_id.name + '"',
            "adresa": '"' + self.company_id.partner_id._display_address(
                without_company=False).replace("\n", ",") + '"',
            "telefon": '"' + self.company_id.phone + '"',
            "mail": '"' + self.company_id.email + '"',
            "banca": '"' + banca + '"',
            "cont": '"' + cont + '"',
            "caen": '"' + self.company_id.caen_code + '"',
        }
        return data

    def generate_sign(self):
        signer = self.signature_id
        data = {
            "nume_declar": '"' + signer.first_name + '"',
            "prenume_declar": '"' + signer.last_name + '"',
            "functie_declar": '"' + signer.function + '"',
        }
        return data

    def get_amount(self, vat_report, tag, value):
        tag = list(filter(lambda entry: entry['name'] == tag, vat_report))
        sign = 1
        if tag:
            tag = tag[0]
            for key, value in tag.items():
                if type(key) == int:
                    if value.get("type_tax_use", "purchase") == "sale":
                        sign = -1
                        continue
            return sign * tag.get(value, 0)
        return 0

    def generate_data(self):
        self.ensure_one()
        report_obj = self.env["report.account_financial_report.vat_report"]
        vat_report_data, tax_data = report_obj._get_vat_report_data(
            self.company_id.id, self.date_from, self.date_to, True
        )
        vat_report = report_obj._get_vat_report_tag_data(
            vat_report_data, tax_data, False
        )
        #print(vat_report)
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
            "R43_2": self.R43_2,
            "R44_2": self.R44_2,
            "total_precedent": self.total_precedent,
            "total_curent": self.total_curent,
        }
        data["R17_1"] = \
            data.get("R1_1", 0) + data.get("R2_1", 0) + data.get("R3_1", 0) +\
            data.get("R4_1", 0) + data.get("R5_1", 0) + data.get("R6_1", 0) +\
            data.get("R7_1", 0) + data.get("R8_1", 0) + data.get("R9_1", 0) +\
            data.get("R10_1", 0) + data.get("R11_1", 0) + data.get("R12_1", 0) +\
            data.get("R13_1", 0) + data.get("R14_1", 0) + data.get("R15_1", 0) +\
            data.get("R16_1", 0)
        data["R17_2"] = \
            data.get("R5_2", 0) + data.get("R6_2", 0) + data.get("R7_2", 0) +\
            data.get("R8_2", 0) + data.get("R9_2", 0) + data.get("R10_2", 0) +\
            data.get("R11_2", 0) + data.get("R12_2", 0) + data.get("R16_2", 0)
        data["R27_1"] = \
            data.get("R18_1", 0) + data.get("R19_1", 0) + data.get("R20_1", 0) + \
            data.get("R21_1", 0) + data.get("R22_1", 0) + data.get("R23_1", 0) + \
            data.get("R24_1", 0) + data.get("R25_1", 0) + data.get("R26_1", 0)
        data["R27_2"] = \
            data.get("R18_2", 0) + data.get("R19_2", 0) + data.get("R20_2", 0) +\
            data.get("R21_2", 0) + data.get("R22_2", 0) + data.get("R23_2", 0) +\
            data.get("R24_2", 0) + data.get("R25_2", 0) + data.get("R43_2", 0) +\
            data.get("R44_2", 0)
        data["R28_2"] = self.R28_2
        data["R32_2"] = data.get("R28_2", 0) + data.get("R29_2", 0) +\
                        data.get("R30_2", 0) + data.get("R31_2", 0)
        vat = data["R32_2"] - data["R17_2"]
        data["R33_2"] = vat if vat < 0 else 0
        data["R34_2"] = vat if vat > 0 else 0
        data["R35_2"] = 0 if self.R42_2_old > 0 else self.R35_2_old
        data["R36_2"] = self.R36_2
        data["R37_2"] = \
            data.get("R34_2", 0) + data.get("R35_2", 0) + data.get("R36_2", 0)
        data["R38_2"] = 0 if self.R35_2_old > 0 else self.R42_2_old
        data["R39_2"] = self.R39_2
        data["R40_2"] = \
            data.get("R33_2", 0) + data.get("R38_2", 0) + data.get("R39_2", 0)
        vat_result = data.get("R37_2", 0) - data.get("R40_2", 0)
        data["R41_2"] = vat_result if vat_result > 0 else 0
        data["R42_2"] = -1 * vat_result if vat_result < 0 else 0
        return data

    def generate_total(self):
        self.ensure_one()
        cust_invoices = self.get_period_invoices(['out_invoice', 'out_refund'])
        supp_invoices = self.get_period_invoices(['in_invoice', 'in_refund'])
        cust_vatp_invoices = self.get_period_vatp_invoices(['in_invoice', 'in_refund'])
        supp_vatp_invoices = self.get_period_vatp_invoices(['in_invoice', 'in_refund'])
        valoare_a = valoare_a1 = tva_a = tva_a1 = 0
        valoare_b = valoare_b1 = tva_b = tva_b1 = 0
        date1 = self.date_to - relativedelta(months=1)
        for inv in cust_vatp_invoices:
            valoare_a += inv.amount_untaxed_signed
            tva_a += inv.amount_tax_signed
            cash_basis_moves = self.env['account.move'].search(
                [('tax_cash_basis_move_id', '=', inv.id),
                 ('date', '<=', self.date_to)]
            )
            for line in cash_basis_moves.line_ids:
                if not line.tax_repartition_line_id:
                    continue
                valoare_a += line.tax_base_amount
                tva_a += line.balance
                if inv.date > date1:
                    valoare_a1 += line.tax_base_amount
                    tva_a1 += line.balance
        for inv in supp_vatp_invoices:
            valoare_a += inv.amount_untaxed_signed
            tva_a += inv.amount_tax_signed
            cash_basis_moves = self.env['account.move'].search(
                [('tax_cash_basis_move_id', '=', inv.id),
                 ('date', '<=', self.date_to)]
            )
            for line in cash_basis_moves.line_ids:
                if not line.tax_repartition_line_id:
                    continue
                valoare_b += line.tax_base_amount
                tva_b += line.balance
                if inv.date > date1:
                    valoare_b1 += line.tax_base_amount
                    tva_b1 += line.balance
        data = {
            "nr_facturi": int(len(cust_invoices)),
            "baza": int(sum(inv.amount_untaxed_signed for inv in cust_invoices)),
            "tva": int(sum(inv.amount_tax_signed for inv in cust_invoices)),
            "nr_facturi_primite": int(len(supp_invoices)),
            "baza_primite": int(sum(-1 * inv.amount_untaxed_signed for inv in supp_invoices)),
            "tva_primite": int(sum(-1 * inv.amount_tax_signed for inv in supp_invoices)),
            "valoare_a": int(valoare_a),
            "valoare_a1": int(valoare_a1),
            "tva_a": int(tva_a),
            "tva_a1": int(tva_a1),
            "valoare_b": int(-1 * valoare_b),
            "valoare_b1": int(-1 * valoare_b1),
            "tva_b": int(-1 * tva_b),
            "tva_b1": int(-1 * tva_b1),
            "nr_fact_emise": 0,
            "total_baza": 0,
            "total_tva": 0,
        }
        return data
