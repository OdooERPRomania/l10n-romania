# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import models


class Declaratie300(models.TransientModel):
    _name = "anaf.d300.v60"
    _inherit = "anaf.d300"
    _description = "Declaratie D300, versiunea 6"

    def build_file(self):
        year, month = self.get_year_month()
        months = self.get_months_number()
        tip_decont = "L"
        tip_decont_e = "301"
        if months == 3:
            tip_decont = "T"
            tip_decont_e = "302"
        elif months == 6:
            tip_decont = "S"
            tip_decont_e = "303"
        elif months == 12:
            tip_decont = "A"
            tip_decont_e = "304"

        data_file = """<?xml version="1.0" encoding="UTF-8"?>
        <declaratie300 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="mfp:anaf:dgti:d300:declaratie:v6 D300.xsd"
        xmlns="mfp:anaf:dgti:d300:declaratie:v6" """

        xmldict = {
            "luna": month,
            "an": year,
            "tip_decont": tip_decont,
            "temei": self.temei,
            "bifa_interne": int(self.bifa_interne),
            "pro_rata": self.pro_rata,
            "bifa_cereale": self.bifa_cereale,
            "bifa_mob": self.bifa_mob,
            "bifa_disp": self.bifa_disp,
            "bifa_cons": self.bifa_cons,
            "solicit_ramb": self.solicit_ramb,
        }
        if self.succesor_id and self.succesor_id.vat_number:
            xmldict["cuiSuccesor"] = int(self.succesor_id.vat_number)

        company_data = self.generate_company_data()
        xmldict.update(company_data)
        sign = self.generate_sign()
        xmldict.update(sign)
        vat_report = self.generate_data()
        xmldict.update(vat_report)
        totalPlata_A = 0
        for key, value in vat_report.items():
            if key != "totalPlata_A":
                totalPlata_A += value

        vat_report_totals = self.generate_total()
        xmldict.update(vat_report_totals)
        total_keys = [
            "nr_facturi",
            "baza",
            "tva",
            "nr_facturi_primite",
            "baza_primite",
            "tva_primite",
        ]
        for _key, value in vat_report_totals.items():
            if _key in total_keys:
                totalPlata_A += value

        xmldict["totalPlata_A"] = totalPlata_A

        month_str = str(month).zfill(2)
        year_str = str(year)[-2:]
        next_date = self.date_next.strftime("%d%m%y")
        nr_evid = "10{}01{}{}{}0000".format(
            tip_decont_e, month_str, year_str, next_date
        )
        control = sum(int(x) for x in nr_evid)
        xmldict["nr_evid"] = nr_evid + "%s" % str(control)[-2:]
        for key, val in xmldict.items():
            data_file += """{}={} """.format(key, self.value_to_string(val))
        data_file += """ />"""
        return data_file

    def generate_company_data(self):
        bank = self.bank_account_id.bank_id.name
        account = self.bank_account_id.acc_number
        banca = bank if bank else ""
        cont = account if account else ""
        data = {
            "cui": int(self.company_id.partner_id.vat_number),
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(
                without_company=True
            ).replace("\n", ","),
            "telefon": self.company_id.phone,
            "mail": self.company_id.email,
            "banca": banca.replace(",", "").replace("#", ""),
            "cont": cont,
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

    def get_amount(self, vat_report, tag):
        amount = vat_report.get(tag)
        if amount:
            return abs(int(round(amount)))
        return 0

    def generate_data(self):
        self.ensure_one()
        vat_report = self._get_anaf_vat_report_data(
            self.company_id.id, self.date_from, self.date_to
        )
        data = {
            "R1_1": self.get_amount(vat_report, "01 - BAZA"),
            "R2_1": self.get_amount(vat_report, "02 - BAZA"),
            "R3_1": self.get_amount(vat_report, "03 - BAZA"),
            "R3_1_1": self.get_amount(vat_report, "03_1 - BAZA"),
            "R4_1": self.get_amount(vat_report, "04 - BAZA"),
            "R5_1": self.get_amount(vat_report, "05 - BAZA"),
            "R5_2": self.get_amount(vat_report, "05 - TVA"),
            "R5_1_1": self.get_amount(vat_report, "05_1 - BAZA"),
            "R5_1_2": self.get_amount(vat_report, "05_1 - TVA"),
            "R6_1": self.get_amount(vat_report, "06 - BAZA"),
            "R6_2": self.get_amount(vat_report, "06 - TVA"),
            "R7_1": self.get_amount(vat_report, "07 - BAZA"),
            "R7_2": self.get_amount(vat_report, "07 - TVA"),
            "R7_1_1": self.get_amount(vat_report, "07_1 - BAZA"),
            "R7_1_2": self.get_amount(vat_report, "07_1 - TVA"),
            "R8_1": self.get_amount(vat_report, "08 - BAZA"),
            "R8_2": self.get_amount(vat_report, "08 - TVA"),
            "R9_1": self.get_amount(vat_report, "09 - BAZA"),
            "R9_2": self.get_amount(vat_report, "09 - TVA"),
            "R10_1": self.get_amount(vat_report, "10 - BAZA"),
            "R10_2": self.get_amount(vat_report, "10 - TVA"),
            "R11_1": self.get_amount(vat_report, "11 - BAZA"),
            "R11_2": self.get_amount(vat_report, "11 - TVA"),
            "R12_1": self.get_amount(vat_report, "12 - BAZA"),
            "R12_2": self.get_amount(vat_report, "12 - TVA"),
            "R12_1_1": self.get_amount(vat_report, "12_1 - BAZA"),
            "R12_1_2": self.get_amount(vat_report, "12_1 - TVA"),
            "R12_2_1": self.get_amount(vat_report, "12_2 - BAZA"),
            "R12_2_2": self.get_amount(vat_report, "12_2 - TVA"),
            "R12_3_1": self.get_amount(vat_report, "12_3 - BAZA"),
            "R12_3_2": self.get_amount(vat_report, "12_3 - TVA"),
            "R13_1": self.get_amount(vat_report, "13 - BAZA"),
            "R14_1": self.get_amount(vat_report, "14 - BAZA"),
            "R15_1": self.get_amount(vat_report, "15 - BAZA"),
            "R16_1": self.get_amount(vat_report, "16 - BAZA"),
            "R16_2": self.get_amount(vat_report, "16 - TVA"),
            "R64_1": self.get_amount(vat_report, "17 - BAZA"),
            "R64_2": self.get_amount(vat_report, "17 - TVA"),
            "R65_1": self.get_amount(vat_report, "18 - BAZA"),
            "R65_2": self.get_amount(vat_report, "18 - TVA"),
            # Purchases
            "R18_1": self.get_amount(vat_report, "20 - BAZA"),
            "R18_2": self.get_amount(vat_report, "20 - TVA"),
            "R18_1_1": self.get_amount(vat_report, "20_1 - BAZA"),
            "R18_1_2": self.get_amount(vat_report, "20_1 - TVA"),
            "R19_1": self.get_amount(vat_report, "21 - BAZA"),
            "R19_2": self.get_amount(vat_report, "21 - TVA"),
            "R20_1": self.get_amount(vat_report, "22 - BAZA"),
            "R20_2": self.get_amount(vat_report, "22 - TVA"),
            "R20_1_1": self.get_amount(vat_report, "22_1 - BAZA"),
            "R20_1_2": self.get_amount(vat_report, "22_1 - TVA"),
            "R21_1": self.get_amount(vat_report, "23 - BAZA"),
            "R21_2": self.get_amount(vat_report, "23 - TVA"),
            "R22_1": self.get_amount(vat_report, "24_1 - BAZA")
            + int(round(0.5 * self.get_amount(vat_report, "24_2 - BAZA"))),
            "R22_2": self.get_amount(vat_report, "24_1 - TVA")
            + self.get_amount(vat_report, "24_2 - TVA"),
            "R23_1": self.get_amount(vat_report, "25_1 - BAZA")
            + int(round(0.5 * self.get_amount(vat_report, "25_2 - BAZA"))),
            "R23_2": self.get_amount(vat_report, "25_1 - TVA")
            + self.get_amount(vat_report, "25_2 - TVA"),
            "R24_1": self.get_amount(vat_report, "26_1 - BAZA")
            + int(round(0.5 * self.get_amount(vat_report, "26_2 - BAZA"))),
            "R24_2": self.get_amount(vat_report, "26_1 - TVA")
            + self.get_amount(vat_report, "26_2 - TVA"),
            "R25_1": self.get_amount(vat_report, "27 - BAZA"),
            "R25_2": self.get_amount(vat_report, "27 - TVA"),
            "R25_1_1": self.get_amount(vat_report, "27_1 - BAZA"),
            "R25_1_2": self.get_amount(vat_report, "27_1 - TVA"),
            "R25_2_1": self.get_amount(vat_report, "27_2 - BAZA"),
            "R25_2_2": self.get_amount(vat_report, "27_2 - TVA"),
            "R25_3_1": self.get_amount(vat_report, "27_3 - BAZA"),
            "R25_3_2": self.get_amount(vat_report, "27_3 - TVA"),
            "R26_1": self.get_amount(vat_report, "30 - BAZA"),
            "R26_1_1": self.get_amount(vat_report, "30_1 - BAZA"),
            "R29_2": self.get_amount(vat_report, "33 - TVA"),
            # Regularization
            "R30_1": self.get_amount(vat_report, "34 - BAZA"),
            "R30_2": self.get_amount(vat_report, "34 - TVA"),
            "R31_2": self.get_amount(vat_report, "35 - TVA"),
            "R43_2": self.get_amount(vat_report, "28 - TVA"),
            "R44_2": self.get_amount(vat_report, "29 - TVA"),
            "R36_2": self.get_amount(vat_report, "40 - TVA"),
            "R39_2": self.get_amount(vat_report, "43 - TVA"),
        }

        data["R12_1"] += (
            data.get("R12_1_1", 0) + data.get("R12_2_1", 0) + data.get("R12_3_1", 0)
        )
        data["R12_2"] += (
            data.get("R12_1_2", 0) + data.get("R12_2_2", 0) + data.get("R12_3_2", 0)
        )
        data["R25_1"] += (
            data.get("R25_1_1", 0) + data.get("R25_2_1", 0) + data.get("R25_3_1", 0)
        )
        data["R25_2"] += (
            data.get("R25_1_2", 0) + data.get("R25_2_2", 0) + data.get("R25_3_2", 0)
        )
        data["R17_1"] = (
            data.get("R1_1", 0)
            + data.get("R2_1", 0)
            + data.get("R3_1", 0)
            + data.get("R4_1", 0)
            + data.get("R5_1", 0)
            + data.get("R6_1", 0)
            + data.get("R7_1", 0)
            + data.get("R8_1", 0)
            + data.get("R9_1", 0)
            + data.get("R10_1", 0)
            + data.get("R11_1", 0)
            + data.get("R12_1", 0)
            + data.get("R13_1", 0)
            + data.get("R14_1", 0)
            + data.get("R15_1", 0)
            + data.get("R16_1", 0)
        )
        data["R17_2"] = (
            data.get("R5_2", 0)
            + data.get("R6_2", 0)
            + data.get("R7_2", 0)
            + data.get("R8_2", 0)
            + data.get("R9_2", 0)
            + data.get("R10_2", 0)
            + data.get("R11_2", 0)
            + data.get("R12_2", 0)
            + data.get("R16_2", 0)
        )
        data["R27_1"] = (
            data.get("R18_1", 0)
            + data.get("R19_1", 0)
            + data.get("R20_1", 0)
            + data.get("R21_1", 0)
            + data.get("R22_1", 0)
            + data.get("R23_1", 0)
            + data.get("R24_1", 0)
            + data.get("R25_1", 0)
        )
        data["R27_2"] = (
            data.get("R18_2", 0)
            + data.get("R19_2", 0)
            + data.get("R20_2", 0)
            + data.get("R21_2", 0)
            + data.get("R22_2", 0)
            + data.get("R23_2", 0)
            + data.get("R24_2", 0)
            + data.get("R25_2", 0)
            + data.get("R43_2", 0)
            + data.get("R44_2", 0)
        )
        data["R28_2"] = data["R27_2"]
        data["R32_2"] = (
            data.get("R28_2", 0)
            + data.get("R29_2", 0)
            + data.get("R30_2", 0)
            + data.get("R31_2", 0)
        )
        vat = data["R32_2"] - data["R17_2"]
        data["R33_2"] = vat if vat > 0 else 0
        data["R34_2"] = -1 * vat if vat < 0 else 0
        data["R35_2"] = 0 if self.R38_2_old > 0 else self.R35_2_old
        data["R37_2"] = (
            data.get("R34_2", 0) + data.get("R35_2", 0) + data.get("R36_2", 0)
        )
        data["R38_2"] = 0 if self.R35_2_old > 0 else self.R38_2_old
        data["R40_2"] = (
            data.get("R33_2", 0) + data.get("R38_2", 0) + data.get("R39_2", 0)
        )
        vat_result = data.get("R37_2", 0) - data.get("R40_2", 0)
        data["R41_2"] = vat_result if vat_result > 0 else 0
        data["R42_2"] = -1 * vat_result if vat_result < 0 else 0
        return data

    def generate_total(self):
        self.ensure_one()
        cust_invoices = self.get_period_invoices(
            ["out_invoice", "out_refund"]
        ).filtered(lambda i: i.correction)
        supp_invoices = self.get_period_invoices(["in_invoice", "in_refund"]).filtered(
            lambda i: i.correction
        )
        cust_vatp_invoices = self.get_period_vatp_invoices(
            ["out_invoice", "out_refund"]
        )
        supp_vatp_invoices = self.get_period_vatp_invoices(["in_invoice", "in_refund"])
        valoare_a = valoare_a1 = tva_a = tva_a1 = 0
        valoare_b = valoare_b1 = tva_b = tva_b1 = 0
        date1 = self.date_to - relativedelta(months=6)
        for inv in cust_vatp_invoices:
            valoare_a += inv.amount_untaxed_signed
            tva_a += inv.amount_tax_signed
            cash_basis_moves = self.env["account.move"].search(
                [("tax_cash_basis_move_id", "=", inv.id), ("date", "<=", self.date_to)]
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
            valoare_b += inv.amount_untaxed_signed
            tva_b += inv.amount_tax_signed
            cash_basis_moves = self.env["account.move"].search(
                [("tax_cash_basis_move_id", "=", inv.id), ("date", "<=", self.date_to)]
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
            "baza_primite": int(
                sum(-1 * inv.amount_untaxed_signed for inv in supp_invoices)
            ),
            "tva_primite": int(
                sum(-1 * inv.amount_tax_signed for inv in supp_invoices)
            ),
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
            "total_precedent": 0,
            "total_curent": 0,
        }
        return data
