# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Mon Jan 18 16:52:08 2021 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Cos(models.AbstractModel):
    _description = "cos"
    _name = "d390.3.cos"
    _inherit = "spec.mixin.d390"
    _generateds_type = "CosType"
    _concrete_rec_name = "d3903_tip"

    d3903_cos_Declaratie390_id = fields.Many2one("d390.3.declaratie390")
    d3903_tip = fields.Char(string="tip", xsd_required=True, xsd_type="string")
    d3903_tara_m1 = fields.Char(string="tara_m1", xsd_required=True, xsd_type="string")
    d3903_cod_m1 = fields.Char(string="cod_m1", xsd_required=True, xsd_type="string")
    d3903_motiv = fields.Integer(string="motiv", xsd_type="integer")
    d3903_tara_m2 = fields.Char(string="tara_m2", xsd_type="string")
    d3903_cod_m2 = fields.Char(string="cod_m2", xsd_type="string")


class Declaratie390(models.AbstractModel):
    _description = "declaratie390"
    _name = "d390.3.declaratie390"
    _inherit = "spec.mixin.d390"
    _generateds_type = "Declaratie390Type"
    _concrete_rec_name = "d3903_luna"

    d3903_luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    d3903_an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    d3903_d_rec = fields.Integer(string="d_rec", xsd_required=True, xsd_type="integer")
    d3903_nume_declar = fields.Char(
        string="nume_declar", xsd_required=True, xsd_type="string"
    )
    d3903_prenume_declar = fields.Char(
        string="prenume_declar", xsd_required=True, xsd_type="string"
    )
    d3903_functie_declar = fields.Char(
        string="functie_declar", xsd_required=True, xsd_type="string"
    )
    d3903_cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    d3903_den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    d3903_adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    d3903_telefon = fields.Char(string="telefon", xsd_type="string")
    d3903_fax = fields.Char(string="fax", xsd_type="string")
    d3903_mail = fields.Char(string="mail", xsd_type="token")
    d3903_totalPlata_A = fields.Integer(
        string="totalPlata_A", xsd_required=True, xsd_type="integer"
    )
    d3903_rezumat = fields.Many2one(
        "d390.3.rezumat", string="rezumat", xsd_required=True
    )
    d3903_cos = fields.One2many(
        "d390.3.cos", "d3903_cos_Declaratie390_id", string="cos", xsd_required=True
    )
    d3903_operatie = fields.One2many(
        "d390.3.operatie",
        "d3903_operatie_Declaratie390_id",
        string="operatie",
        xsd_required=True,
    )


class Operatie(models.AbstractModel):
    _description = "operatie"
    _name = "d390.3.operatie"
    _inherit = "spec.mixin.d390"
    _generateds_type = "OperatieType"
    _concrete_rec_name = "d3903_tip"

    d3903_operatie_Declaratie390_id = fields.Many2one("d390.3.declaratie390")
    d3903_tip = fields.Char(string="tip", xsd_required=True, xsd_type="string")
    d3903_tara = fields.Char(string="tara", xsd_required=True, xsd_type="string")
    d3903_codO = fields.Char(string="codO", xsd_type="string")
    d3903_denO = fields.Char(string="denO", xsd_required=True, xsd_type="string")
    d3903_baza = fields.Integer(string="baza", xsd_required=True, xsd_type="integer")


class Rezumat(models.AbstractModel):
    _description = "rezumat"
    _name = "d390.3.rezumat"
    _inherit = "spec.mixin.d390"
    _generateds_type = "RezumatType"
    _concrete_rec_name = "d3903_nr_pag"

    d3903_nr_pag = fields.Integer(
        string="nr_pag", xsd_required=True, xsd_type="integer"
    )
    d3903_nrOPI = fields.Integer(string="nrOPI", xsd_required=True, xsd_type="integer")
    d3903_bazaL = fields.Integer(string="bazaL", xsd_required=True, xsd_type="integer")
    d3903_bazaT = fields.Integer(string="bazaT", xsd_required=True, xsd_type="integer")
    d3903_bazaA = fields.Integer(string="bazaA", xsd_required=True, xsd_type="integer")
    d3903_bazaP = fields.Integer(string="bazaP", xsd_required=True, xsd_type="integer")
    d3903_bazaS = fields.Integer(string="bazaS", xsd_required=True, xsd_type="integer")
    d3903_bazaR = fields.Integer(string="bazaR", xsd_required=True, xsd_type="integer")
    d3903_total_baza = fields.Integer(
        string="total_baza", xsd_required=True, xsd_type="integer"
    )
