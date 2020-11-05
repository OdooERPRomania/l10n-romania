# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Sat Oct 31 17:10:31 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Declaratie300(models.AbstractModel):
    _description = "declaratie300"
    _name = "D300.00.declaratie300"
    _inherit = "spec.mixin.D300"
    _generateds_type = "Declaratie300Type"
    _concrete_rec_name = "D30000_luna"

    D30000_luna = fields.Integer(string="luna", xsd_required=True, xsd_type="integer")
    D30000_an = fields.Integer(string="an", xsd_required=True, xsd_type="integer")
    D30000_bifa_interne = fields.Integer(
        string="bifa_interne", xsd_required=True, xsd_type="integer"
    )
    D30000_temei = fields.Integer(string="temei", xsd_required=True, xsd_type="integer")
    D30000_nume_declar = fields.Char(
        string="nume_declar", xsd_required=True, xsd_type="string"
    )
    D30000_prenume_declar = fields.Char(
        string="prenume_declar", xsd_required=True, xsd_type="string"
    )
    D30000_functie_declar = fields.Char(
        string="functie_declar", xsd_required=True, xsd_type="string"
    )
    D30000_cui = fields.Char(string="cui", xsd_required=True, xsd_type="token")
    D30000_den = fields.Char(string="den", xsd_required=True, xsd_type="string")
    D30000_adresa = fields.Char(string="adresa", xsd_required=True, xsd_type="string")
    D30000_telefon = fields.Char(string="telefon", xsd_type="string")
    D30000_fax = fields.Char(string="fax", xsd_type="string")
    D30000_mail = fields.Char(string="mail", xsd_type="token")
    D30000_banca = fields.Char(string="banca", xsd_required=True, xsd_type="string")
    D30000_cont = fields.Char(string="cont", xsd_required=True, xsd_type="string")
    D30000_caen = fields.Char(string="caen", xsd_required=True, xsd_type="string")
    D30000_tip_decont = fields.Char(
        string="tip_decont", xsd_required=True, xsd_type="string"
    )
    D30000_pro_rata = fields.Float(
        string="pro_rata", xsd_required=True, xsd_type="double"
    )
    D30000_bifa_cereale = fields.Char(
        string="bifa_cereale", xsd_required=True, xsd_type="string"
    )
    D30000_bifa_mob = fields.Char(
        string="bifa_mob", xsd_required=True, xsd_type="string"
    )
    D30000_bifa_disp = fields.Char(
        string="bifa_disp", xsd_required=True, xsd_type="string"
    )
    D30000_bifa_cons = fields.Char(
        string="bifa_cons", xsd_required=True, xsd_type="string"
    )
    D30000_solicit_ramb = fields.Char(
        string="solicit_ramb", xsd_required=True, xsd_type="string"
    )
    D30000_nr_evid = fields.Integer(
        string="nr_evid", xsd_required=True, xsd_type="integer"
    )
    D30000_totalPlata_A = fields.Integer(
        string="totalPlata_A", xsd_required=True, xsd_type="integer"
    )
    D30000_R1_1 = fields.Integer(string="R1_1", xsd_type="integer")
    D30000_R2_1 = fields.Integer(string="R2_1", xsd_type="integer")
    D30000_R3_1 = fields.Integer(string="R3_1", xsd_type="integer")
    D30000_R3_1_1 = fields.Integer(string="R3_1_1", xsd_type="integer")
    D30000_R4_1 = fields.Integer(string="R4_1", xsd_type="integer")
    D30000_R5_1 = fields.Integer(string="R5_1", xsd_type="integer")
    D30000_R5_2 = fields.Integer(string="R5_2", xsd_type="integer")
    D30000_R5_1_1 = fields.Integer(string="R5_1_1", xsd_type="integer")
    D30000_R5_1_2 = fields.Integer(string="R5_1_2", xsd_type="integer")
    D30000_R6_1 = fields.Integer(string="R6_1", xsd_type="integer")
    D30000_R6_2 = fields.Integer(string="R6_2", xsd_type="integer")
    D30000_R7_1 = fields.Integer(string="R7_1", xsd_type="integer")
    D30000_R7_2 = fields.Integer(string="R7_2", xsd_type="integer")
    D30000_R7_1_1 = fields.Integer(string="R7_1_1", xsd_type="integer")
    D30000_R7_1_2 = fields.Integer(string="R7_1_2", xsd_type="integer")
    D30000_R8_1 = fields.Integer(string="R8_1", xsd_type="integer")
    D30000_R8_2 = fields.Integer(string="R8_2", xsd_type="integer")
    D30000_R9_1 = fields.Integer(string="R9_1", xsd_type="integer")
    D30000_R9_2 = fields.Integer(string="R9_2", xsd_type="integer")
    D30000_R10_1 = fields.Integer(string="R10_1", xsd_type="integer")
    D30000_R10_2 = fields.Integer(string="R10_2", xsd_type="integer")
    D30000_R11_1 = fields.Integer(string="R11_1", xsd_type="integer")
    D30000_R11_2 = fields.Integer(string="R11_2", xsd_type="integer")
    D30000_R12_1 = fields.Integer(string="R12_1", xsd_type="integer")
    D30000_R12_2 = fields.Integer(string="R12_2", xsd_type="integer")
    D30000_R12_1_1 = fields.Integer(string="R12_1_1", xsd_type="integer")
    D30000_R12_1_2 = fields.Integer(string="R12_1_2", xsd_type="integer")
    D30000_R12_2_1 = fields.Integer(string="R12_2_1", xsd_type="integer")
    D30000_R12_2_2 = fields.Integer(string="R12_2_2", xsd_type="integer")
    D30000_R12_3_1 = fields.Integer(string="R12_3_1", xsd_type="integer")
    D30000_R12_3_2 = fields.Integer(string="R12_3_2", xsd_type="integer")
    D30000_R13_1 = fields.Integer(string="R13_1", xsd_type="integer")
    D30000_R14_1 = fields.Integer(string="R14_1", xsd_type="integer")
    D30000_R15_1 = fields.Integer(string="R15_1", xsd_type="integer")
    D30000_R16_1 = fields.Integer(string="R16_1", xsd_type="integer")
    D30000_R16_2 = fields.Integer(string="R16_2", xsd_type="integer")
    D30000_R17_1 = fields.Integer(string="R17_1", xsd_type="integer")
    D30000_R17_2 = fields.Integer(string="R17_2", xsd_type="integer")
    D30000_R18_1 = fields.Integer(string="R18_1", xsd_type="integer")
    D30000_R18_2 = fields.Integer(string="R18_2", xsd_type="integer")
    D30000_R18_1_1 = fields.Integer(string="R18_1_1", xsd_type="integer")
    D30000_R18_1_2 = fields.Integer(string="R18_1_2", xsd_type="integer")
    D30000_R19_1 = fields.Integer(string="R19_1", xsd_type="integer")
    D30000_R19_2 = fields.Integer(string="R19_2", xsd_type="integer")
    D30000_R20_1 = fields.Integer(string="R20_1", xsd_type="integer")
    D30000_R20_2 = fields.Integer(string="R20_2", xsd_type="integer")
    D30000_R20_1_1 = fields.Integer(string="R20_1_1", xsd_type="integer")
    D30000_R20_1_2 = fields.Integer(string="R20_1_2", xsd_type="integer")
    D30000_R21_1 = fields.Integer(string="R21_1", xsd_type="integer")
    D30000_R21_2 = fields.Integer(string="R21_2", xsd_type="integer")
    D30000_R22_1 = fields.Integer(string="R22_1", xsd_type="integer")
    D30000_R22_2 = fields.Integer(string="R22_2", xsd_type="integer")
    D30000_R23_1 = fields.Integer(string="R23_1", xsd_type="integer")
    D30000_R23_2 = fields.Integer(string="R23_2", xsd_type="integer")
    D30000_R24_1 = fields.Integer(string="R24_1", xsd_type="integer")
    D30000_R24_2 = fields.Integer(string="R24_2", xsd_type="integer")
    D30000_R25_1 = fields.Integer(string="R25_1", xsd_type="integer")
    D30000_R25_2 = fields.Integer(string="R25_2", xsd_type="integer")
    D30000_R25_1_1 = fields.Integer(string="R25_1_1", xsd_type="integer")
    D30000_R25_1_2 = fields.Integer(string="R25_1_2", xsd_type="integer")
    D30000_R25_2_1 = fields.Integer(string="R25_2_1", xsd_type="integer")
    D30000_R25_2_2 = fields.Integer(string="R25_2_2", xsd_type="integer")
    D30000_R25_3_1 = fields.Integer(string="R25_3_1", xsd_type="integer")
    D30000_R25_3_2 = fields.Integer(string="R25_3_2", xsd_type="integer")
    D30000_R43_2 = fields.Integer(string="R43_2", xsd_type="integer")
    D30000_R44_2 = fields.Integer(string="R44_2", xsd_type="integer")
    D30000_R26_1 = fields.Integer(string="R26_1", xsd_type="integer")
    D30000_R26_1_1 = fields.Integer(string="R26_1_1", xsd_type="integer")
    D30000_R27_1 = fields.Integer(string="R27_1", xsd_type="integer")
    D30000_R27_2 = fields.Integer(string="R27_2", xsd_type="integer")
    D30000_R28_2 = fields.Integer(string="R28_2", xsd_type="integer")
    D30000_R29_2 = fields.Integer(string="R29_2", xsd_type="integer")
    D30000_R30_1 = fields.Integer(string="R30_1", xsd_type="integer")
    D30000_R30_2 = fields.Integer(string="R30_2", xsd_type="integer")
    D30000_R31_2 = fields.Integer(string="R31_2", xsd_type="integer")
    D30000_R32_2 = fields.Integer(string="R32_2", xsd_type="integer")
    D30000_R33_2 = fields.Integer(string="R33_2", xsd_type="integer")
    D30000_R34_2 = fields.Integer(string="R34_2", xsd_type="integer")
    D30000_R35_2 = fields.Integer(string="R35_2", xsd_type="integer")
    D30000_R36_2 = fields.Integer(string="R36_2", xsd_type="integer")
    D30000_R37_2 = fields.Integer(string="R37_2", xsd_type="integer")
    D30000_R38_2 = fields.Integer(string="R38_2", xsd_type="integer")
    D30000_R39_2 = fields.Integer(string="R39_2", xsd_type="integer")
    D30000_R40_2 = fields.Integer(string="R40_2", xsd_type="integer")
    D30000_R41_2 = fields.Integer(string="R41_2", xsd_type="integer")
    D30000_R42_2 = fields.Integer(string="R42_2", xsd_type="integer")
    D30000_nr_facturi = fields.Integer(string="nr_facturi", xsd_type="integer")
    D30000_baza = fields.Integer(string="baza", xsd_type="integer")
    D30000_tva = fields.Integer(string="tva", xsd_type="integer")
    D30000_nr_facturi_primite = fields.Integer(
        string="nr_facturi_primite", xsd_type="integer"
    )
    D30000_baza_primite = fields.Integer(string="baza_primite", xsd_type="integer")
    D30000_tva_primite = fields.Integer(string="tva_primite", xsd_type="integer")
    D30000_valoare_a = fields.Integer(string="valoare_a", xsd_type="integer")
    D30000_valoare_a1 = fields.Integer(string="valoare_a1", xsd_type="integer")
    D30000_tva_a = fields.Integer(string="tva_a", xsd_type="integer")
    D30000_tva_a1 = fields.Integer(string="tva_a1", xsd_type="integer")
    D30000_valoare_b = fields.Integer(string="valoare_b", xsd_type="integer")
    D30000_valoare_b1 = fields.Integer(string="valoare_b1", xsd_type="integer")
    D30000_tva_b = fields.Integer(string="tva_b", xsd_type="integer")
    D30000_tva_b1 = fields.Integer(string="tva_b1", xsd_type="integer")
    D30000_nr_fact_emise = fields.Integer(string="nr_fact_emise", xsd_type="integer")
    D30000_total_baza = fields.Integer(string="total_baza", xsd_type="integer")
    D30000_total_tva = fields.Integer(string="total_tva", xsd_type="integer")
    D30000_cuiSuccesor = fields.Char(string="cuiSuccesor", xsd_type="token")
    D30000_R64_1 = fields.Integer(string="R64_1", xsd_type="integer")
    D30000_R64_2 = fields.Integer(string="R64_2", xsd_type="integer")
    D30000_R65_1 = fields.Integer(string="R65_1", xsd_type="integer")
    D30000_R65_2 = fields.Integer(string="R65_2", xsd_type="integer")
    D30000_total_precedent = fields.Integer(
        string="total_precedent", xsd_type="integer"
    )
    D30000_total_curent = fields.Integer(string="total_curent", xsd_type="integer")
