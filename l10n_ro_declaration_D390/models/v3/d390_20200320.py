# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

dict_tags = {
    "01 - BAZA": "L",
    "03 - BAZA": "P",
    "20 - BAZA": "A",
    "22_1 - BAZA": "S",
    }



class Declaratie390(models.TransientModel):
    _name = "anaf.d390.v3"
    _inherit = "anaf.d390"
    _description = "declaratie 390, v3"

    def build_file(self):
        year, month = self.get_year_month()
        month_invoices = self.get_period_invoices(
            ["out_invoice", "out_refund", "in_invoice", "in_refund", "in_receipt"]
        )
        invoices = month_invoices.filtered(lambda i: i.partner_type == "3")
        if not invoices:
            raise UserError(_("No intracomunitarian transation"))

        data_file = """<?xml version="1.0" encoding="UTF-8"?>
<declaratie390 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="mfp:anaf:dgti:d390:declaratie:v3 D390.xsd"
               xmlns="mfp:anaf:dgti:d390:declaratie:v3"
               """

        xmldict = {
            "luna": str(int(month)),
            "an": year,
            "d_rec": int(self.rectificative),
            "totalPlata_A": 0,
        }
        sign = self.generate_sign()
        xmldict.update(sign)
        company_data = self.generate_company_data()
        xmldict.update(company_data)
        operatie = self._get_operatie(invoices)
        xmldict.update({"operatie": operatie})
        rezumat = self._get_rezumat(operatie)
        xmldict.update({"rezumat": rezumat})
        cos = self._get_cos()
        if len(cos)>0:
            xmldict.update({"cos": cos})


        if "rezumat" in xmldict:
            totalPlata_A = (
                xmldict["rezumat"]["total_baza"] + xmldict["rezumat"]["nrOPI"]
            )
            xmldict["totalPlata_A"] = totalPlata_A

        for key, val in xmldict.items():
            if key not in ("operatie", "rezumat", "cos"):
                data_file += """{}="{}" """.format(key, val)
        data_file += """>"""

        nr_pag = 0
        if "operatie" in xmldict:
            nr_pag += 1
        if "cos" in xmldict:
            nr_pag += 1
        xmldict["rezumat"]["nr_pag"] = nr_pag

        data_file += """
    <rezumat """
        for key, val in xmldict["rezumat"].items():
            data_file += """{}="{}" """.format(key, val)
        data_file += """/>"""

        if "cos" in xmldict:
            for client in xmldict["cos"]:
                data_file += """
            <cos """
                for key, val in client.items():
                    data_file += """{}="{}" """.format(key, val)
                data_file += """/>"""


        for client in xmldict["operatie"]:
            data_file += """
    <operatie """
            for key, val in client.items():
                data_file += """{}="{}" """.format(key, val)
            data_file += """/>"""

        data_file += """
</declaratie390>"""
        _logger.warning(data_file)
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

    def _is_R(self, line):
        res = False
        if (
            line.product_id.anaf_code_id.parent_id.name == "21"
            or line.product_id.anaf_code_id.name == "21"
        ):
            res = True
        return res

    def _get_operation_type(self, line):
        operation_type = ""
        for tag in line.tax_tag_ids:
            tag_name = tag.name[1:]
            operation_type = dict_tags[tag_name]
        return operation_type

    def _get_operatie(self, invoices):
        self.ensure_one()
        operatii = []
        partner_ids = invoices.mapped("partner_id")
        for partner in partner_ids:
            denO = partner.name.replace("&", "-").replace('"', "")
            (
                country_code,
                identifier_type,
                vat_number,
            ) = partner._parse_anaf_vat_info()
            partner_dict = {
                "tara": country_code,
                "codO": vat_number,
                "denO": denO,
            }
            part_invoices = invoices.filtered(lambda r: r.partner_id.id == partner.id)
            for inv in part_invoices:
                sign = 1
                if inv.move_type in [
                    "out_invoice",
                    "out_receipt",
                    "in_refund",
                ]:
                    sign = -1
                for line in inv.invoice_line_ids:
                    if self._is_R(line):
                        oper = "R"
                    else:
                        oper = self._get_operation_type(line)
                    oper_line = list(
                        filter(
                            lambda r: r["tip"] == oper and r["codO"] == vat_number,
                            operatii,
                        )
                    )
                    if oper_line:
                        oper_line[0]["baza"] += int(round(sign * line.balance))
                    else:
                        new_dict = partner_dict.copy()
                        new_dict.update(
                            {
                                "tip": oper,
                                "baza": int(round(sign * line.balance)),
                            }
                        )
                        operatii.append(new_dict)
        _logger.warning(operatii)
        return operatii

    def _get_rezumat(self, operatie):
        nrOperatori = len(operatie)
        dict_rezumat = {"L": 0, "T": 0, "A": 0, "P": 0, "S": 0, "R": 0}

        for item in operatie:
            for type_op in dict_rezumat.keys():
                if item["tip"] == type_op:
                    dict_rezumat[type_op] += item["baza"]
        total_baza = sum([val for val in dict_rezumat.values()])
        rezumat = {
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

    def _get_cos(self):

        moves_given = self.env["stock.picking"].search(
            [("date_done", ">=", self.date_from),
             ("date_done", "<=", self.date_to)
             ])
        lists_cos = []
        for picking in moves_given:
            if picking.notice:
                contact = picking.partner_id
                country_code = contact._map_anaf_country_code(contact.country_id.code) or ""
                if country_code in contact._get_anaf_europe_codes():

                    if not picking.new_contact :
                        t_cos = ("A",
                                 contact.country_id.code,
                                 contact.vat_number)
                        lists_cos.append(t_cos)
        moves_new = self.env["stock.picking"].search(
            [("date_transfer_new_contact", ">=", self.date_from),
             ("date_transfer_new_contact", "<=", self.date_to)
             ])
        for picking in moves_new:
            if picking.notice:
                contact = picking.partner_id
                new_contact = picking.new_contact
                country_code = contact._map_anaf_country_code(contact.country_id.code) or ""
                new_country_code = new_contact._map_anaf_country_code(new_contact.country_id.code) or ""
                if new_country_code in  contact._get_anaf_europe_codes():
                    if new_contact :
                        t_cos = ("B",
                                 country_code,
                                 contact.vat_number,
                                 new_country_code,
                                 new_contact.vat_number)
                        lists_cos.append(t_cos)
        s_cos = list(set(lists_cos))

        dicts_cos = []
        for item in s_cos:
            if len(item) == 3 :
                dict_cos = {"tip" : item[0],
                            "tara_m1" : item[1],
                            "cod_m1": item[2]
                            }
            if len(item) == 5 :
                dict_cos = {"tip": item[0],
                            "tara_m1": item[1],
                            "cod_m1": item[2],
                            "motiv": "2",
                            "tara_m2": item[3],
                            "cod_m2": item[4]
                            }
            dicts_cos.append(dict_cos)

        return dicts_cos

