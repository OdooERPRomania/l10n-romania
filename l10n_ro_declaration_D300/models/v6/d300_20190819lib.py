# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Sun Oct 18 11:10:42 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Declaratie300(models.AbstractModel):
    _name = "anaf.d300.v60"
    _inherit = "anaf.mixin"
    _description = "Declaratie D300, versiunea 6"

    D30060_luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    D30060_an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    D30060_bifa_interne = fields.Integer(
        string="bifa_interne", xsd_required=True, xsd_type="integer"
    )
    D30060_temei = fields.Integer(string="temei", xsd_required=True, xsd_type="integer")
    D30060_nume_declar = fields.Char(
        string="nume_declar", xsd_required=True, xsd_type="string"
    )
    D30060_prenume_declar = fields.Char(
        string="prenume_declar", xsd_required=True, xsd_type="string"
    )
    D30060_functie_declar = fields.Char(
        string="functie_declar", xsd_required=True, xsd_type="string"
    )
    D30060_cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    D30060_den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    D30060_adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    D30060_telefon = fields.Char(string="telefon", xsd_type="string")
    D30060_fax = fields.Char(string="fax", xsd_type="string")
    D30060_mail = fields.Char(string="mail", xsd_type="token")
    D30060_banca = fields.Char(string="banca", xsd_required=True, xsd_type="string")
    D30060_cont = fields.Char(string="cont", xsd_required=True, xsd_type="string")
    D30060_caen = fields.Char(string="caen", xsd_required=True, xsd_type="string")
    D30060_tip_decont = fields.Char(
        string="tip_decont", xsd_required=True, xsd_type="string"
    )
    D30060_pro_rata = fields.Float(
        string="pro_rata", xsd_required=True, xsd_type="double"
    )
    D30060_bifa_cereale = fields.Char(
        string="bifa_cereale", xsd_required=True, xsd_type="string"
    )
    D30060_bifa_mob = fields.Char(
        string="bifa_mob", xsd_required=True, xsd_type="string"
    )
    D30060_bifa_disp = fields.Char(
        string="bifa_disp", xsd_required=True, xsd_type="string"
    )
    D30060_bifa_cons = fields.Char(
        string="bifa_cons", xsd_required=True, xsd_type="string"
    )
    D30060_solicit_ramb = fields.Char(
        string="solicit_ramb", xsd_required=True, xsd_type="string"
    )
    D30060_nr_evid = fields.Integer(
        string="nr_evid", xsd_required=True, xsd_type="integer"
    )
    D30060_totalPlata_A = fields.Integer(
        string="totalPlata_A", xsd_required=True, xsd_type="integer"
    )
    D30060_R1_1 = fields.Integer(string="R1_1", xsd_type="integer")
    D30060_R2_1 = fields.Integer(string="R2_1", xsd_type="integer")
    D30060_R3_1 = fields.Integer(string="R3_1", xsd_type="integer")
    D30060_R3_1_1 = fields.Integer(string="R3_1_1", xsd_type="integer")
    D30060_R4_1 = fields.Integer(string="R4_1", xsd_type="integer")
    D30060_R5_1 = fields.Integer(string="R5_1", xsd_type="integer")
    D30060_R5_2 = fields.Integer(string="R5_2", xsd_type="integer")
    D30060_R5_1_1 = fields.Integer(string="R5_1_1", xsd_type="integer")
    D30060_R5_1_2 = fields.Integer(string="R5_1_2", xsd_type="integer")
    D30060_R6_1 = fields.Integer(string="R6_1", xsd_type="integer")
    D30060_R6_2 = fields.Integer(string="R6_2", xsd_type="integer")
    D30060_R7_1 = fields.Integer(string="R7_1", xsd_type="integer")
    D30060_R7_2 = fields.Integer(string="R7_2", xsd_type="integer")
    D30060_R7_1_1 = fields.Integer(string="R7_1_1", xsd_type="integer")
    D30060_R7_1_2 = fields.Integer(string="R7_1_2", xsd_type="integer")
    D30060_R8_1 = fields.Integer(string="R8_1", xsd_type="integer")
    D30060_R8_2 = fields.Integer(string="R8_2", xsd_type="integer")
    D30060_R9_1 = fields.Integer(string="R9_1", xsd_type="integer")
    D30060_R9_2 = fields.Integer(string="R9_2", xsd_type="integer")
    D30060_R10_1 = fields.Integer(string="R10_1", xsd_type="integer")
    D30060_R10_2 = fields.Integer(string="R10_2", xsd_type="integer")
    D30060_R11_1 = fields.Integer(string="R11_1", xsd_type="integer")
    D30060_R11_2 = fields.Integer(string="R11_2", xsd_type="integer")
    D30060_R12_1 = fields.Integer(string="R12_1", xsd_type="integer")
    D30060_R12_2 = fields.Integer(string="R12_2", xsd_type="integer")
    D30060_R12_1_1 = fields.Integer(string="R12_1_1", xsd_type="integer")
    D30060_R12_1_2 = fields.Integer(string="R12_1_2", xsd_type="integer")
    D30060_R12_2_1 = fields.Integer(string="R12_2_1", xsd_type="integer")
    D30060_R12_2_2 = fields.Integer(string="R12_2_2", xsd_type="integer")
    D30060_R12_3_1 = fields.Integer(string="R12_3_1", xsd_type="integer")
    D30060_R12_3_2 = fields.Integer(string="R12_3_2", xsd_type="integer")
    D30060_R13_1 = fields.Integer(string="R13_1", xsd_type="integer")
    D30060_R14_1 = fields.Integer(string="R14_1", xsd_type="integer")
    D30060_R15_1 = fields.Integer(string="R15_1", xsd_type="integer")
    D30060_R16_1 = fields.Integer(string="R16_1", xsd_type="integer")
    D30060_R16_2 = fields.Integer(string="R16_2", xsd_type="integer")
    D30060_R17_1 = fields.Integer(string="R17_1", xsd_type="integer")
    D30060_R17_2 = fields.Integer(string="R17_2", xsd_type="integer")
    D30060_R18_1 = fields.Integer(string="R18_1", xsd_type="integer")
    D30060_R18_2 = fields.Integer(string="R18_2", xsd_type="integer")
    D30060_R18_1_1 = fields.Integer(string="R18_1_1", xsd_type="integer")
    D30060_R18_1_2 = fields.Integer(string="R18_1_2", xsd_type="integer")
    D30060_R19_1 = fields.Integer(string="R19_1", xsd_type="integer")
    D30060_R19_2 = fields.Integer(string="R19_2", xsd_type="integer")
    D30060_R20_1 = fields.Integer(string="R20_1", xsd_type="integer")
    D30060_R20_2 = fields.Integer(string="R20_2", xsd_type="integer")
    D30060_R20_1_1 = fields.Integer(string="R20_1_1", xsd_type="integer")
    D30060_R20_1_2 = fields.Integer(string="R20_1_2", xsd_type="integer")
    D30060_R21_1 = fields.Integer(string="R21_1", xsd_type="integer")
    D30060_R21_2 = fields.Integer(string="R21_2", xsd_type="integer")
    D30060_R22_1 = fields.Integer(string="R22_1", xsd_type="integer")
    D30060_R22_2 = fields.Integer(string="R22_2", xsd_type="integer")
    D30060_R23_1 = fields.Integer(string="R23_1", xsd_type="integer")
    D30060_R23_2 = fields.Integer(string="R23_2", xsd_type="integer")
    D30060_R24_1 = fields.Integer(string="R24_1", xsd_type="integer")
    D30060_R24_2 = fields.Integer(string="R24_2", xsd_type="integer")
    D30060_R25_1 = fields.Integer(string="R25_1", xsd_type="integer")
    D30060_R25_2 = fields.Integer(string="R25_2", xsd_type="integer")
    D30060_R25_1_1 = fields.Integer(string="R25_1_1", xsd_type="integer")
    D30060_R25_1_2 = fields.Integer(string="R25_1_2", xsd_type="integer")
    D30060_R25_2_1 = fields.Integer(string="R25_2_1", xsd_type="integer")
    D30060_R25_2_2 = fields.Integer(string="R25_2_2", xsd_type="integer")
    D30060_R25_3_1 = fields.Integer(string="R25_3_1", xsd_type="integer")
    D30060_R25_3_2 = fields.Integer(string="R25_3_2", xsd_type="integer")
    D30060_R43_2 = fields.Integer(string="R43_2", xsd_type="integer")
    D30060_R44_2 = fields.Integer(string="R44_2", xsd_type="integer")
    D30060_R26_1 = fields.Integer(string="R26_1", xsd_type="integer")
    D30060_R26_1_1 = fields.Integer(string="R26_1_1", xsd_type="integer")
    D30060_R27_1 = fields.Integer(string="R27_1", xsd_type="integer")
    D30060_R27_2 = fields.Integer(string="R27_2", xsd_type="integer")
    D30060_R28_2 = fields.Integer(string="R28_2", xsd_type="integer")
    D30060_R29_2 = fields.Integer(string="R29_2", xsd_type="integer")
    D30060_R30_1 = fields.Integer(string="R30_1", xsd_type="integer")
    D30060_R30_2 = fields.Integer(string="R30_2", xsd_type="integer")
    D30060_R31_2 = fields.Integer(string="R31_2", xsd_type="integer")
    D30060_R32_2 = fields.Integer(string="R32_2", xsd_type="integer")
    D30060_R33_2 = fields.Integer(string="R33_2", xsd_type="integer")
    D30060_R34_2 = fields.Integer(string="R34_2", xsd_type="integer")
    D30060_R35_2 = fields.Integer(string="R35_2", xsd_type="integer")
    D30060_R36_2 = fields.Integer(string="R36_2", xsd_type="integer")
    D30060_R37_2 = fields.Integer(string="R37_2", xsd_type="integer")
    D30060_R38_2 = fields.Integer(string="R38_2", xsd_type="integer")
    D30060_R39_2 = fields.Integer(string="R39_2", xsd_type="integer")
    D30060_R40_2 = fields.Integer(string="R40_2", xsd_type="integer")
    D30060_R41_2 = fields.Integer(string="R41_2", xsd_type="integer")
    D30060_R42_2 = fields.Integer(string="R42_2", xsd_type="integer")
    D30060_nr_facturi = fields.Integer(string="nr_facturi", xsd_type="integer")
    D30060_baza = fields.Integer(string="baza", xsd_type="integer")
    D30060_tva = fields.Integer(string="tva", xsd_type="integer")
    D30060_nr_facturi_primite = fields.Integer(
        string="nr_facturi_primite", xsd_type="integer"
    )
    D30060_baza_primite = fields.Integer(string="baza_primite", xsd_type="integer")
    D30060_tva_primite = fields.Integer(string="tva_primite", xsd_type="integer")
    D30060_valoare_a = fields.Integer(string="valoare_a", xsd_type="integer")
    D30060_valoare_a1 = fields.Integer(string="valoare_a1", xsd_type="integer")
    D30060_tva_a = fields.Integer(string="tva_a", xsd_type="integer")
    D30060_tva_a1 = fields.Integer(string="tva_a1", xsd_type="integer")
    D30060_valoare_b = fields.Integer(string="valoare_b", xsd_type="integer")
    D30060_valoare_b1 = fields.Integer(string="valoare_b1", xsd_type="integer")
    D30060_tva_b = fields.Integer(string="tva_b", xsd_type="integer")
    D30060_tva_b1 = fields.Integer(string="tva_b1", xsd_type="integer")
    D30060_nr_fact_emise = fields.Integer(string="nr_fact_emise", xsd_type="integer")
    D30060_total_baza = fields.Integer(string="total_baza", xsd_type="integer")
    D30060_total_tva = fields.Integer(string="total_tva", xsd_type="integer")
    D30060_cuiSuccesor = fields.Char(string="cuiSuccesor", xsd_type="token")
    D30060_R64_1 = fields.Integer(string="R64_1", xsd_type="integer")
    D30060_R64_2 = fields.Integer(string="R64_2", xsd_type="integer")
    D30060_R65_1 = fields.Integer(string="R65_1", xsd_type="integer")
    D30060_R65_2 = fields.Integer(string="R65_2", xsd_type="integer")
    D30060_total_precedent = fields.Integer(
        string="total_precedent", xsd_type="integer"
    )
    D30060_total_curent = fields.Integer(string="total_curent", xsd_type="integer")

    # New fields not from schema
    nr_evid = fields.Char()
    succesor_id = fields.Many2one(
        "res.partner",
        string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din "
        "Legea nr.207/2015 privind Codul de procedură fiscală",
    )

    def build_file(self):
        year, month = self.get_year_month()
        xmldict = {
            "D30060_luna": month,
            "D30060_an": year,
            "D30060_nr_evid": self.nr_evid,
            "D30060_cuiSuccesor": self.succesor_id.vat_number,
        }
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)
        # vat_report_totals = self.generate_total(vat_report)
        # xmldict.update(vat_report_totals)
        return xmldict

    def generate_company_data(self):
        data = {
            "D30060_cui": self.company_id.partner_id.vat_number,
            "D30060_den": self.company_id.name,
            "D30060_adresa": self.company_id.partner_id.address_get(["default"]),
            "D30060_telefon": self.company_id.phone,
            "D30060_mail": self.company_id.email,
            "D30060_banca": self.bank_account_id.bank_id.name,
            "D30060_cont": self.bank_account_id.acc_number,
            "D30060_caen": self.company_id.caen_code,
        }
        return data

    def generate_sign(self):
        signer = self.signature_id
        data = {
            "D30060_nume_declar": signer.first_name,
            "D30060_prenume_declar": signer.last_name,
            "D30060_functie_declar": signer.function,
        }
        return data

    def generate_data(self):
        company = self.company_id
        company_id = company.id
        date_from = self.date_from
        date_to = self.date_to
        vat_report_data, tax_data = self._get_vat_report_data(
            company_id, date_from, date_to
        )
        vat_report = self._get_vat_report_tag_data(vat_report_data, tax_data, False)
        print(vat_report)
        data = {}
        # data = {
        #     "D30060_R1_1":
        #     "D30060_R2_1":
        #     "D30060_R3_1":
        #     "D30060_R3_1_1":
        #     "D30060_R4_1":
        #     "D30060_R5_1"
        #     "D30060_R18_1"
        #     "D30060_R5_2"
        #     "D30060_R18_2"
        #     "D30060_R5_1_1"
        #     "D30060_R18_1_1"
        #     "D30060_R5_1_2"
        #     "D30060_R18_1_2"
        #     "D30060_R6_1"
        #     "D30060_R19_1":
        #     "D30060_R6_2"
        #     "D30060_R19_2":
        #     "D30060_R7_1"
        #     "D30060_R20_1":
        #     "D30060_R7_2"
        #     "D30060_R20_2":
        #     "D30060_R7_1_1"
        #     "D30060_R20_1_1":
        #     "D30060_R7_1_2"
        #     "D30060_R20_1_2":
        #     "D30060_R8_1"
        #     "D30060_R21_1":
        #     "D30060_R8_2"
        #     "D30060_R21_2":
        #     "D30060_R9_1":
        #     "D30060_R9_2":
        #     "D30060_R10_1":
        #     "D30060_R10_2":
        #     "D30060_R11_1":
        #     "D30060_R11_2":
        #     "D30060_R12_1"
        #     "D30060_R25_1":
        #     "D30060_R12_2"
        #     "D30060_R25_2":
        #     "D30060_R12_1_1"
        #     "D30060_R25_1_1":
        #     "D30060_R12_1_2"
        #     "D30060_R25_1_2":
        #     "D30060_R12_2_1"
        #     "D30060_R25_2_1":
        #     "D30060_R12_2_2"
        #     "D30060_R25_2_2":
        #     "D30060_R12_3_1"
        #     "D30060_R25_3_1":
        #     "D30060_R12_3_2"
        #     "D30060_R25_3_2":
        #     "D30060_R13_1":
        #     "D30060_R14_1":
        #     "D30060_R15_1":
        #     "D30060_R16_1":
        #     "D30060_R16_2":
        #     "D30060_R17_1":
        #     "D30060_R17_2":
        #     "D30060_R22_1":
        #     "D30060_R22_2":
        #     "D30060_R23_1":
        #     "D30060_R23_2":
        #     "D30060_R24_1":
        #     "D30060_R24_2":
        #     "D30060_R43_2":
        #     "D30060_R44_2":
        #     "D30060_R26_1":
        #     "D30060_R26_1_1":
        #     "D30060_R27_1":
        #     "D30060_R27_2":
        #     "D30060_R28_2":
        #     "D30060_R29_2":
        #     "D30060_R30_1":
        #     "D30060_R30_2":
        #     "D30060_R31_2":
        #     "D30060_R32_2":
        #     "D30060_R33_2":
        #     "D30060_R34_2":
        #     "D30060_R35_2":
        #     "D30060_R36_2":
        #     "D30060_R37_2":
        #     "D30060_R38_2":
        #     "D30060_R39_2":
        #     "D30060_R40_2":
        #     "D30060_R41_2":
        #     "D30060_R42_2":
        #     "D30060_R64_1":
        #     "D30060_R64_2":
        #     "D30060_R65_1":
        #     "D30060_R65_2":
        # }
        return data
