# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SalePurchaseJournalReport(models.TransientModel):
    _name = "l10n.ro.account.report.journal"
    _inherit = "anaf.mixin"
    _description = "Sale Purchase Journal Report"

    journal_type = fields.Selection(
        selection=[
            ("purchase", "Purchase = In invoices"),
            ("sale", "Sale = Out invoices"),
        ],
        string="Journal type",
        default="sale",
        required=True,
    )
    show_warnings = fields.Boolean(
        "Show Warnings",
        default=1,
        help="If you check this, you will have another column that is going "
        "to show you errors/warnings if exist",
    )

    def print_report_html(self):
        res = self.print_report(html=True)
        return res

    def print_report(self, html=False):
        self.ensure_one()
        [data] = self.read()
        datas = {"ids": [], "model": "l10n_ro_account_report_journal", "form": data}
        report_action = "l10n_ro_account_report_journal.action_report_sale" + (
            "_html" if html else ""
        )
        datas["form"]["anaf"] = self.id
        ref = self.env.ref(report_action)
        res = ref.report_action(docids=[], data=datas, config=False)
        return res
