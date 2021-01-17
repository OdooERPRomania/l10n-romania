# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)
dict_tags = {
    "11_1 - TVA": [5, "L", "TVA"],
    "11_1 - BAZA": (5, "L", "BAZA", "11_1 - TVA"),
    "09_1 - BAZA": (19, "N", "BAZA", "09_1 - TVA"),
    "09_1 - TVA": (19, "N", "TVA", "09_1 - BAZA"),
    "09_2 - BAZA": (19, "N", "BAZA", "09_2 - TVA", "%50?"),
    "09_2 - TVA": (19, "N", "TVA", "09_2 - BAZA", "%50?"),
    "10_1 - TVA": (9, "N", "TVA", "10_1 - BAZA"),
    "10_1 - BAZA": (9, "N", "BAZA", "10_1 - TVA"),
    "10_2 - TVA": (9, "N", "TVA", "10_2 - BAZA", "%50?"),
    "10_2 - BAZA": (9, "N", "BAZA", "10_2 - TVA", "%50?"),
    "11_1 - BAZA": (5, "N", "BAZA", "11_1 - TVA"),
    "11_1 - TVA": (5, "N", "TVA", "09_1 - BAZA"),
    "11_2 - TVA": (5, "N", "TVA", "11_2 - BAZA"),
    "12_1 - BAZA": (19, "N", "BAZA", "12_1 - TVA"),
    "12_1 - TVA": (19, "N", "BAZA", "12_1 - BAZA"),
    "12_2 - BAZA": (9, "N", "BAZA", "12_2 - TVA"),
    "12_2 - TVA": (9, "N", "TVA", "12_2 - BAZA"),
    "12_3 - BAZA": (5, "N", "BAZA", "12_3 - TVA"),
    "12_3 - TVA": (5, "N", "TVA", "12_3 - BAZA"),
    "01 - BAZA": (5, "L", "BAZA", "01 - BAZA"),
    "01 - TVA": (5, "L", "TVA", "01 - BAZA"),
    "03 - TVA": (5, "P", "TVA", "01 - BAZA"),
    "03 - BAZA": (5, "P", "TVA", "01 - BAZA"),
    "05 - BAZA": (19, "N", "BAZA", "05 - TVA"),
    "05 - TVA": (19, "L", "TVA", "05 - BAZA"),
    "05_1 - BAZA": (9, "L", "BAZA", "09_1 - TVA"),
    "05_1 - TVA": (9, "L", "TVA", "09_1 - BAZA"),
    "06 - BAZA": (19, "N", "BAZA", "06 - TVA"),
    "06 - TVA": (19, "N", "TVA", "06 - BAZA"),
    "07 - BAZA": (9, "S", "BAZA", "07 - TVA"),
    "07 - TVA": (9, "S", "TVA", "07 - BAZA"),
    "07_1 - BAZA": (9, "S", "BAZA", "07_1 - TVA"),
    "07_1 - TVA": (9, "S", "TVA", "07_1 - BAZA"),
    "08 - BAZA": (19, "N", "BAZA", "08 - TVA"),
    "08 - TVA": (19, "N", "TVA", "08 - BAZA"),
    "09 - BAZA": (19, "N", "BAZA", "09 - TVA"),
    "09 - TVA": (19, "N", "TVA", "09 - BAZA"),
    "10 - BAZA": (19, "N", "BAZA", "10 - TVA"),
    "10 - TVA": (19, "N", "TVA", "10 - BAZA"),
    "10_1 - BAZA": (19, "N", "BAZA", "10_1 - TVA"),
    "10_1 - TVA": (19, "N", "TVA", "10_1 - BAZA"),
    "10_2 - BAZA": (19, "N", "BAZA", "10_2 - TVA"),
    "10_2 - TVA": (19, "N", "TVA", "10_2 - BAZA"),
    "13 - BAZA": (0, "N", "BAZA", ""),
    "14 - BAZA": (0, "N", "BAZA", ""),
    "15 - BAZA": (0, "N", "BAZA", ""),
    "16 - BAZA": (19, "N", "BAZA", "16 - TVA"),
    "16 - TVA": (19, "N", "TVA", "16 - BAZA"),
    "17 - BAZA": (19, "N", "BAZA", "17 - BAZA"),
    "17 - TVA": (19, "N", "TVA", "17 - BAZA"),
    "18 - BAZA": (19, "N", "BAZA", "18 - TVA"),
    "18 - TVA": (19, "N", "TVA", "18 - BAZA"),
    "20 - BAZA": (19, "L", "BAZA", "20 - TVA"),
    "20 - TVA": (19, "L", "TVA", "20 - BAZA"),
    "20_1 - BAZA": (19, "L", "BAZA", "20_1 - TVA"),
    "20_1 - TVA": (19, "L", "TVA", "20_1 - BAZA"),
    "21 - BAZA": (19, "N", "BAZA", "21 - TVA"),
    "21 - TVA": (19, "N", "TVA", "21 - BAZA"),
    "22 - BAZA": (19, "S", "BAZA", "22 - TVA"),
    "22 - TVA": (19, "S", "TVA", "22 - BAZA"),
    "22_1 - BAZA": (19, "S", "BAZA", "22_1 - TVA"),
    "22_1 - TVA": (19, "S", "TVA", "22_1 - BAZA"),
    "23 - BAZA": (19, "N", "BAZA", "23 - TVA"),
    "23 - TVA": (19, "N", "TVA", "23 - BAZA"),
    "24 - BAZA": (19, "N", "BAZA", "24 - TVA"),
    "24 - TVA": (19, "N", "TVA", "24 - BAZA"),
    "24.1 - BAZA": (19, "N", "BAZA", "24_1 - TVA"),
    "24_1 - BAZA": (19, "N", "BAZA", "24_1 - TVA"),
    "24_1 - TVA": (19, "N", "TVA", "24_1 - BAZA"),
    "24_2 - BAZA": (19, "N", "BAZA", "24_2 - TVA"),
    "24_2 - TVA": (19, "N", "TVA", "24_2 - BAZA"),
    "25 - BAZA": (19, "N", "BAZA", "25 - TVA"),
    "25 - TVA": (19, "N", "TVA", "25 - BAZA"),
    "25_1 - BAZA": (9, "N", "BAZA", "25_1 - TVA"),
    "25_1 - TVA": (9, "N", "TVA", "25_1 - BAZA"),
    "25_2 - BAZA": (19, "N", "BAZA", "25_2 - TVA"),
    "25_2 - TVA": (19, "N", "TVA", "25_2 - BAZA"),
    "26 - BAZA": (19, "N", "BAZA", "26 - TVA"),
    "26 - TVA": (19, "N", "TVA", "26 - BAZA"),
    "26_1 - BAZA": (5, "N", "BAZA", "26_1 - TVA"),
    "26_1 - TVA": (5, "N", "TVA", "26_1 - BAZA"),
    "26_2 - BAZA": (19, "N", "BAZA", "26_2 - TVA"),
    "26_2 - TVA": (19, "N", "TVA", "26_2 - BAZA"),
    "27 - BAZA": (19, "N", "BAZA", "27 - TVA"),
    "27 - TVA": (19, "N", "TVA", "27 - BAZA"),
    "27_1 - BAZA": (19, "N", "BAZA", "27_1 - TVA"),
    "27_1 - TVA": (19, "N", "TVA", "27_1 - BAZA"),
    "27_2 - BAZA": (9, "N", "BAZA", "27_2 - TVA"),
    "27_2 - TVA": (9, "N", "TVA", "27_2 - BAZA"),
    "27_3 - BAZA": (19, "N", "BAZA", "27_3 - TVA"),
    "27_3 - TVA": (19, "N", "TVA", "27_3 - BAZA"),
    "28 - TVA": (19, "N", "TVA", ""),
    "29 - TVA": (19, "N", "TVA", ""),
    "30 - BAZA": (0, "N", "BAZA", ""),
    "30_1 - BAZA": (0, "N", "BAZA", ""),
    "33 - TVA": (19, "N", "TVA", ""),
    "34 - BAZA": (19, "N", "BAZA", "34 - TVA"),
    "34 - TVA": (19, "N", "TVA", "34 - BAZA"),
    "35 - TVA": (19, "N", "TVA", ""),
}


class Declaratie390(models.TransientModel):
    _name = "anaf.d390.v3"
    _inherit = "anaf.d390"
    _description = "declaratie 390, v3"

    def build_file(self):
        year, month = self.get_year_month()
        months = self.get_months_number()
        obj_invoice = self.env["account.move"]

        invoices = obj_invoice.search(
            [
                ("state", "in", ["posted"]),
                ("move_type", "!=", "out_receipt"),
                ("invoice_date", ">=", self.date_from),
                ("invoice_date", "<=", self.date_to),
                "|",
                ("company_id", "=", self.company_id.id),
                ("company_id", "in", self.company_id.child_ids.ids),
            ]
        )

        data_file = """<?xml version="1.0" encoding="UTF-8"?>
            <declaratie390
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="mfp:anaf:dgti:d390:declaratie:v3"
            xmlns="mfp:anaf:dgti:d390:declaratie:v3"
            """

        xmldict = {
            "luna": month,
            "an": year,
            "d_rec": None,
            "totalPlata_A": None,
        }

        totalPlataA = 0

        _logger.warning("xmldict")
        sign = self.generate_sign()
        company_data = self.generate_company_data()
        xmldict.update(sign)
        xmldict.update(company_data)
        xmldict.update({"totalPlataA": totalPlataA})
        sign = self.generate_sign()
        operatie = self._get_operatie(invoices)
        rezumat = self._get_rezumat(operatie)
        xmldict.update({"operatie": operatie})
        xmldict.update({"rezumat": rezumat})
        _logger.warning(xmldict)

        for key, val in xmldict.items():
            if key not in (
                "operatie",
                "rezumat",
                "rezumat2",
                "serieFacturi",
                "lista",
                "facturi",
                "op1",
                "op2",
            ):
                data_file += """{}="{}" """.format(key, val)
                _logger.warning(key)
                _logger.warning(val)
        data_file += """>"""

        data_file += """
    <rezumat """
        for key, val in xmldict["rezumat"].items():
            data_file += """{}="{}" """.format(key, val)

        data_file += """
    />"""

        for client in xmldict["operatie"]:
            data_file += """
    <op2 """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        data_file += """
    </declaratie390>"""

        return data_file

    def generate_company_data(self):
        if self.company_id.partner_id.vat_number.find("RO") == 1:
            cui = int(self.company_id.partner_id.vat_number[2:])
        else:
            cui = int(self.company_id.partner_id.vat_number)

        data = {
            "cui": cui,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(
                without_company=True
            ).replace("\n", ","),
            "telefon": self.company_id.phone,
            "fax": self.company_id.phone,
            "mail": self.company_id.email,
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

    def generate_sign(self):
        signer = self.signature_id
        data = {
            "tip_intocmit": 1,
            "den_intocmit": signer.name,
            "Dcif_intocmit": signer.vat,
        }
        if signer.type == "company":
            data.update({"calitate_intocmit": signer.quality})
        else:
            data.update({"functie_intocmit ": signer.function})
        return data

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
        invoices_ids = invoices.mapped("id")
        months_year = self.get_months_period()
        for month, year in months_year:
            if month < 12:
                end_months = datetime.datetime(year, month + 1, 1)
            else:
                end_months = datetime.datetime(year + 1, 1, 1)
            invoices = self.env["account.move"].search(
                [
                    ("state", "=", "posted"),
                    ("invoice_date", ">=", datetime.datetime(year, month, 1)),
                    ("invoice_date", "<", end_months),
                    ("company_id", "=", self.company_id.id),
                    ("id", "in", invoices_ids),
                ]
            )

            invoices.sorted(key=lambda r: r.invoice_date)
            invoice_montly.append(invoices)
        return invoice_montly

    def _get_operatie(self, invoices):
        def _is_R(invoices):
            res = False
            inv_lines = []
            for inv in invoices:
                if inv.invoice_line_ids:
                    inv_lines.append(inv.invoice_line_ids)

            codes = inv.invoice_line_ids.mapped("product_id.anaf_code_id")

            for line in inv_lines:
                _logger.warning(line.product_id.anaf_code_id.parent_id.name)
                if (
                    line.product_id.anaf_code_id.parent_id.name == "21"
                    or line.product_id.anaf_code_id.name == "21"
                ):
                    res = True
            return res

        def _get_operation_type(invoices, R):
            ### Is used to determine the type of operation.
            ###   Input: more invoices
            ###   Return: a dictionary keys operation type and values are invoice lines for this operation type

            operation_type = {"L": [], "T": [], "A": [], "P": [], "S": [], "R": []}

            mv_line_obj = self.env["account.move.line"]
            invoices_id = []
            for invoice in invoices:
                invoices_id.append(invoice.id)

            domain = [
                ("move_id.id", "in", invoices_id),
                ("tax_exigible", "=", True),
                ("tax_tag_ids", "!=", False),
                ("move_id.state", "=", "posted"),
            ]

            move_lines = mv_line_obj.search(domain)
            _logger.warning("THISSSSSS")
            _logger.warning(move_lines)
            for record in move_lines:

                for tag in record.tax_tag_ids:
                    _logger.warning(tag)
                    tag_name = tag.name[1:]
                    type = dict_tags[tag_name][1]
                    if type != "N":
                        if type == "L":
                            if R:
                                operation_type["R"].append(record)
                                continue
                        operation_type[type].append(record)
            # _logger.warning('Move Linesssss')
            # _logger.warning(operation_type)
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
                            mv_line_obj._get_refund_tax_audit_condition(record)
                            and -1
                            or 1
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

        def _get_data(part_invoices, partner, R):
            denP = partner.name.replace("&", "-").replace('"', "")
            #  operation type
            line = _get_operation_type(part_invoices, R)
            res_dict = []
            new_dict = {}
            _logger.warning("OOOOOOoooo0000")
            _logger.warning(line)
            for oper_type, move_lines in line.items():
                if len(move_lines) > 0:
                    tags_line = _get_vat_line(move_lines)[0]
                    _logger.warning("OOOOOOoooo0000")
                    _logger.warning(tags_line)
                    _logger.warning(oper_type)

                    # base_cota , tva_cota , invoices_number dicts it is used  for sort on cota TVA
                    base_cota = 0

                    for key in tags_line.keys():
                        if dict_tags[key][2] == "BAZA":
                            base_cota += tags_line[key]
                    tara = partner.country_id.code
                    codO = partner._split_vat(partner.vat)[1]
                    new_dict = {
                        "tip": oper_type,
                        "tara": tara,
                        "codO": codO,
                        "denO": partner.name,
                        "baza": base_cota,
                    }
                    res_dict.append(new_dict)
                    # _logger.warning(new_dict)
            return res_dict

        self.ensure_one()

        obj_partner = self.env["res.partner"]

        comp_curr = self.company_id.currency_id
        operatii = []

        partner_ids = invoices.mapped("partner_id.id")

        for partner in obj_partner.browse(partner_ids):
            part_invoices = invoices.filtered(lambda r: r.partner_id.id == partner.id)
            part_invoices_noR = part_invoices.filtered(lambda r: _is_R(r) == False)
            part_invoices_R = part_invoices.filtered(lambda r: _is_R(r) == True)
            _logger.warning("FFFFLT")
            _logger.warning(partner.name)
            if len(part_invoices_noR) > 0:
                new_dict = _get_data(part_invoices_noR, partner, False)
                operatii += new_dict
            if len(part_invoices_R) > 0:
                new_dict = _get_data(part_invoices_R, partner, True)
                operatii += new_dict

        _logger.warning(operatii)
        return operatii

    def _get_inv_lines(self, invoices, sel_cota, domain):
        obj_inv_line = self.env["account.move.line"]
        inv_lines = False
        if invoices:
            invs = invoices.filtered(lambda r: domain)
            domain = [("move_id", "in", invs.ids)]
            inv_lines = obj_inv_line.search(domain)
            cotas = []
            for inv_line in inv_lines:
                cotas += [tax for tax in inv_line.tax_ids]
            filtered_inv_lines = []
            cota_amount = 0
            for cota in cotas:
                cota_inv = inv_lines.filtered(lambda r: cota.id in r.tax_ids.ids)
                cota_amount = 0
                if cota.amount_type == "percent":
                    if cota.children_tax_ids:
                        cota_amount = int(abs(cota.children_tax_ids[0].amount) * 100)
                    else:
                        cota_amount = int(cota.amount * 100)
                elif cota.amount_type == "amount":
                    cota_amount = int(cota.amount)
                if cota_amount == sel_cota:
                    filtered_inv_lines = []
                    for inv_line in inv_lines:
                        tax = inv_line.invoice_line_tax_id
                        if cota.id in tax.ids:
                            filtered_inv_lines.append(inv_line.id)
            inv_lines = obj_inv_line.browse(filtered_inv_lines)
        return inv_lines

    def _get_rezumat(self, operatie):

        nr_pag = 1
        nrOperatori = len(operatie)
        dict_rezumat = {"L": 0, "T": 0, "A": 0, "P": 0, "S": 0, "R": 0}

        for item in operatie:
            for type_op in dict_rezumat.keys():
                if item["tip"] == type_op:
                    dict_rezumat[type_op] += item["baza"]
        total_baza = sum([val for val in dict_rezumat.values()])
        rezumat = {
            "nr_pag": nr_pag,
            "nrOPI": nrOperatori,
            "bazaL": dict_rezumat["L"],
            "bazaT": dict_rezumat["T"],
            "bazaA": dict_rezumat["A"],
            "bazaP": dict_rezumat["P"],
            "bazaS": dict_rezumat["S"],
            "bazaR": dict_rezumat["R"],
            "total_baza": total_baza,
        }
        return rezumat
