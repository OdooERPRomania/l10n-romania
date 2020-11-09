# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RunDeclaration(models.TransientModel):
    _name = "anaf.d394"
    _inherit = "anaf.mixin"
    _description = "Declaratie 394"

    intocmit_id = fields.Many2one(
        "res.partner",
        string="Intocmit",
    )
    optiune = fields.Boolean(string="optiune")
    schimb_optiune = fields.Boolean(string="schimb_optiune")
    prsAfiliat = fields.Boolean(string="prsAfiliat")

    solicit = fields.Boolean(string="solicit")
    achizitiiPE = fields.Integer(
        string="achizitiiPE",
        compute="_compute_solicit_amounts")
    achizitiiCR = fields.Integer(
        string="achizitiiCR",
        compute="_compute_solicit_amounts")
    achizitiiCB = fields.Integer(
        string="achizitiiCB",
        compute="_compute_solicit_amounts")
    achizitiiCI = fields.Integer(
        string="achizitiiCI",
        compute="_compute_solicit_amounts")
    achizitiiA = fields.Integer(
        string="achizitiiA",
        compute="_compute_solicit_amounts")
    achizitiiB24 = fields.Integer(
        string="achizitiiB24",
        compute="_compute_solicit_amounts")
    achizitiiB20 = fields.Integer(
        string="achizitiiB20",
        compute="_compute_solicit_amounts")
    achizitiiB19 = fields.Integer(
        string="achizitiiB19",
        compute="_compute_solicit_amounts")
    achizitiiB9 = fields.Integer(
        string="achizitiiB9",
        compute="_compute_solicit_amounts")
    achizitiiB5 = fields.Integer(
        string="achizitiiB5",
        compute="_compute_solicit_amounts")
    achizitiiS24 = fields.Integer(
        string="achizitiiS24",
        compute="_compute_solicit_amounts")
    achizitiiS20 = fields.Integer(
        string="achizitiiS20",
        compute="_compute_solicit_amounts")
    achizitiiS19 = fields.Integer(
        string="achizitiiS19",
        compute="_compute_solicit_amounts")
    achizitiiS9 = fields.Integer(
        string="achizitiiS9",
        compute="_compute_solicit_amounts")
    achizitiiS5 = fields.Integer(
        string="achizitiiS5",
        compute="_compute_solicit_amounts")
    importB = fields.Integer(
        string="importB",
        compute="_compute_solicit_amounts")
    acINecorp = fields.Integer(
        string="acINecorp",
        compute="_compute_solicit_amounts")
    livrariBI = fields.Integer(
        string="livrariBI",
        compute="_compute_solicit_amounts")
    BUN24 = fields.Integer(
        string="BUN24",
        compute="_compute_solicit_amounts")
    BUN20 = fields.Integer(
        string="BUN20",
        compute="_compute_solicit_amounts")
    BUN19 = fields.Integer(
        string="BUN19",
        compute="_compute_solicit_amounts")
    BUN9 = fields.Integer(
        string="BUN9",
        compute="_compute_solicit_amounts")
    BUN5 = fields.Integer(
        string="BUN5",
        compute="_compute_solicit_amounts")
    valoareScutit = fields.Integer(
        string="valoareScutit",
        compute="_compute_solicit_amounts")
    BunTI = fields.Integer(
        string="BunTI",
        compute="_compute_solicit_amounts")
    Prest24 = fields.Integer(
        string="Prest24",
        compute="_compute_solicit_amounts")
    Prest20 = fields.Integer(
        string="Prest20",
        compute="_compute_solicit_amounts")
    Prest19 = fields.Integer(
        string="Prest19",
        compute="_compute_solicit_amounts")
    Prest9 = fields.Integer(
        string="Prest9",
        compute="_compute_solicit_amounts")
    Prest5 = fields.Integer(
        string="Prest5",
        compute="_compute_solicit_amounts")
    PrestScutit = fields.Integer(
        string="PrestScutit",
        compute="_compute_solicit_amounts")
    LIntra = fields.Integer(
        string="LIntra",
        compute="_compute_solicit_amounts")
    PrestIntra = fields.Integer(
        string="PrestIntra",
        compute="_compute_solicit_amounts")
    Export = fields.Integer(
        string="Export",
        compute="_compute_solicit_amounts")
    livINecorp = fields.Integer(
        string="livINecorp",
        compute="_compute_solicit_amounts")
    efectuat = fields.Integer(
        string="efectuat",
        compute="_compute_solicit_amounts")
