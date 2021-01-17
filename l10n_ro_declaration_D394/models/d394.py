# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ANAFD394(models.TransientModel):
    _name = "anaf.d394"
    _inherit = "anaf.mixin"
    _description = "Declaratie 394"

    @api.model
    def _get_default_declaration(self):
        d394 = self.env["anaf.declaration"].search(
            [("name", "=", "d394")], limit=1)
        if d394:
            return d394
        return super(ANAFD394, self)._get_default_declaration()

    declaration_id = fields.Many2one(default=_get_default_declaration)

    #anaf_cross_opt = fields.Boolean("ANAF Crosschecking",
    #                                related="company_id.anaf_cross_opt")
    #anaf_cross_new_opt = fields.Boolean("Allow ANAF Crosschecking")
    solicit = fields.Boolean("Request VAT Reimbursment")
    achizitiiPE = fields.Boolean(
        "Purchases of Eolian Parks",
        help="Achizitii de bunuri si servicii legate direct de"
             " bunurile imobile: Parcuri Eoliene",
        compute="compute_vat_return"
    )
    achizitiiCR = fields.Boolean(
        "Purchases of Residential Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
             " bunurile imobile: constructii rezidentiale",
        compute="compute_vat_return"
    )
    achizitiiCB = fields.Boolean(
        "Purchases of Office Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
             " bunurile imobile: cladiri de birouri",
        compute="compute_vat_return"
    )
    achizitiiCI = fields.Boolean(
        "Purchases of Industrial Buildings",
        help="Achizitii de bunuri si servicii legate direct de"
             " bunurile imobile: constructii industriale",
        compute="compute_vat_return"
    )
    achizitiiA = fields.Boolean(
        "Purchases of Real Estates: Others",
        help="Achizitii de bunuri si servicii legate direct de"
             " bunurile imobile: altele",
        compute="compute_vat_return"
    )
    achizitiiB24 = fields.Boolean(
        "Purchased Goods with 24% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 24%",
        compute="compute_vat_return"
    )
    achizitiiB20 = fields.Boolean(
        "Purchased Goods with 20% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 20%",
        compute="compute_vat_return"
    )
    achizitiiB19 = fields.Boolean(
        "Purchased Goods with 19% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 19%",
        compute="compute_vat_return"
    )
    achizitiiB9 = fields.Boolean(
        "Purchased Goods with 9% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 9%",
        compute="compute_vat_return"
    )
    achizitiiB5 = fields.Boolean(
        "Purchased Goods with 5% VAT",
        help="Achizitii de bunuri, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 5%",
        compute="compute_vat_return"
    )
    achizitiiS24 = fields.Boolean(
        "Purchased Services with 24% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 24%",
        compute="compute_vat_return"
    )
    achizitiiS20 = fields.Boolean(
        "Purchased Services with 20% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 20%",
        compute="compute_vat_return"
    )
    achizitiiS19 = fields.Boolean(
        "Purchased Services with 19% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 19%",
        compute="compute_vat_return"
    )
    achizitiiS9 = fields.Boolean(
        "Purchased Services with 9% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 9%",
        compute="compute_vat_return"
    )
    achizitiiS5 = fields.Boolean(
        "Purchased Services with 5% VAT",
        help="Achizitii de servicii, cu exceptia celor legate direct"
             " de bunuri imobile cu cota 5%",
        compute="compute_vat_return"
    )
    importB = fields.Boolean(
        "Purchase Goods - Imports",
        help="Importuri de bunuri",
        compute="compute_vat_return"
    )
    acINecorp = fields.Boolean(
        "Purchase of Intangible Assets",
        help="Achizitii imobilizari necorporale",
        compute="compute_vat_return"
    )
    livrariBI = fields.Boolean(
        "Sales from Real Estates",
        help="Livrari de bunuri imobile",
        compute="compute_vat_return"
    )
    BUN24 = fields.Boolean(
        "Sales Goods with 24% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor"
             " imobile cu cota de 24%",
        compute="compute_vat_return"
    )
    BUN20 = fields.Boolean(
        "Sales Goods with 20% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor"
             " imobile cu cota de 20%",
        compute="compute_vat_return"
    )
    BUN19 = fields.Boolean(
        "Sales Goods with 19% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor"
             " imobile cu cota de 19%",
        compute="compute_vat_return"
    )
    BUN9 = fields.Boolean(
        "Sales Goods with 9% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor"
             " imobile cu cota de 9%",
        compute="compute_vat_return"
    )
    BUN5 = fields.Boolean(
        "Sales Goods with 5% VAT",
        help="Livrari de bunuri, cu exceptia bunurilor"
             " imobile cu cota de 5%",
        compute="compute_vat_return"
    )
    valoareScutit = fields.Boolean(
        "Sales Goods exempt from VAT",
        help="Livrari de bunuri scutite de TVA",
        compute="compute_vat_return"
    )
    BunTI = fields.Boolean(
        "Sales Goods with Inverse Taxation",
        help="Livrari de bunuri/prestari de servicii pt care"
             " se aplica taxarea inversa",
        compute="compute_vat_return"
    )
    Prest24 = fields.Boolean(
        "Sales Services with 24% VAT",
        help="Prestari de servicii cu cota de 24%",
        compute="compute_vat_return"
    )
    Prest20 = fields.Boolean(
        "Sales Services with 20% VAT",
        help="Prestari de servicii cu cota de 20%",
        compute="compute_vat_return"
    )
    Prest19 = fields.Boolean(
        "Sales Services with 19% VAT",
        help="Prestari de servicii cu cota de 19%",
        compute="compute_vat_return"
    )
    Prest9 = fields.Boolean(
        "Sales Services with 9% VAT",
        help="Prestari de servicii cu cota de 9%",
        compute="compute_vat_return"
    )
    Prest5 = fields.Boolean(
        "Sales Services with 5% VAT",
        help="Prestari de servicii cu cota de 5%",
        compute="compute_vat_return"
    )
    PrestScutit = fields.Boolean(
        "Sales Services exempt from VAT",
        help="Prestari de servicii scutite de TVA",
        compute="compute_vat_return"
    )
    LIntra = fields.Boolean(
        "Sales Goods - Intra-Community",
        help="Livrari intracomunitare de bunuri",
        compute="compute_vat_return"
    )
    PrestIntra = fields.Boolean(
        "Sales Services - Intra-Community",
        help="Prestari intracomunitare de servicii",
        compute="compute_vat_return"
    )
    Export = fields.Boolean(
        "Sales Goods - Exports",
        help="Exporturi de bunuri",
        compute="compute_vat_return"
    )
    livINecorp = fields.Boolean(
        "Sales of Intangible Assets",
        help="Livrari imobilizari necorporale",
        compute="compute_vat_return"
    )
