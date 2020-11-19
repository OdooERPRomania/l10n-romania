# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from copy import deepcopy

from odoo import api, fields, models

from .column_config import JOURNAL_COLUMNS, SUMED_COLUMNS

_logger = logging.getLogger(__name__)


class SaleJournalReport(models.TransientModel):
    _name = "report.l10n_ro_account_report_journal.report_sale_purchase"
    _description = "Report Sale Purchase Journal"

    @api.model
    def _get_report_values(self, docids, data=None):
        journal_type = data["form"]["journal_type"]
        anaf = self.env["l10n.ro.account.report.journal"].browse(data["form"]["anaf"])
        types = []
        if journal_type == "sale":
            types = ["out_invoice", "out_refund", "out_receipt"]
        else:
            types = ["in_invoice", "in_refund", "in_receipt"]
        invoices = anaf.get_period_invoices(types)
        invoices += anaf.get_period_vatp_invoices(types)

        if journal_type == "sale":
            types = ["in_invoice", "in_refund", "in_receipt"]
            supp_tags_name = [
                "05 - BAZA",
                "05 - TVA",
                "07 - BAZA",
                "07 - TVA",
                "12_1 - BAZA",
                "12_1 - TVA",
                "12_2 - BAZA",
                "12_2 - TVA",
                "12_3 - BAZA",
                "12_3 - TVA",
            ]
            tags_obj = self.env["account.account.tag"]
            tags = self.env["account.account.tag"]
            for tag in supp_tags_name:
                tags |= tags_obj._get_tax_tags(tag, anaf.company_id.country_id.id)
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
        for k, v in JOURNAL_COLUMNS.items():
            for tag in v["tags"]:
                if tag in all_known_tags.keys():
                    all_known_tags[tag] += [k]
                else:
                    all_known_tags[tag] = [k]
        return all_known_tags

    def get_vatp_not_eligible(self, line, vals):
        nd_tax_base = JOURNAL_COLUMNS["base_neex"]["tags"]
        nd_tax_vat = JOURNAL_COLUMNS["tva_neex"]["tags"]
        for tag in line.tax_tag_ids:
            type_multiplicator = line.journal_id.type == "sale" and -1 or 1
            tag_amount = type_multiplicator * line.balance
            if tag.tax_report_line_ids:
                # Then, the tag comes from a report line, and hence has a + or - sign (also in its name)
                for report_line in tag.tax_report_line_ids:
                    tag_id = report_line.tag_name
                    if tag_id in nd_tax_base:
                        vals["base_neex"] += tag_amount
                    elif tag_id in nd_tax_vat:
                        vals["tva_neex"] += tag_amount
            else:
                # Then, it's a financial tag (sign is always +, and never shown in tag name)
                tag_id = tag.name
                if tag_id in nd_tax_base:
                    vals["base_neex"] += tag_amount
                elif tag_id in nd_tax_vat:
                    vals["tva_neex"] += tag_amount
        return vals

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
        all_reconcile = self.env["account.move"].search(
            [
                ("tax_cash_basis_move_id", "=", invoice.id),
                ("date", "<=", anaf.date_to),
            ]
        )
        for move in all_reconcile:
            if move.date < anaf.date_to:
                for move_line in move.line_ids:
                    vals = self.get_vatp_not_eligible(move_line, vals)
            if move.date >= anaf.date_from and anaf.date_to:
                # is payment in period and we are going also to show it, and also substract it
                vals["rowspan"] += 1
                payment = {
                    "number": move.ref,
                    "date": move.date,
                    "amount": move.amount_total,
                    "base_19": 0,
                    "base_9": 0,
                    "base_5": 0,
                    "tva_19": 0,
                    "tva_9": 0,
                    "tva_5": 0,
                }
                res = anaf.with_context(move_id=move.id)._get_vat_report_data(
                    anaf.company_id.id, anaf.date_from, anaf.date_to
                )
                if res:
                    for _key, value in res.items():
                        if _key in all_known_tags.keys():
                            for tagx in all_known_tags[_key]:
                                new_sign = sign
                                if "tva" in tagx:
                                    new_sign = -1 * new_sign
                                if tagx in payment:
                                    payment[tagx] += new_sign * value
                vals["payments"].append(payment)
        return vals

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
        and total dictionary with the sums of columns"""

        if not invoices:
            return [], {}
        # must be int
        all_known_tags = self.get_all_tags()
        print(all_known_tags)
        empty_row = self.add_new_row()

        sign = 1 if report_type_sale else -1
        sign = 1
        report_lines = []
        vatp_tags = ["tva_neex", "base_exig", "base_neex", "tva_exig"]
        for inv1 in invoices:
            (
                country_code,
                identifier_type,
                vat_number,
            ) = inv1.commercial_partner_id._parse_anaf_vat_info()
            new_sign = sign
            if report_type_sale and inv1.move_type in [
                "in_invoice",
                "in_refund",
                "in_receipt",
            ]:
                new_sign = -1 * sign
            checked_tags = vatp_tags
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
                anaf.company_id.id, anaf.date_from, anaf.date_to
            )
            if inv1.name == "INV/2020/11/0003":
                print(res)
            if res:
                for _key, value in res.items():
                    if _key in all_known_tags.keys():
                        for tagx in all_known_tags[_key]:
                            vals[tagx] += value
            if inv1.name == "INV/2020/11/0003":
                print(vals)
            for line in inv1.line_ids:
                if line.tax_tag_ids and not line.tax_exigible:  # VAT on payment
                    put_payments = True
                    vals = self.get_vatp_not_eligible(line, vals)

            if put_payments:
                vals = self.get_payment_vals(anaf, all_known_tags, vals, new_sign, inv1)

            if vals["rowspan"] > 1:
                vals["rowspan"] -= 1

            if put_payments and vals.get("payments"):
                for pay in vals.get("payments"):
                    for _key, value in SUMED_COLUMNS.items():
                        for tag in value:
                            vals[tag] += pay.get(tag, 0)
                    pay["base_exig"] = pay["base_19"] + pay["base_9"] + pay["base_5"]
                    pay["tva_exig"] = pay["tva_19"] + pay["tva_9"] + pay["tva_5"]
            for _key, value in SUMED_COLUMNS.items():
                # put the aggregated values ( summed columns)
                vals[_key] = sum([vals[x] for x in value])
            if identifier_type == "1":
                vals["scutit1"] = 0.0
            else:
                vals["base_0"] = 0.0
            if inv1.name == "INV/2020/11/0003":
                print(vals)
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

    def add_new_row(self):
        empty_row = {k: 0.0 for k in SUMED_COLUMNS}
        empty_row.update(
            {k: 0.0 for k, v in JOURNAL_COLUMNS.items() if v["type"] == "int"}
        )
        empty_row.update(
            {k: "" for k, v in JOURNAL_COLUMNS.items() if v["type"] == "char"}
        )
        empty_row.update(
            {k: [] for k, v in JOURNAL_COLUMNS.items() if v["type"] == "list"}
        )
        return empty_row
