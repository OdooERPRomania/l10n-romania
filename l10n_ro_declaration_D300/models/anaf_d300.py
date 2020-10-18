# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AnafD300(models.Model):
    _name = "anaf.d300"
    _inherit = "anaf.mixin"
    _description = "Anaf Declaration D300"
    _anaf_number = "300"

    nr_evid = fields.Char()
    bifa_interne = fields.Boolean(
        "Bifa Interne",
        help="Se aplica metoda simplificata pentru operatiuni interne",
    )
    temei = fields.Selection(
        [("0", "Art.105 alin(6) lit.a)"),
         ("2", "Art.105 alin(6) lit.b)")],
        string="Temei Legal",
        help="Temeiul legal (Lege 207/2015 privind Codul de procedura fiscala )",
    )
    succesor_id = fields.Many2one(
        "res.partner", string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din Legea nr.207/2015 privind Codul de procedură fiscală")
    bifa_cereale = fields.Boolean(
        "Cereal Transactions",
        help="Aţi efectuat livrari de cereale şi "
            "plante tehnice pentru care se "
            "aplică taxarea inversă în "
            "conformitate cu prevederile "
            "art.160 din Codul fiscal, a căror "
            "exigibilitate intervine în perioada "
            "de raportare ?",
    )
    bifa_mob = fields.Boolean(
        "Phone Transactions",
        help="Aţi efectuat livrari de telefoane "
            "mobile pentru care se aplică "
            "taxarea inversă în "
            "conformitate cu prevederile "
            "art.331 din Codul fiscal, a căror "
            "exigibilitate intervine în perioada "
            "de raportare ? ",
    )
    bifa_disp = fields.Boolean(
        "Electronics Transactions",
        help="Aţi efectuat livrari de dispozitive "
            "cu circuite integrate inainte de "
            "integrarea lor in produse "
            "destinate utilizatorului final "
            "pentru care se aplică taxarea "
            "inversă în "
            "conformitate cu prevederile "
            "art.331 din Codul fiscal, a căror "
            "exigibilitate intervine în perioada "
            "de raportare ? ",
    )
    bifa_cons = fields.Boolean(
        "Purchases of Eolian Parks",
        help="Aţi efectuat livrari de console "
            "de jocuri, tablete PC si laptopuri "
            "pentru care se aplică taxarea "
            "inversă în "
            "conformitate cu prevederile "
            "art.331 din Codul fiscal, a căror "
            "exigibilitate intervine în perioada "
            "de raportare ? ",
    )
    solicit_ramb = fields.Boolean("Request VAT Reimbursment")
    bank_account_id = fields.Many2one(
        "res.partner.bank", string="Bank Account",
        domain=[("id", "in", company_id.bank_ids.ids)])

    def build_file(self):
        year, month = self.get_year_month()
        xmldict = {
            "luna": month,
            "an": year,
            "nr_evid": "",
            "cuiSuccesor": self.succesor_id.vat_number
        }
        company_data = self.generate_get_company()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        trans = self.generate_transactions()
        xmldict.update(trans)
        vat_report = self.generate_data()
        #xmldict.update(vat_report)
        #vat_report_totals = self.generate_total(vat_report)
        #xmldict.update(vat_report_totals)
        #return super(AnafD300, self).build_file(xmldict)
        return True

    def generate_company_data(self):
        data = {
            "cui": self.company_id.partner_id.vat_number,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id.address_get(['default']),
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
            "functie_declar": signer.function
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
        vat_report = self._get_vat_report_tag_data(
            vat_report_data, tax_data, False
        )
        print(vat_report)
        # data = {
        #     "R1_1":
        #     "R2_1":
        #     "R3_1":
        #     "R3_1_1":
        #     "R4_1":
        #     "R5_1" =  "R18_1"
        #     "R5_2" =   "R18_2"
        #     "R5_1_1" = "R18_1_1"
        #     "R5_1_2" = "R18_1_2"
        #     "R6_1": "R19_1":
        #     "R6_2" "R19_2":
        #     "R7_1": "R20_1":
        #     "R7_2": "R20_2":
        #     "R7_1_1": "R20_1_1":
        #     "R7_1_2": "R20_1_2":
        #     "R8_1": "R21_1":
        #     "R8_2":  "R21_2":
        #     "R9_1":
        #     "R9_2":
        #     "R10_1":
        #     "R10_2":
        #     "R11_1":
        #     "R11_2":
        #     "R12_1":"R25_1":
        #     "R12_2":"R25_2":
        #     "R12_1_1": "R25_1_1":
        #     "R12_1_2":"R25_1_2":
        #     "R12_2_1":"R25_2_1":
        #     "R12_2_2": "R25_2_2":
        #     "R12_3_1":"R25_3_1":
        #     "R12_3_2":"R25_3_2":
        #
        #
        #     "R13_1":
        #     "R14_1":
        #     "R15_1":
        #     "R16_1":
        #     "R16_2":
        #     "R17_1":
        #     "R17_2":
        #
        #
        #     "R22_1":
        #     "R22_2":
        #     "R23_1":
        #     "R23_2":
        #     "R24_1":
        #     "R24_2":
        #
        #     "R43_2":
        #     "R44_2":
        #     "R26_1":
        #     "R26_1_1":
        #     "R27_1":
        #     "R27_2":
        #     "R28_2":
        #     "R29_2":
        #     "R30_1":
        #     "R30_2":
        #     "R31_2":
        #     "R32_2":
        #     "R33_2":
        #     "R34_2":
        #     "R35_2":
        #     "R36_2":
        #     "R37_2":
        #     "R38_2":
        #     "R39_2":
        #     "R40_2":
        #     "R41_2":
        #     "R42_2":
        #     "R64_1":
        #     "R64_2":
        #     "R65_1":
        #     "R65_2":
        # }

    def generate_total(self):
        # total_precedent
        # total_curent
        # nr_facturi
        # baza
        # tva
        # nr_facturi_primite
        # baza_primite
        # tva_primite
        # totalPlata_A
        # valoare_a
        # valoare_a1
        # tva_a
        # tva_a1
        # valoare_b
        # valoare_b1
        # tva_b
        # tva_b1
        # nr_fact_emise
        # total_baza
        # total_tva
