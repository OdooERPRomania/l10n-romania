# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from copy import deepcopy
from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)

# {'14 - BAZA': 0.0, '11 - BAZA': 0.0, '10 - BAZA': 0.0, '09 - BAZA': 200.0, '11 - TVA': 0.0, '10 - TVA': 0.0, '09 - TVA': 38.0}
# {'14 - BAZA': 800.0}
# {}
# {'15 - BAZA': 800.0}
# {'14 - BAZA': 800.0}
# {'01 - BAZA': 400.0, '03 - BAZA': 400.0}
# {'01 - BAZA': 400.0, '03 - BAZA': 400.0}
# {'14 - BAZA': 200.0}
# {'13 - BAZA': 800.0}
# {'14 - BAZA': 200.0, '11 - BAZA': 200.0, '10 - BAZA': 200.0, '09 - BAZA': 200.0, '11 - TVA': 10.0, '10 - TVA': 18.0, '09 - TVA': 38.0}
# {'14 - BAZA': 200.0, '11 - BAZA': 200.0, '10 - BAZA': 200.0, '09 - BAZA': 200.0, '11 - TVA': 10.0, '10 - TVA': 18.0, '09 - TVA': 38.0}
# # {'14 - BAZA': 200.0}
# BILL/2020/11/0011
# {'26_2 - BAZA': 100.0, '25_2 - BAZA': 100.0, '24_2 - BAZA': 100.0, '26_2 - TVA': 2.5, '25_2 - TVA': 4.5, '24_2 - TVA': 9.5}
# BILL/2020/11/0010
# {'07 - BAZA': 800.0, '07_1 - BAZA': 800.0, '22 - BAZA': 800.0, '22_1 - BAZA': 800.0}
# BILL/2020/11/0005
# {'05 - BAZA': 300.0, '05_1 - BAZA': 300.0, '20 - BAZA': 300.0, '20_1 - BAZA': 300.0, '07 - BAZA': 300.0, '07_1 - BAZA': 300.0, '22 - BAZA': 300.0, '22_1 - BAZA': 300.0, '05 - TVA': -33.0, '05_1 - TVA': -33.0, '20 - TVA': 33.0, '20_1 - TVA': 33.0, '07 - TVA': -33.0, '07_1 - TVA': -33.0, '22 - TVA': 33.0, '22_1 - TVA': 33.0}
# BILL/2020/11/0003
# {'12_3 - BAZA': 200.0, '27_3 - BAZA': 200.0, '12_2 - BAZA': 200.0, '27_2 - BAZA': 200.0, '12_1 - BAZA': 200.0, '27_1 - BAZA': 200.0, '12_3 - TVA': -10.0, '27_3 - TVA': 10.0, '12_2 - TVA': -18.0, '27_2 - TVA': 18.0, '12_1 - TVA': -38.0, '27_1 - TVA': 38.0}
sale_and_purchase_comun_columns = {
    "base_neex": {"type": "int", "tags": ["09 - BAZA", "10 - BAZA", "11 - BAZA"]},  # vat on payment base
    "tva_neex": {"type": "int", "tags": ["09 - TVA", "10 - TVA", "11 - TVA"]},  # vat on payment vat
    "base_exig": {"type": "int", "tags": ["09 - BAZA", "10 - BAZA", "11 - BAZA"]},  # vat on payment = sum of vat
    "tva_exig": {"type": "int", "tags": ["09 - TVA", "10 - TVA", "11 - TVA"]},  # what was payed = sum of base
    # payment must have number,date,amount(value), base, vat
    "base_ded1": {"type": "int", "tags": ["01 - BAZA"]},  # intracomunitar servicii
    "base_ded2": {"type": "int", "tags": ["03 - BAZA"]},  # intracomunitar bunuri
    "base_19": {"type": "int", "tags": ["09 - BAZA"]},
    "base_9": {"type": "int", "tags": ["10 - BAZA"]},
    "base_5": {"type": "int", "tags": ["11 - BAZA"]},
    "base_0": {"type": "int", "tags": ["14 - BAZA"]},
    "tva_19": {"type": "int", "tags": ["09 - TVA"]},
    "tva_9": {"type": "int", "tags": ["10 - TVA"]},
    "tva_5": {"type": "int", "tags": ["11 - TVA"]},
    "tva_bun": {"type": "int", "tags": []},
    "tva_serv": {"type": "int", "tags": []},
    "invers": {"type": "int", "tags": ["13 - BAZA"]},
    "neimp": {"type": "int", "tags": ["30 - BAZA"]},
    "others": {"type": "int", "tags": []},
    "scutit1": {"type": "int", "tags": ["14 - BAZA"]},  # cu drept de deducere
    "scutit2": {"type": "int", "tags": ["15 - BAZA"]},  # fara drept de deducere
    "payments": {"type": "list", "tags": []},
    "base_col": {"type": "int",
                 "tags": ["05 - BAZA", "07 - BAZA", "07_1 - BAZA", "12_1_1 - BAZA", "12_1_1 - BAZA", "12_1_1 - BAZA"]},
    "tva_col": {"type": "int",
                "tags": ["05 - TVA", "07 - TVA", "07_1 - TVA", "12_1_1 - TVA", "12_1_1 - TVA", "12_1_1 - TVA"]},
    "warnings": {"type": "char", "tags": []},
}
sumed_columns = {
    "total_base": ["base_19", "base_9", "base_5", "base_0", "base_exig"],
    "total_vat": ["tva_19", "tva_9", "tva_5", "tva_bun", "tva_serv", "tva_exig"],
}


class SaleJournalReport(models.TransientModel):
    _name = "report.l10n_ro_account_report_journal.report_sale_purchase"
    _description = "Report Sale Purchase Journal"

    @api.model
    def _get_report_values(self, docids, data=None):
        journal_type = data["form"]["journal_type"]
        print(data)
        anaf = self.env["l10n.ro.account.report.journal"].browse(data["form"]["anaf"])
        types = []
        if journal_type == 'sale':
            types = ["out_invoice", "out_refund", "out_receipt"]
        else:
            types = ["in_invoice", "in_refund", "in_receipt"]
        invoices = anaf.get_period_invoices(types)
        invoices += anaf.get_period_vatp_invoices(types)

        if journal_type == 'sale':
            types = ["in_invoice", "in_refund", "in_receipt"]
            supp_tags_name = [
                "07 - BAZA", "07 - TVA", "07_1 - BAZA", "07_1 - TVA",
                "12 - BAZA", "12 - TVA", "12_1 - BAZA", "12_1 - TVA",
                "12_2 - BAZA", "12_2 - TVA", "12_3 - BAZA", "12_3 - TVA",
                "24_2 - BAZA", "24_2 - TVA", "25_2 - BAZA", "25_2 - TVA",
                "26_2 - BAZA", "26_2 - TVA"
            ]
            tags_obj = self.env['account.account.tag']
            tags = self.env['account.account.tag']
            for tag in supp_tags_name:
                tags |= tags_obj._get_tax_tags(
                    tag, anaf.company_id.country_id.id)
            print(tags.ids)
            supp_invoices = anaf.get_period_invoices_by_tags(types, tags.ids)
            invoices |= supp_invoices
        show_warnings = data["form"]["show_warnings"]
        report_type_sale = journal_type == "sale"

        report_lines, totals = self.compute_report_lines(
            anaf, invoices, data, show_warnings, report_type_sale
        )

        docargs = {
            "print_datetime": fields.datetime.now(),
            "date_from": anaf.date_from,
            "date_to": anaf.date_to,
            "show_warnings": show_warnings,
            "user": self.env.user.name,
            "company": anaf.company_id,
            "lines": report_lines,
            "totals": totals,
            "report_type_sale": report_type_sale,
        }
        return docargs

    def get_all_tags(self):
        all_known_tags = {}
        for k, v in sale_and_purchase_comun_columns.items():
            for tag in v["tags"]:
                if tag in all_known_tags.keys():
                    all_known_tags[tag] += [k]
                    warn = (
                        f"tag='{tag}' exist in column={k} but "
                        f"also in column='{all_known_tags[tag]}'"
                    )
                    _logger.warning(warn)
                    # raise ValidationError(warn )
                else:
                    all_known_tags[tag] = [k]
        return all_known_tags

    def get_payment_vals(self, anaf, all_known_tags, vals, sign, invoice):
        # This invoice is vat on payment and we are going to put the payments
        # search the reconcile line
        reconcile_account_move_line_id = False
        for line in invoice.line_ids:
            if line.account_id.code.startswith(
                "411"
            ) or line.account_id.code.startswith("401"):
                reconcile_account_move_line_id = line.id
                break
        # find all the reconciliation till date to
        all_reconcile = self.env['account.move'].search(
            [("tax_cash_basis_move_id", "=", invoice.id),
             ("date", "<=", anaf.date_to),
            ]
        )
        all_reconcile_ids = [x.id for x in all_reconcile]

        for move in all_reconcile_ids:
            if move.date < anaf.date_from:
                # this payment is in a period before and we will just substract it
                for move_line in move.line_ids:
                    for tag in move_line.tax_tag_ids:
                        if (
                            tag.name
                            in sale_and_purchase_comun_columns["base_neex"][
                            "tags"
                        ]
                        ):
                            vals["base_neex"] -= sign * (
                                move_line.credit - move_line.debit
                            )
                        elif (
                            tag.name
                            in sale_and_purchase_comun_columns["tva_neex"][
                                "tags"
                            ]
                        ):
                            vals["tva_neex"] -= sign * (
                                move_line.credit - move_line.debit
                            )
            else:
                # is payment in period and we are going also to show it, and also substract it
                vals["rowspan"] += 1
                vals["payments"] += [
                    {
                        "number": move.ref,
                        "date": move.date,
                        "amount": move.amount_total,
                        "base_exig": 0,
                        "tva_exig": 0,
                    }
                ]
                for move_line in move.line_ids:
                    if "TVA" in "".join(
                        [x.name for x in move_line.tax_tag_ids]
                    ):
                        vals["payments"][-1]["tva_exig"] += sign * (
                            move_line.credit - move_line.debit
                        )
                    elif "BAZA" in "".join(
                        [x.name for x in move_line.tax_tag_ids]
                    ):
                        vals["payments"][-1]["base_exig"] += sign * (
                            move_line.credit - move_line.debit
                        )
                    for tag in move_line.tax_tag_ids:
                        if tag.name in all_known_tags.keys():
                            for tagx in all_known_tags[tag.name]:
                                if tagx in ["base_neex", "tva_neex"]:
                                    vals[tagx] -= sign * (
                                        move_line.credit - move_line.debit
                                    )  # we substract neexigible because is exigible
                                else:
                                    vals[tagx] += sign * (
                                        move_line.credit - move_line.debit
                                    )
        return vals

    def add_new_row(self):
        empty_row = {k: 0.0 for k in sumed_columns}
        empty_row.update(
            {
                k: 0.0
                for k, v in sale_and_purchase_comun_columns.items()
                if v["type"] == "int"
            }
        )
        empty_row.update(
            {
                k: ""
                for k, v in sale_and_purchase_comun_columns.items()
                if v["type"] == "char"
            }
        )
        empty_row.update(
            {
                k: []
                for k, v in sale_and_purchase_comun_columns.items()
                if v["type"] == "list"
            }
        )
        return empty_row


    def compute_report_lines(
        self, anaf, invoices, data, show_warnings=False, report_type_sale=True
    ):
        """input:
        invoices = account.move list of invoices to be showed in report
        payments = account.move list of payments done on vat_on_payment invoices
        vat_on_payment_reconcile = partial.reconcile  list of efective accounting
                                   moves that are telling what taxes are to be paid
        data = dictionary with selected options like date_from, date_to, company...

        returns a list of a dictionary for table with the key as column
        and total dictionary with the sums of columns """

        if not invoices:
            return [], {}
        # must be int
        all_known_tags = self.get_all_tags()
        empty_row = self.add_new_row()

        sign = 1 if report_type_sale else -1
        sign = 1
        report_lines = []
        vatp_tags = ["tva_neex", "base_exig", "base_neex", "tva_exig"]
        for inv1 in invoices:
            new_sign = sign
            if report_type_sale and inv1.move_type in ["in_invoice", "in_refund", "in_receipt"]:
                new_sign = -1 * sign
            checked_tags = vatp_tags
            if inv1.partner_id.country_id == self.env.ref("base.ro"):
                checked_tags += [
                    "tva_bun", "tva_serv", "invers", "neimp", "others", "scutit1" "scutit2"]
            vals = deepcopy(empty_row)
            vals["number"] = inv1.name
            vals["date"] = inv1.invoice_date
            vals["partner"] = inv1.commercial_partner_id.name
            vals["vat"] = inv1.invoice_partner_display_vat
            vals["total"] = new_sign * (inv1.amount_total_signed)
            vals["warnings"] = ""
            vals["rowspan"] = 1

            put_payments = False
            # after parsing the invoice lines, if is vat on payment,
            # to put also the payments take all the lines from this
            # invoice and put them into dictionary
            res = anaf.with_context(move_id=inv1.id)._get_vat_report_data(
                anaf.company_id.id, anaf.date_from, anaf.date_to)
            print(inv1.name)
            print(res)
            non_ded_base = ["24_2 - BAZA", "25_2 - BAZA", "26_2 - BAZA"]
            if res:
                for _key, value in res.items():
                    if _key in all_known_tags.keys():
                        for tagx in all_known_tags[_key]:
                            if tagx not in checked_tags:
                                if tagx in non_ded_base:
                                    value = 0.5 * value
                                vals[tagx] += value

            for line in inv1.line_ids:
                if not line.tax_exigible:  # VAT on payment
                    put_payments = True
                    for tag in line.tax_tag_ids:
                        # adding the base and vat from original invoice
                        if (
                            tag.name
                            in sale_and_purchase_comun_columns["base_neex"]["tags"]
                        ):
                            vals["base_neex"] += sign * (line.credit - line.debit)
                            unknown_line = False
                        elif (
                            tag.name
                            in sale_and_purchase_comun_columns["tva_neex"]["tags"]
                        ):
                            vals["tva_neex"] += sign * (line.credit - line.debit)
                            unknown_line = False

            if put_payments:
                vals = self.get_payment_vals(anaf, all_known_tags, vals, sign, inv1)

            if vals["rowspan"] > 1:
                vals["rowspan"] -= 1

            vals["base_neex"], vals["tva_neex"] = (
                round(vals["base_neex"], 2),
                round(vals["tva_neex"], 2),
            )

            for key, value in sumed_columns.items():
                # put the aggregated values ( summed columns)
                vals[key] = sum([vals[x] for x in value])

            report_lines += [vals]  # we added another line to the table

        # make the totals dictionary for total line of table as sum of all the integer/float values of vals
        int_float_keys = []
        for key, value in report_lines[0].items():
            if (type(value) is int) or (type(value) is float):
                int_float_keys.append(key)
        totals = {}
        for key in int_float_keys:
            totals[key] = round(sum([x[key] for x in report_lines]), 2)
        totals["payments"] = []

        return report_lines, totals
