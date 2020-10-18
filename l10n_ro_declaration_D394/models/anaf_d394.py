# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AnafD394(models.Model):
    _name = "anaf.d394"
    _inherit = "anaf.mixin"
    _description = "Anaf Declaration D394"

    anaf_cross_opt = fields.Boolean(
        "ANAF Crosschecking", related="company_id.anaf_cross_opt"
    )
    anaf_cross_new_opt = fields.Boolean("Allow ANAF Crosschecking")
    solicit = fields.Boolean("Request VAT Reimbursment")
    achizitiiPE = fields.Boolean(
        "Purchases of Eolian Parks",
        help="Achizitii de bunuri si servicii legate direct de"
        " bunurile imobile: Parcuri Eoliene",
    )
    achizitiiCR = fields.Boolean(
        "Purchases of Residential Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
        " bunurile imobile: constructii rezidentiale",
    )
    achizitiiCB = fields.Boolean(
        "Purchases of Office Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
        " bunurile imobile: cladiri de birouri",
    )
    achizitiiCI = fields.Boolean(
        "Purchases of Industrial Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
        " bunurile imobile: constructii industriale",
    )
    achizitiiA = fields.Boolean(
        "Purchases of Real Estates: Others",
        help="Achizitii de bunuri si servicii legate direct de"
        " bunurile imobile: altele",
    )
    achizitiiB24 = fields.Boolean(
        "Purchased Goods with 24% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 24%",
    )
    achizitiiB20 = fields.Boolean(
        "Purchased Goods with 20% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 20%",
    )
    achizitiiB19 = fields.Boolean(
        "Purchased Goods with 19% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 19%",
    )
    achizitiiB9 = fields.Boolean(
        "Purchased Goods with 9% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 9%",
    )
    achizitiiB5 = fields.Boolean(
        "Purchased Goods with 5% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 5%",
    )
    achizitiiS24 = fields.Boolean(
        "Purchased Services with 24% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 24%",
    )
    achizitiiS20 = fields.Boolean(
        "Purchased Services with 20% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 20%",
    )
    achizitiiS19 = fields.Boolean(
        "Purchased Services with 19% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 19%",
    )
    achizitiiS9 = fields.Boolean(
        "Purchased Services with 9% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 9%",
    )
    achizitiiS5 = fields.Boolean(
        "Purchased Services with 5% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
        " de bunuri imobile cu cota 5%",
    )
    importB = fields.Boolean("Purchase Goods - Imports", help="Importuri de bunuri")
    acINecorp = fields.Boolean(
        "Purchase of Intangible Assets", help="Achizitii imobilizari necorporale"
    )
    livrariBI = fields.Boolean(
        "Sales from Real Estates", help="Livrari de bunuri imobile"
    )
    BUN24 = fields.Boolean(
        "Sales Goods with 24% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor" " imobile cu cota de 24%",
    )
    BUN20 = fields.Boolean(
        "Sales Goods with 20% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor" " imobile cu cota de 20%",
    )
    BUN19 = fields.Boolean(
        "Sales Goods with 19% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor" " imobile cu cota de 19%",
    )
    BUN9 = fields.Boolean(
        "Sales Goods with 9% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor" " imobile cu cota de 9%",
    )
    BUN5 = fields.Boolean(
        "Sales Goods with 5% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor" " imobile cu cota de 5%",
    )
    valoareScutit = fields.Boolean(
        "Sales Goods exempt from VAT", help="Livrari de bunuri scutite de TVA"
    )
    BunTI = fields.Boolean(
        "Sales Goods with Inverse Taxation",
        help="Livrari de bunuri/prestari de servicii pt care"
        " se aplica taxarea inversa",
    )
    Prest24 = fields.Boolean(
        "Sales Services with 24% VAT", help="Prestari de servicii cu cota de 24%"
    )
    Prest20 = fields.Boolean(
        "Sales Services with 20% VAT", help="Prestari de servicii cu cota de 20%"
    )
    Prest19 = fields.Boolean(
        "Sales Services with 19% VAT", help="Prestari de servicii cu cota de 19%"
    )
    Prest9 = fields.Boolean(
        "Sales Services with 9% VAT", help="Prestari de servicii cu cota de 9%"
    )
    Prest5 = fields.Boolean(
        "Sales Services with 5% VAT", help="Prestari de servicii cu cota de 5%"
    )
    PrestScutit = fields.Boolean(
        "Sales Services exempt from VAT", help="Prestari de servicii scutite de TVA"
    )
    LIntra = fields.Boolean(
        "Sales Goods - Intra-Community", help="Livrari intracomunitare de bunuri"
    )
    PrestIntra = fields.Boolean(
        "Sales Services - Intra-Community", help="Prestari intracomunitare de servicii"
    )
    Export = fields.Boolean("Sales Goods - Exports", help="Exporturi de bunuri")
    livINecorp = fields.Boolean(
        "Sales of Intangible Assets", help="Livrari imobilizari necorporale"
    )

    # InformatiiType
    # Rezumat1Type
    # DetaliuType
    # Rezumat2Type
    # SerieFacturiType
    # ListaType
    # FacturiType
    # Op1Type
    # Op11Type
    # Op2Type

    @api.model
    def get_tip_D394(self):
        months = self.get_months_number()
        if months == 3:
            tip_D394 = "T"
        elif months == 6:
            tip_D394 = "S"
        elif months == 12:
            tip_D394 = "A"
        else:
            tip_D394 = "L"
        return tip_D394

    def build_file(self):
        self.generate_op1()
        self.generate_op2()
        self.generate_series()
        self.generate_invoice()
        self.generate_list()
        self.compute_totals()
        return super(AnafD394, self).build_file()

    def generate_op1(self):
        move_obj = self.env["account.move"]
        domain = [
            (
                "move_type",
                "in",
                ["in_invoice", "in_refund", "out_invoice", "out_refund"],
            ),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to)("state", "=", "posted"),
            ("company_id", "=", self.company_id.id),
        ]
        invoices = move_obj.search(domain)
        op1 = self.env["account.move.line"].read_group(
            [("move_id", "in", invoices.ids)],
            [
                "move_id.operation_type",
                "move_id.partner_type",
                "move_id.commercial_partner_id",
                "tax_group_id",
                "tax_base_amount",
                "balance",
            ],
            ["journal_id"],
            lazy=False,
        )
