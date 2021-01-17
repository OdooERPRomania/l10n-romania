# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime
import logging
import re

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Declaratie394(models.TransientModel):
    _name = "anaf.d394.v3"
    _inherit = "anaf.d394"
    _description = "declaratie 394, v3"

    def build_file(self):
        data_file = """<?xml version="1.0" encoding="UTF-8"?>
            <declaratie394
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="mfp:anaf:dgti:d394:declaratie:v3 D394.xsd"
            xmlns="mfp:anaf:dgti:d394:declaratie:v3"
            """

        year, month = self.get_year_month()
        months = self.get_months_number()
        tip_D394 = "L"
        if months == 3:
            tip_D394 = "T"
        elif months == 6:
            tip_D394 = "S"
        elif months == 12:
            tip_D394 = "A"
        invoices = self.get_period_invoices(
            ["out_invoice", "out_refund",
             "in_invoice", "in_refund",
             "in_receipt"])

        op1 = self._get_op1(invoices)
        sistem_tva = 0
        for val in op1:
            if val["tip"] == "AI":
                sistem_tva = 1

        recipes = self.get_period_invoices(["out_receipt"])
        op2 = self._get_op2(recipes)

        payments = self._get_payments()
        _logger.warning("xmldict")
        _logger.warning(sistem_tva)
        xmldict = {
            "luna": month,
            "an": year,
            "tip_D394": tip_D394,
            "optiune": int(self.optiune),
            "schimb_optiune": int(self.schimb_optiune),
            "prsAfiliat": int(self.prsAfiliat),
            "informatii": self._generate_informatii(invoices, payments, op1, op2),
            "rezumat1": self._generate_rezumat1(invoices, payments, op1, op2),
            "rezumat2": self._generate_rezumat2(recipes, payments, op1, op2),
            "serieFacturi": self._get_inv_series(invoices),
            "lista": self._generate_lista(),
            "facturi": self.generate_facturi(),
            "op1": op1,
            "op2": op2,
        }
        if invoices:
            xmldict.update({"op_efectuate": 1})
        else:
            if recipes:
                xmldict.update({"op_efectuate": 1})
            else:
                xmldict.update({"op_efectuate": 0})
        totalPlataA = 0
        totalPlataA += (
            xmldict["informatii"]["nrCui1"]
            + xmldict["informatii"]["nrCui2"]
            + xmldict["informatii"]["nrCui3"]
            + xmldict["informatii"]["nrCui4"]
        )
        for line in xmldict["rezumat2"]:
            totalPlataA += line["bazaA"] + line["bazaL"] + line["bazaAI"]

        _logger.warning("xmldict")
        company_data = self.generate_company_data()

        xmldict.update(company_data)
        xmldict.update({"totalPlataA": totalPlataA})
        sign = self.generate_sign()
        xmldict.update(sign)
        _logger.warning(xmldict)

        for key, val in xmldict.items():
            if key not in (
                "informatii",
                "rezumat1",
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
    <informatii """
        for key, val in xmldict["informatii"].items():
            data_file += """{}="{}" """.format(key, val)
        data_file += """
    />"""
        for client in xmldict["rezumat1"]:
            data_file += """
    <rezumat1 """
            for key, val in client.items():
                if key != "detaliu":
                    data_file += """{}="{}" """.format(key, val)
            if client["detaliu"]:
                data_file += """>"""
                for line in client["detaliu"]:
                    data_file += """
        <detaliu """
                    for det_key, det_val in line.items():
                        data_file += """{}="{}" """.format(det_key, det_val)
                    data_file += """/>"""
                data_file += """
    </rezumat1>"""
            else:
                data_file += """/>"""
        for client in xmldict["rezumat2"]:
            data_file += """
    <rezumat2 """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        for client in xmldict["serieFacturi"]:
            data_file += """
    <serieFacturi """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        for client in xmldict["lista"]:
            data_file += """
    <lista """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        for client in xmldict["facturi"]:
            data_file += """
    <facturi """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        for client in xmldict["op1"]:
            data_file += """
    <op1 """
            for key, val in client.items():
                if key != "op11":
                    data_file += """{}="{}" """.format(key, val)
            if client["op11"]:
                data_file += """>"""
                for line in client["op11"]:
                    data_file += """<op11 """
                    for key, val in line.items():
                        data_file += """{}="{}" """.format(key, val)
                    data_file += """/>"""
                data_file += """
    </op1>"""
            else:
                data_file += """/>"""
        for client in xmldict["op2"]:
            data_file += """
    <op2 """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""
        data_file += """
    </declaratie394>"""

        return data_file

    def generate_company_data(self):
        if self.company_id.partner_id.vat_number.find("RO") == 1:
            cui = int(self.company_id.partner_id.vat_number[2:])
        else:
            cui = int(self.company_id.partner_id.vat_number)
        vat_payment = self.company_id.partner_id.with_context({
            "check_date": self.date_to}).check_vat_on_payment()
        data = {
            "cui": cui,
            "den": self.company_id.name,
            "adresa": self.company_id.partner_id._display_address(
                without_company=True
            ).replace("\n", ","),
            "telefon": self.company_id.phone,
            "mail": self.company_id.email,
            "caen": self.company_id.caen_code,
            "sistemTVA": 1 if vat_payment else 0,
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

    def generate_facturi(self):
        tag_config = {
            "baza19": {"base_19"},
            "TVA19": {"tva_19"},
            "baza9": {"base_9"},
            "TVA9": {"tva_9"},
            "baza5": {"base_5"},
            "TVA5": {"tva_5"}
        }
        inv_type_dict = {
            "baza20": 0,
            "baza19": 0,
            "baza9": 0,
            "baza5": 0,
            "TVA20": 0,
            "TVA19": 0,
            "TVA9": 0,
            "TVA5": 0
        }
        facturi = []
        invoices1 = self.get_period_invoices(cancel=True)
        invoices = invoices1.filtered(
            lambda r:
            r.move_type == "out_refund" or r.state == "cancel" or
            r.sequence_type in ("autoinv1", "autoinv2"))

        for inv in invoices:
            inv_type = False
            if inv.move_type in ("out_invoice", "out_refund"):
                if inv.state == "cancel":
                    inv_type = 2
                elif inv.move_type == "out_refund":
                    inv_type = 1
                elif inv.sequence_type == "autoinv1":
                    inv_type = 3
            elif inv.sequence_type == "autoinv2":
                inv_type = 4
            if inv_type:
                new_dict = {
                    "tip_factura": inv_type,
                    "serie": inv.sequence_prefix,
                    "nr": inv.sequence_number
                }
                if inv_type == 3 or inv_type == 4:
                    new_dict += inv_type_dict
                    vals = self.get_journal_line_vals(inv)
                    for _key, value in tag_config.items():
                        for tagx in value:
                            new_dict[tagx] += vals.get(tagx)
                facturi.append(new_dict)
        return facturi

    def _get_payments(self):
        tag_config = {
            "base_19": {"base_19"},
            "tva_19": {"tva_19"},
            "base_9": {"base_9"},
            "tva_9": {"tva_9"},
            "base_5": {"base_5"},
            "tva_5": {"tva_5"}
        }
        pay_type_dict = {
            "base_24": 0, "base_20": 0, "base_19": 0, "base_9": 0, "base_5": 0,
            "tva_24": 0, "tva_20": 0, "tva_19": 0, "tva_9": 0, "tva_5": 0,
        }
        payments = []
        types = ["out_invoice", "out_refund", "in_invoice", "in_refund"]
        vatp_invoices = self.get_period_vatp_invoices(types)
        for inv1 in vatp_invoices:
            pay = {
                "type": inv1.move_type,
                "vat_on_payment": inv1.vat_on_payment
            }
            pay += pay_type_dict
            vals = self.get_journal_line_vals(inv1)
            for _key, value in tag_config.items():
                for tagx in value:
                    pay[tagx] += vals.get(tagx)
            payments.append(pay)
            _logger.warning("PPPXXXPPPP")
            _logger.warning(payments)
        return payments

    def _get_op1(self, invoices):
        def _get_partner_type(invoices):
            # Get list of invoices by partner_type
            partner_type = []
            for part_type in invoices.mapped("partner_type"):
                partner_type[part_type] = invoices.filtered(
                    lambda i: i.partner_type == part_type)
            return partner_type

        def _get_operation_type(invoices):
            # Get list of invoices by operatiuon_type
            operation_type = []
            for oper_type in invoices.mapped("operation_type"):
                operation_type[oper_type] = invoices.filtered(
                    lambda i: i.operation_type == oper_type)
            return operation_type

        def _get_partner_data(new_dict, partner):
            if partner_type == "1":
                new_dict["cuiP"] = partner._split_vat(partner.vat)[1]
            elif partner_type == "2":
                if partner.vat:
                    new_dict["cuiP"] = partner._split_vat(partner.vat)[1]
                else:
                    if partner.country_id:
                        new_dict["taraP"] = (
                            partner.country_id
                            and partner.country_id.code.upper()
                        )
                    if partner.city:
                        new_dict["locP"] = partner.city
                    if partner.state_id:
                        new_dict["judP"] = (
                            partner.state_id and partner.state_id.order_code
                        )
                    if partner.street:
                        new_dict["strP"] = partner.street
                    if partner.street2:
                        new_dict["strP"] += partner.street2
                    if partner.street2:
                        new_dict["detP"] = (
                            partner.street2 and partner.street2
                        )
            else:
                new_dict["cuiP"] = partner._split_vat(partner.vat)[1]
            return new_dict

        def _get_cota_list(move_lines):
            cota_list = []
            for move in move_lines:
                cotas = self.get_cota_vals(move)
                _logger.warning("OOOOOOoooo0000")
                _logger.warning(cotas)
                for line in cotas:
                    cota_line = filter(
                        lambda r: r["cota"] == line.get("cota") and r["anaf_code"] == line.get("anaf_code"),
                        cota_list,
                    )
                    if cota_line:
                        cota_line["nr_fact"] += line.get("nr_fact")
                        cota_line["base"] += line.get("base")
                        cota_line["vat"] += line.get("vat")
                    else:
                        cotas.append({
                            "cota": line.get("cota"),
                            "nr_fact": line.get("nr_fact"),
                            "base": line.get("base"),
                            "vat": line.get("vat"),
                            "anaf_code": line.get("anaf_code"),
                        })
            return cota_list

        def _get_vat_data(part_invoices, partner, partner_type, doc_type=False):
            denP = partner.name.replace("&", "-").replace('"', "")
            line = _get_operation_type(part_invoices)
            res_dict = []
            for oper_type, move_lines in line.items():
                partner_dict = {
                    "tip": oper_type,
                    "tip_partener": partner_type,
                    "denP": denP,
                    "tip_document": doc_type,
                }
                partner_dict = _get_partner_data(partner_dict, partner)
                cota_list = _get_cota_list(move_lines)
                for line in cota_list:
                    cota_line = filter(
                        lambda r: r["cota"] == line.get("cota"),
                        res_dict,
                    )
                    if cota_line:
                        cota_line["nr_fact"] += line.get("nr_fact")
                        cota_line["base"] += line.get("base")
                        cota_line["vat"] += line.get("vat")
                        if cota_line.get("anaf_code") != "":
                            anaf_code_line = filter(
                                lambda r: r["anaf_code"] == cota_line.get("anaf_code"),
                                cota_line["op11"],
                            )
                            if anaf_code_line:
                                cota_line["nr_fact"] += cota_line.get("nr_fact")
                                cota_line["base"] += cota_line.get("base")
                                cota_line["vat"] += cota_line.get("vat")
                            else:
                                cota_line["op11"].append({
                                    "nr_fact": cota_line.get("nr_fact"),
                                    "base": cota_line.get("base"),
                                    "vat": cota_line.get("vat"),
                                    "anaf_code": cota_line.get("anaf_code"),
                                })
                    else:
                        new_dict = partner_dict.copy()
                        new_dict.update({
                            "nr_fact": line.get("nr_fact"),
                            "base": line.get("base"),
                            "vat": line.get("vat"),
                        })
                        if line.get("anaf_code") != "":
                            new_dict["op11"] = [{
                                "nr_fact": line.get("nr_fact"),
                                "base": line.get("base"),
                                "vat": line.get("vat"),
                                "anaf_code": line.get("anaf_code"),
                            }]
                        res_dict.append(new_dict)
            return res_dict

        self.ensure_one()
        op1 = []
        _logger.warning("Partener Oper Type")
        partner_types = _get_partner_type(invoices)
        _logger.warning(partner_types)
        for partner_type, part_types_inv in partner_types.items():
            partners = part_types_inv.mapped("partner_id")
            for partner in partners:
                _logger.warning("Partener")
                _logger.warning(partner.name)
                part_invoices = part_types_inv.filtered(
                    lambda r: r.partner_id.id == partner.id
                )
                new_dict = {}
                if partner_type == "2":
                    doc_types = part_invoices.mapped("invoice_origin_d394")
                    _logger.warning(doc_types)
                    for doc_type in doc_types:
                        doctype_invoices = part_invoices.filtered(
                            lambda r: r.invoice_origin_d394 == doc_type
                        )
                        new_dict = _get_vat_data(
                            doctype_invoices, partner, partner_type, doc_type
                        )
                        op1 += new_dict
                else:
                    doctype_invoices = part_invoices
                    new_dict = _get_vat_data(
                        doctype_invoices, partner, partner_type)
                if new_dict:
                    _logger.warning(new_dict)
                    op1 += new_dict
        _logger.warning(op1)
        return op1

    def compute_invoice_taxes_ammount(self, invoices):
        """Helper to get the taxes grouped according their account.tax.group.
        This method is only used when printing the invoice.
        """
        ress = []
        for move in invoices:
            inv_groups = move.amount_by_group
            for group in inv_groups:
                found = False
                for group_f in ress:
                    if group_f[0] == group[0]:
                        group_f[1]["base"] += group[1]["base"]
                        group_f[1]["amount"] += group[1]["amount"]
                        found = True
                if not found:
                    ress.append(group)
        _logger.warning(ress)
        return ress

    def _get_op2(self, receipts):
        op2 = []
        oper_type = "I1"
        months = {
            fields.Date.from_string(receipt.invoice_date).month for receipt in receipts
        }

        nrAMEF = len({receipt.journal_id.id for receipt in receipts})
        nrBF = len(receipts)
        total = 0
        baza20 = baza19 = baza9 = baza5 = 0
        tva20 = tva19 = tva9 = tva5 = 0
        cota_groups = self.compute_invoice_taxes_ammount(receipts)

        for cota_group in cota_groups:
            cota_group_dict = cota_group[1]
            if cota_group[0].name == "TVA 19%":
                baza19 = cota_group_dict["base"]
                tva19 = cota_group_dict["amount"]
            if cota_group[0].name == "TVA 9%":
                baza9 = cota_group_dict["base"]
                tva9 = cota_group_dict["amount"]
            if cota_group[0].name == "TVA 5%":
                baza5 = cota_group_dict["base"]
                tva5 = cota_group_dict["amount"]

            _logger.warning(cota_group[1])
            op2.append(
                {
                    "tip_op2": oper_type,
                    "luna": list(months)[0],
                    "nrAMEF": int(round(nrAMEF)),
                    "nrBF": int(round(nrBF)),
                    "total": int(
                        round(
                            baza20
                            + baza19
                            + baza9
                            + baza5
                            + tva20
                            + tva19
                            + tva9
                            + tva5
                        )
                    ),
                    "baza20": int(round(baza20)),
                    "baza19": int(round(baza19)),
                    "baza9": int(round(baza9)),
                    "baza5": int(round(baza5)),
                    "TVA20": int(round(tva20)),
                    "TVA19": int(round(tva19)),
                    "TVA9": int(round(tva9)),
                    "TVA5": int(round(tva5)),
                }
            )
        return op2

    def _generate_rezumat1(self, invoices, payments, op1, op2):
        self.ensure_one()
        rezumat1 = []
        partner_types = {x["tip_partener"] for x in op1}
        for partner_type in partner_types:
            cotas = {x["cota"] for x in op1 if x["tip_partener"] == partner_type}
            for cota in cotas:
                op1s = []
                if partner_type == "2":
                    doc_types = {
                        x["tip_document"]
                        for x in op1
                        if x["tip_partener"] == partner_type and x["tip"] == "N"
                    }
                    for doc_type in doc_types:
                        _logger.warning("RRRezumaTTTT")
                        _logger.warning(doc_types)

                        op1s = [
                            x
                            for x in op1
                            if x["tip_partener"] == partner_type
                            and x["cota"] == cota
                            and x["tip_document"] == doc_type
                            and x["tip"] == "N"
                        ]
                        if op1s:
                            rezumat1.append(self.generate_rezumat1(invoices, op1s))
                            _logger.warning(" N")
                            _logger.warning(op1s)
                            _logger.warning(self.generate_rezumat1(invoices, op1s))
                    op1s = [
                        x
                        for x in op1
                        if x["tip_partener"] == partner_type
                        and x["cota"] == cota
                        and x["tip"] != "N"
                    ]
                    if op1s:
                        rezumat1.append(self.generate_rezumat1(invoices, op1s))
                        _logger.warning("No N")
                        _logger.warning(op1s)
                        _logger.warning(self.generate_rezumat1(invoices, op1s))
                else:
                    op1s = [
                        x
                        for x in op1
                        if x["tip_partener"] == partner_type and x["cota"] == cota
                    ]
                    if op1s:
                        rezumat1.append(self.generate_rezumat1(invoices, op1s))
                        _logger.warning("Partenr 1")
                        _logger.warning(op1s)
                        _logger.warning(self.generate_rezumat1(invoices, op1s))

        return rezumat1

    def generate_rezumat1(self, invoices, op1s):
        self.ensure_one()
        obj_inv = self.env["account.move"]
        obj_inv_line = self.env["account.move.line"]
        obj_d394_code = self.env["anaf.product.code"]
        partner_type = op1s[0]["tip_partener"]
        oper_type = op1s[0]["tip"]
        cota_amount = int(op1s[0]["cota"])
        rezumat1 = {}
        rezumat1["tip_partener"] = op1s[0]["tip_partener"]
        rezumat1["cota"] = op1s[0]["cota"]
        if cota_amount != 0:
            rezumat1["facturiL"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "L"))
            )
            rezumat1["bazaL"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "L"))
            )
            rezumat1["tvaL"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "L"))
            )
        if partner_type == "1" and cota_amount == 0:
            rezumat1["facturiLS"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "LS"))
            )
            rezumat1["bazaLS"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "LS"))
            )
        if partner_type == "1" and cota_amount != 0:
            rezumat1["facturiA"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "A"))
            )
            rezumat1["bazaA"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "A"))
            )
            rezumat1["tvaA"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "A"))
            )
        if partner_type == "1" and cota_amount != 0:
            rezumat1["facturiAI"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "AI"))
            )
            rezumat1["bazaAI"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "AI"))
            )
            rezumat1["tvaAI"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "AI"))
            )
        if partner_type in ("1", "3", "4") and cota_amount == 0:
            rezumat1["facturiAS"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "AS"))
            )
            rezumat1["bazaAS"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "AS"))
            )
        if (partner_type == "1") and (cota_amount == 0):
            rezumat1["facturiV"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "V"))
            )
            rezumat1["bazaV"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "V"))
            )
            rezumat1["tvaV"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "V"))
            )
        if (partner_type != "2") and (cota_amount != 0):
            rezumat1["facturiC"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "C"))
            )
            rezumat1["bazaC"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "C"))
            )
            rezumat1["tvaC"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "C"))
            )
        if op1s[0]["tip_partener"] == "2" and ("tip_document" in op1s[0]):

            rezumat1["facturiN"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "N"))
            )
            rezumat1["document_N"] = op1s[0]["tip_document"]

            rezumat1["bazaN"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "N"))
            )
        rez_detaliu = []
        for op1 in op1s:
            if op1["op11"]:
                for line in op1["op11"]:
                    code = line["codPR"]
                    new_code = obj_d394_code.search([("name", "=", code)])
                    if len(new_code) >= 2:
                        new_code = new_code[0]
                    if new_code and new_code.parent_id:
                        new_code = new_code.parent_id
                    if rez_detaliu:
                        found = False
                        for val in rez_detaliu:
                            if new_code.name == val["bun"]:
                                found = True
                        if found:
                            for val in rez_detaliu:
                                if new_code.name == val["bun"]:
                                    if op1["tip"] == "L":
                                        val["nrLiv"] += int(round(line["nrFactPR"]))
                                        val["bazaLiv"] += int(round(line["bazaPR"]))
                                        val["tvaLiv"] += int(round(line["tvaPR"]))
                                    if op1["tip"] == "V" and op1["cota"] == 0:
                                        val["nrLivV"] += int(round(line["nrFactPR"]))
                                        val["bazaLivV"] += int(round(line["bazaPR"]))
                                    #    val['tvaLivV'] += int(
                                    #        round(line['tvaPR']))
                                    if op1["tip"] == "A":
                                        val["nrAchiz"] += int(round(line["nrFactPR"]))
                                        val["bazaAchiz"] += int(round(line["bazaPR"]))
                                        val["tvaAchiz"] += int(round(line["tvaPR"]))
                                    if op1["tip"] == "AI":
                                        val["nrAchizAI"] += int(round(line["nrFactPR"]))
                                        val["bazaAchizAI"] += int(round(line["bazaPR"]))
                                        val["tvaAchizAI"] += int(round(line["tvaPR"]))
                                    if op1["tip"] == "C" and op1["cota"] != 0:
                                        val["nrAchizC"] += int(round(line["nrFactPR"]))
                                        val["bazaAchizC"] += int(round(line["bazaPR"]))
                                        val["tvaAchizC"] += int(round(line["tvaPR"]))
                                    if op1["tip"] == "N" and partner_type == "2":
                                        val["nrN"] += int(round(line["nrFactPR"]))
                                        val["valN"] += int(round(line["bazaPR"]))
                        else:
                            val = {}
                            val["bun"] = new_code.name
                            if op1["tip"] == "L":
                                val["nrLiv"] = val["bazaLiv"] = 0
                                val["tvaLiv"] = 0
                            if op1["tip"] == "V" and op1["cota"] == 0:
                                val["nrLivV"] = val["bazaLivV"] = 0
                            #    val['tvaLivV'] = 0
                            if op1["tip"] == "A":
                                val["nrAchiz"] = val["bazaAchiz"] = 0
                                val["tvaAchiz"] = 0
                            if op1["tip"] == "AI":
                                val["nrAchizAI"] = val["bazaAchizAI"] = 0
                                val["tvaAchizAI"] = 0
                            if op1["tip"] == "C" and op1["cota"] != 0:
                                val["nrAchizC"] = val["bazaAchizC"] = 0
                                val["tvaAchizC"] = 0
                            if partner_type == "2":
                                val["nrN"] = val["valN"] = 0
                            if op1["tip"] == "L":
                                val["nrLiv"] += int(round(line["nrFactPR"]))
                                val["bazaLiv"] += int(round(line["bazaPR"]))
                                val["tvaLiv"] += int(round(line["tvaPR"]))
                            if op1["tip"] == "V" and op1["cota"] == 0:
                                val["nrLivV"] += int(round(line["nrFactPR"]))
                                val["bazaLivV"] += int(round(line["bazaPR"]))
                            #    val['tvaLivV'] += int(
                            #        round(line['tvaPR']))
                            if op1["tip"] == "A":
                                val["nrAchiz"] += int(round(line["nrFactPR"]))
                                val["bazaAchiz"] += int(round(line["bazaPR"]))
                                val["tvaAchiz"] += int(round(line["tvaPR"]))
                            if op1["tip"] == "AI":
                                val["nrAchizAI"] += int(round(line["nrFactPR"]))
                                val["bazaAchizAI"] += int(round(line["bazaPR"]))
                                val["tvaAchizAI"] += int(round(line["tvaPR"]))
                            if op1["tip"] == "C" and op1["cota"] != 0:
                                val["nrAchizC"] += int(round(line["nrFactPR"]))
                                val["bazaAchizC"] += int(round(line["bazaPR"]))
                                val["tvaAchizC"] += int(round(line["tvaPR"]))
                            if op1["tip"] == "N" and partner_type == "2":
                                val["nrN"] += int(round(line["nrFactPR"]))
                                val["valN"] += int(round(line["bazaPR"]))
                            rez_detaliu.append(val)
                    else:
                        val = {}
                        val["bun"] = new_code.name
                        if op1["tip"] == "L":
                            val["nrLiv"] = val["bazaLiv"] = 0
                            val["tvaLiv"] = 0
                        if op1["tip"] == "V" and op1["cota"] == 0:
                            val["nrLivV"] = val["bazaLivV"] = 0
                        #    val['tvaLivV'] = 0
                        if op1["tip"] == "A":
                            val["nrAchiz"] = val["bazaAchiz"] = 0
                            val["tvaAchiz"] = 0
                        if op1["tip"] == "AI":
                            val["nrAchizAI"] = val["bazaAchizAI"] = 0
                            val["tvaAchizAI"] = 0
                        if op1["tip"] == "C" and op1["cota"] != 0:
                            val["nrAchizC"] = val["bazaAchizC"] = 0
                            val["tvaAchizC"] = 0
                        if partner_type == "2":
                            val["nrN"] = val["valN"] = 0

                        if op1["tip"] == "L":
                            val["nrLiv"] += int(round(line["nrFactPR"]))
                            val["bazaLiv"] += int(round(line["bazaPR"]))
                            val["tvaLiv"] += int(round(line["tvaPR"]))
                        if op1["tip"] == "V" and op1["cota"] == 0:
                            val["nrLivV"] += int(round(line["nrFactPR"]))
                            val["bazaLivV"] += int(round(line["bazaPR"]))
                        #    val['tvaLivV'] += int(round(line['tvaPR']))
                        if op1["tip"] == "A":
                            val["nrAchiz"] += int(round(line["nrFactPR"]))
                            val["bazaAchiz"] += int(round(line["bazaPR"]))
                            val["tvaAchiz"] += int(round(line["tvaPR"]))
                        if op1["tip"] == "AI":
                            val["nrAchizAI"] += int(round(line["nrFactPR"]))
                            val["bazaAchizAI"] += int(round(line["bazaPR"]))
                            val["tvaAchizAI"] += int(round(line["tvaPR"]))
                        if op1["tip"] == "C" and op1["cota"] != 0:
                            val["nrAchizC"] += int(round(line["nrFactPR"]))
                            val["bazaAchizC"] += int(round(line["bazaPR"]))
                            val["tvaAchizC"] += int(round(line["tvaPR"]))
                        if op1["tip"] == "N" and partner_type == "2":
                            val["nrN"] += int(round(line["nrFactPR"]))
                            val["valN"] += int(round(line["bazaPR"]))
                        rez_detaliu.append(val)
        rezumat1["detaliu"] = rez_detaliu
        return rezumat1

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

    def generate_rezumat2(self, sel_cota, invoices, op1s, op2):
        self.ensure_one()
        obj_inv = self.env["account.move"]
        obj_inv_line = self.env["account.move.line"]
        rezumat2 = {}
        if op1s:
            oper_type = op1s[0]["tip"]
            cota_amount = int(op1s[0]["cota"])
            _logger.warning("Rezumat 2")
            _logger.warning(op1s)
            rezumat2["cota"] = op1s[0]["cota"]
            # To review
            rezumat2["bazaFSLcod"] = 0
            rezumat2["TVAFSLcod"] = 0
            rezumat2["bazaFSL"] = 0
            rezumat2["TVAFSL"] = 0
            rezumat2["bazaFSA"] = 0
            rezumat2["TVAFSA"] = 0
            rezumat2["bazaFSAI"] = 0
            rezumat2["TVAFSAI"] = 0

            rezumat2["bazaBFAI"] = 0
            rezumat2["TVABFAI"] = 0

            rezumat2["bazaL_PF"] = 0
            rezumat2["tvaL_PF"] = 0

            fr_inv = (
                domain
            ) = "r.operation_type == 'L' and \
                r.fiscal_receipt is True"
            inv_lines = self._get_inv_lines(invoices, cota_amount, domain)
            if inv_lines:
                rezumat2["bazaBFAI"] = int(
                    round(
                        sum(
                            line.price_subtotal
                            for line in inv_lines
                            if not line.invoice_id.journal_id.fiscal_receipt
                        )
                    )
                )
                rezumat2["TVABFAI"] = int(
                    round(
                        sum(
                            line.price_normal_taxes
                            and line.price_normal_taxes
                            or line.price_taxes
                            for line in inv_lines
                            if not line.invoice_id.journal_id.fiscal_receipt
                        )
                    )
                )
            rezumat2["nrFacturiL"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "L"))
            )
            rezumat2["bazaL"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "L"))
            )
            rezumat2["tvaL"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "L"))
            )
            rezumat2["nrFacturiA"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] in ("A", "C")))
            )
            rezumat2["bazaA"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] in ("A", "C")))
            )
            rezumat2["tvaA"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] in ("A", "C")))
            )
            rezumat2["nrFacturiAI"] = int(
                round(sum(op["nrFact"] for op in op1s if op["tip"] == "AI"))
            )
            rezumat2["bazaAI"] = int(
                round(sum(op["baza"] for op in op1s if op["tip"] == "AI"))
            )
            rezumat2["tvaAI"] = int(
                round(sum(op["tva"] for op in op1s if op["tip"] == "AI"))
            )
            if cota_amount == 5:
                rezumat2["baza_incasari_i1"] = int(
                    round(sum(x["baza5"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["tva_incasari_i1"] = int(
                    round(sum(x["TVA5"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["baza_incasari_i2"] = int(
                    round(sum(x["baza5"] for x in op2 if x["tip_op2"] == "I2"))
                )
                rezumat2["tva_incasari_i2"] = int(
                    round(sum(x["TVA5"] for x in op2 if x["tip_op2"] == "I2"))
                )
            if cota_amount == 9:
                rezumat2["baza_incasari_i1"] = int(
                    round(sum(x["baza9"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["tva_incasari_i1"] = int(
                    round(sum(x["TVA9"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["baza_incasari_i2"] = int(
                    round(sum(x["baza9"] for x in op2 if x["tip_op2"] == "I2"))
                )
                rezumat2["tva_incasari_i2"] = int(
                    round(sum(x["TVA9"] for x in op2 if x["tip_op2"] == "I2"))
                )
            if cota_amount == 19:
                rezumat2["baza_incasari_i1"] = int(
                    round(sum(x["baza19"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["tva_incasari_i1"] = int(
                    round(sum(x["TVA19"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["baza_incasari_i2"] = int(
                    round(sum(x["baza19"] for x in op2 if x["tip_op2"] == "I2"))
                )
                rezumat2["tva_incasari_i2"] = int(
                    round(sum(x["TVA19"] for x in op2 if x["tip_op2"] == "I2"))
                )
            if cota_amount == 20:
                rezumat2["baza_incasari_i1"] = int(
                    round(sum(x["baza20"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["tva_incasari_i1"] = int(
                    round(sum(x["TVA20"] for x in op2 if x["tip_op2"] == "I1"))
                )
                rezumat2["baza_incasari_i2"] = int(
                    round(sum(x["baza20"] for x in op2 if x["tip_op2"] == "I2"))
                )
                rezumat2["tva_incasari_i2"] = int(
                    round(sum(x["TVA20"] for x in op2 if x["tip_op2"] == "I2"))
                )
            domain = "r.operation_type == 'L' and \
                r.partner_type == '2' and r.amount_total <= 10000"
            inv_lines = self._get_inv_lines(invoices, cota_amount, domain)
        else:
            rezumat2["cota"] = sel_cota
            rezumat2["bazaFSLcod"] = 0
            rezumat2["TVAFSLcod"] = 0
            rezumat2["bazaFSL"] = 0
            rezumat2["TVAFSL"] = 0
            rezumat2["bazaFSA"] = 0
            rezumat2["TVAFSA"] = 0
            rezumat2["bazaFSAI"] = 0
            rezumat2["TVAFSAI"] = 0
            rezumat2["bazaBFAI"] = 0
            rezumat2["TVABFAI"] = 0
            rezumat2["nrFacturiL"] = 0
            rezumat2["bazaL"] = 0
            rezumat2["tvaL"] = 0
            rezumat2["nrFacturiA"] = 0
            rezumat2["bazaA"] = 0
            rezumat2["tvaA"] = 0
            rezumat2["nrFacturiAI"] = 0
            rezumat2["bazaAI"] = 0
            rezumat2["tvaAI"] = 0
            rezumat2["baza_incasari_i1"] = 0
            rezumat2["tva_incasari_i1"] = 0
            rezumat2["baza_incasari_i2"] = 0
            rezumat2["tva_incasari_i2"] = 0
            rezumat2["bazaL_PF"] = 0
            rezumat2["tvaL_PF"] = 0
        return rezumat2

    def _generate_rezumat2(self, invoices, payments, op1, op2):
        self.ensure_one()
        rezumat2 = []
        cotas = set([x["cota"] for x in op1 if x["cota"] != 0] + [5, 9, 19, 20])
        for cota in cotas:
            op1s = [x for x in op1 if x["cota"] == cota]
            rezumat2.append(self.generate_rezumat2(cota, invoices, op1s, op2))
        return rezumat2

    def _generate_lista(self):
        self.ensure_one()
        obj_tax = self.env["account.tax"]
        obj_invoice = self.env["account.move"]
        obj_inv_line = self.env["account.move.line"]
        comp_curr = self.company_id.currency_id
        caens = [
            "1071",
            "4520",
            "4730",
            "47761",
            "47762",
            "4932",
            "55101",
            "55102",
            "55103",
            "5630",
            "0812",
            "9313",
            "9602",
            "9603",
        ]
        lista = []
        invoices = obj_invoice.search(
            [
                ("move_type", "in", ["out_invoice", "out_refund"]),
                ("state", "in", ["open", "paid"]),
                ("invoice_date", ">=", self.date_from),
                ("invoice_date", "<=", self.date_to),
                ("move_type", "!=", "out_receipt"),
                "|",
                ("company_id", "=", self.company_id.id),
                ("company_id", "in", self.company_id.child_ids.ids),
            ]
        )

        companies = set(invoices.mapped("company_id.id"))
        for company in self.env["res.company"].browse(companies):
            if company.codcaen.code.zfill(4) in caens:
                comp_inv = invoices.filtered(lambda r: r.company_id.id == company.id)
                cotas = []
                for invoice in comp_inv:
                    cotas += {tax.id for tax in invoice.tax_ids}
                cotas = set(cotas)
                for cota in obj_tax.browse(cotas):
                    cota_amount = 0
                    if cota.type == "percent":
                        if cota.child_ids:
                            cota_amount = int(abs(cota.child_ids[0].amount) * 100)
                        else:
                            cota_amount = int(cota.amount * 100)
                    elif cota.type == "amount":
                        cota_amount = int(cota.amount)
                    cota_inv = comp_inv.filtered(lambda r: cota.id in r.tax_ids.ids)
                    inv_lines = obj_inv_line.search(
                        [("invoice_id", "in", cota_inv.ids)]
                    )
                    bazab = bazas = tvab = tvas = 0
                    for line in inv_lines:
                        inv_curr = line.invoice_id.currency_id
                        inv_date = line.invoice_id.date_invoice
                        if line.product_id.type in ("product", "consumables"):
                            bazab += inv_curr.with_context({"date": inv_date}).compute(
                                line.price_subtotal, comp_curr
                            )
                            tvab += inv_curr.with_context({"date": inv_date}).compute(
                                line.price_normal_taxes
                                and line.price_normal_taxes
                                or line.price_taxes,
                                comp_curr,
                            )
                        else:
                            bazas += inv_curr.with_context({"date": inv_date}).compute(
                                line.price_subtotal, comp_curr
                            )
                            tvas += inv_curr.with_context({"date": inv_date}).compute(
                                line.price_normal_taxes
                                and line.price_normal_taxes
                                or line.price_taxes,
                                comp_curr,
                            )
                    if bazab != 0:
                        bdict = {
                            "caen": company.codcaen.code.zfill(4),
                            "cota": cota_amount,
                            "operat": 1,
                            "valoare": int(round(bazab)),
                            "tva": int(round(tvab)),
                        }
                        lista.append(bdict)
                    if bazas != 0:
                        sdict = {
                            "caen": company.codcaen.code.zfill(4),
                            "cota": cota_amount,
                            "operat": 2,
                            "valoare": int(round(bazas)),
                            "tva": int(round(tvas)),
                        }
                        lista.append(sdict)
        return lista

    def _get_inv_series(self, invoices):

        regex = re.compile("[^a-zA-Z]")
        ctx = self._context.copy()
        year, month = self.get_year_month()
        ctx["fiscalyear_id"] = year
        # invoices = obj_invoice.search([
        #    ('state', '!=', 'draft'),
        #    ('invoice_date', '>=', self.date_from),
        #    ('invoice_date', '<=', self.date_to),
        #    '|',
        #    ('company_id', '=', self.company_id.id),
        #    ('company_id', 'in', self.company_id.child_ids.ids),
        #    '|',
        #    ('move_type', 'in', ('out_invoice', 'out_refund')),
        #    ('journal_id.sequence_type', 'in', ('autoinv1', 'autoinv2'))
        # ])

        journals = self.env["account.journal"]
        journal_ids = set(invoices.mapped("journal_id.id"))
        seq_dict = []
        _logger.warning(journal_ids)
        for journal in journals.browse(journal_ids):

            journal_invoices = invoices.filtered(
                lambda r: r.journal_id.id == journal.id
            )
            first_name = min(journal_invoices._origin.mapped("name"))
            _logger.warning(journal_invoices)
            _logger.warning(journal_invoices._origin.mapped("name"))
            record_first_name = journal_invoices.filtered(
                lambda r: r.name == first_name
            )
            _logger.warning(record_first_name[0])
            formatt, format_values = journal_invoices._get_sequence_format_param(
                first_name
            )
            type_reset = journal_invoices._deduce_sequence_number_reset(first_name)
            _logger.warning(str(formatt).split("{seq:")[0].format(**format_values))

            no_digit = format_values["seq_length"]
            nr_init = 0
            nr_last = 10 ^ no_digit - 1
            tip = 1
            partner = journal.partner_id
            if journal.sequence_type == "autoinv1":
                tip = 3
            elif journal.sequence_type != "normal":
                tip = 4

            seria = str(formatt).split("{seq:")[0].format(**format_values)
            dict_serie = {
                "tip": tip,
                "serieI": seria,
                "nrI": str(nr_init),
                "nrF": str(nr_last),
            }
            if partner:
                dict_serie["den"] = partner.name
                dict_serie["cui"] = partner._split_vat(partner.vat)[1]

            seq_dict.append(dict_serie)
            if journal.sequence_type == "normal":
                tip = 2
            elif journal.sequence_type == "autoinv1":
                tip = 3
            else:
                tip = 4
            dict_series1 = {"tip": tip, "serieI": seria}
            if type_reset == "month":
                dict_series1.update({"nrI": 0, "nrF": format_values["seq"]})
            else:
                dict_series1.update(
                    {
                        "nrI": str(format_values["seq"] - len(journal_invoices)),
                        "nrF": format_values["seq"],
                    }
                )
            seq_dict.append(dict_series1)
        return seq_dict

    def _generate_informatii(self, invoices, payments, op1, op2):
        informatii = {}
        informatii["nrCui1"] = len(
            {op["cuiP"] for op in op1 if op["tip_partener"] == "1"}
        )
        informatii["nrCui2"] = len([op for op in op1 if op["tip_partener"] == "2"])
        informatii["nrCui3"] = len(
            {op["cuiP"] for op in op1 if op["tip_partener"] == "3"}
        )
        informatii["nrCui4"] = len(
            {op["cuiP"] for op in op1 if op["tip_partener"] == "4"}
        )
        informatii["nr_BF_i1"] = sum(op["nrBF"] for op in op2 if op["tip_op2"] == "I1")
        informatii["incasari_i1"] = sum(
            op["total"] for op in op2 if op["tip_op2"] == "I1"
        )
        informatii["incasari_i2"] = sum(
            op["total"] for op in op2 if op["tip_op2"] == "I2"
        )
        informatii["nrFacturi_terti"] = len(
            set(invoices.filtered(lambda r: r.journal_id.sequence_type == "autoinv2"))
        )

        informatii["nrFacturi_benef"] = len(
            set(invoices.filtered(lambda r: r.journal_id.sequence_type == "autoinv1"))
        )
        informatii["nrFacturi"] = len(
            set(
                invoices.filtered(
                    lambda r: r.move_type in ("out_invoice", "out_refund")
                )
            )
        )
        informatii["nrFacturiL_PF"] = 0
        # informatii['nrFacturiLS_PF'] = len(
        #    set(invoices.filtered(lambda r: r.operation_type == 'LS' and
        #                                    r.partner_type == '2' and
        #                                    r.amount_total <= 10000)))
        # informatii['val_LS_PF'] = int(round(sum(
        #    inv.amount_total for inv in invoices.filtered(
        #        lambda r: r.operation_type == 'LS' and
        #                  r.partner_type == '2' and
        #                  r.amount_total <= 10000))))
        informatii["tvaDedAI24"] = int(
            round(
                sum(
                    op["tva_24"]
                    for op in payments
                    if op["type"] in ("in_invoice", "in_refund")
                    and op["vat_on_payment"] is True
                )
            )
        )
        informatii["tvaDedAI20"] = int(
            round(
                sum(
                    op["tva_20"]
                    for op in payments
                    if op["type"] in ("in_invoice", "in_refund")
                    and op["vat_on_payment"] is True
                )
            )
        )
        informatii["tvaDedAI19"] = int(
            round(
                sum(
                    op["tva_19"]
                    for op in payments
                    if op["type"] in ("in_invoice", "in_refund")
                    and op["vat_on_payment"] is True
                )
            )
        )
        informatii["tvaDedAI9"] = int(
            round(
                sum(
                    op["tva_9"]
                    for op in payments
                    if op["type"] in ("in_invoice", "in_refund")
                    and op["vat_on_payment"] is True
                )
            )
        )
        informatii["tvaDedAI5"] = int(
            round(
                sum(
                    op["tva_5"]
                    for op in payments
                    if op["type"] in ("in_invoice", "in_refund")
                    and op["vat_on_payment"] is True
                )
            )
        )

        comm_partner = self.company_id.partner_id.commercial_partner_id
        ctx = dict(self._context)
        ctx.update({"check_date": self.date_to})

        if comm_partner.with_context(ctx)._check_vat_on_payment():
            informatii["tvaDed24"] = int(
                round(
                    sum(
                        op["tva_24"]
                        for op in payments
                        if op["type"] in ("in_invoice", "in_refund")
                        and op["vat_on_payment"] is False
                    )
                )
            )
            informatii["tvaDed20"] = int(
                round(
                    sum(
                        op["tva_20"]
                        for op in payments
                        if op["type"] in ("in_invoice", "in_refund")
                        and op["vat_on_payment"] is False
                    )
                )
            )
            informatii["tvaDed19"] = int(
                round(
                    sum(
                        op["tva_19"]
                        for op in payments
                        if op["type"] in ("in_invoice", "in_refund")
                        and op["vat_on_payment"] is False
                    )
                )
            )
            informatii["tvaDed9"] = int(
                round(
                    sum(
                        op["tva_9"]
                        for op in payments
                        if op["type"] in ("in_invoice", "in_refund")
                        and op["vat_on_payment"] is False
                    )
                )
            )
            informatii["tvaDed5"] = int(
                round(
                    sum(
                        op["tva_5"]
                        for op in payments
                        if op["type"] in ("in_invoice", "in_refund")
                        and op["vat_on_payment"] is False
                    )
                )
            )
            informatii["tvaCol24"] = int(
                round(
                    sum(
                        op["tva_24"]
                        for op in payments
                        if op["type"] in ("out_invoice", "out_refund")
                        and op["vat_on_payment"] is True
                    )
                )
            )
            informatii["tvaCol20"] = int(
                round(
                    sum(
                        op["tva_20"]
                        for op in payments
                        if op["type"] in ("out_invoice", "out_refund")
                        and op["vat_on_payment"] is True
                    )
                )
            )
            informatii["tvaCol19"] = int(
                round(
                    sum(
                        op["tva_19"]
                        for op in payments
                        if op["type"] in ("out_invoice", "out_refund")
                        and op["vat_on_payment"] is True
                    )
                )
            )
            informatii["tvaCol9"] = int(
                round(
                    sum(
                        op["tva_9"]
                        for op in payments
                        if op["type"] in ("out_invoice", "out_refund")
                        and op["vat_on_payment"] is True
                    )
                )
            )
            informatii["tvaCol5"] = int(
                round(
                    sum(
                        op["tva_5"]
                        for op in payments
                        if op["type"] in ("out_invoice", "out_refund")
                        and op["vat_on_payment"] is True
                    )
                )
            )
        informatii["incasari_ag"] = 0
        informatii["costuri_ag"] = 0
        informatii["marja_ag"] = 0
        informatii["tva_ag"] = 0
        informatii["pret_vanzare"] = 0
        informatii["pret_cumparare"] = 0
        informatii["marja_antic"] = 0
        informatii["tva_antic"] = 0
        informatii["solicit"] = int(self.solicit)
        if self.solicit:
            informatii["achizitiiPE"] = int(self.achizitiiPE)
            informatii["achizitiiCR"] = int(self.achizitiiCR)
            informatii["achizitiiCB"] = int(self.achizitiiCB)
            informatii["achizitiiCI"] = int(self.achizitiiCI)
            informatii["achizitiiA"] = int(self.achizitiiA)
            informatii["achizitiiB24"] = int(self.achizitiiB24)
            informatii["achizitiiB20"] = int(self.achizitiiB20)
            informatii["achizitiiB19"] = int(self.achizitiiB19)
            informatii["achizitiiB9"] = int(self.achizitiiB9)
            informatii["achizitiiB5"] = int(self.achizitiiB5)
            informatii["achizitiiS24"] = int(self.achizitiiS24)
            informatii["achizitiiS20"] = int(self.achizitiiS20)
            informatii["achizitiiS19"] = int(self.achizitiiS19)
            informatii["achizitiiS9"] = int(self.achizitiiS9)
            informatii["achizitiiS5"] = int(self.achizitiiS5)
            informatii["importB"] = int(self.importB)
            informatii["acINecorp"] = int(self.acINecorp)
            informatii["livrariBI"] = int(self.livrariBI)
            informatii["BUN24"] = int(self.BUN24)
            informatii["BUN20"] = int(self.BUN20)
            informatii["BUN19"] = int(self.BUN19)
            informatii["BUN9"] = int(self.BUN9)
            informatii["BUN5"] = int(self.BUN5)
            informatii["valoareScutit"] = int(self.valoareScutit)
            informatii["BunTI"] = int(self.BunTI)
            informatii["Prest24"] = int(self.Prest24)
            informatii["Prest20"] = int(self.Prest20)
            informatii["Prest19"] = int(self.Prest19)
            informatii["Prest9"] = int(self.Prest9)
            informatii["Prest5"] = int(self.Prest5)
            informatii["PrestScutit"] = int(self.PrestScutit)
            informatii["LIntra"] = int(self.LIntra)
            informatii["PrestIntra"] = int(self.PrestIntra)
            informatii["Export"] = int(self.Export)
            informatii["livINecorp"] = int(self.livINecorp)
            informatii["efectuat"] = int(self.solicit)
        return informatii
