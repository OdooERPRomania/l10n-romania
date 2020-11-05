# Copyright 2020 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated Thu Nov  5 08:48:48 2020 by https://github.com/akretion/generateds-odoo
# and generateDS.py.
# Python 3.6.9 (default, Oct  8 2020, 12:12:24)  [GCC 8.4.0]
#
from odoo import fields, models


class Declaratie394(models.AbstractModel):
    _description = 'declaratie394'
    _name = 'D394.00.declaratie394'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Declaratie394Type'
    _concrete_rec_name = 'D39400_luna'

    D39400_luna = fields.Integer(
        string="luna", xsd_required=True,
        xsd_type="integer")
    D39400_an = fields.Integer(
        string="an", xsd_required=True,
        xsd_type="integer")
    D39400_tip_D394 = fields.Char(
        string="tip_D394", xsd_required=True,
        xsd_type="string")
    D39400_sistemTVA = fields.Integer(
        string="sistemTVA", xsd_required=True,
        xsd_type="integer")
    D39400_op_efectuate = fields.Integer(
        string="op_efectuate",
        xsd_required=True,
        xsd_type="integer")
    D39400_cui = fields.Char(
        string="cui", xsd_required=True,
        xsd_type="token")
    D39400_caen = fields.Char(
        string="caen", xsd_required=True,
        xsd_type="string")
    D39400_den = fields.Char(
        string="den", xsd_required=True,
        xsd_type="string")
    D39400_adresa = fields.Char(
        string="adresa", xsd_required=True,
        xsd_type="string")
    D39400_telefon = fields.Char(
        string="telefon", xsd_required=True,
        xsd_type="string")
    D39400_fax = fields.Char(
        string="fax",
        xsd_type="string")
    D39400_mail = fields.Char(
        string="mail",
        xsd_type="string")
    D39400_totalPlata_A = fields.Integer(
        string="totalPlata_A",
        xsd_required=True,
        xsd_type="integer")
    D39400_cifR = fields.Char(
        string="cifR",
        xsd_type="token")
    D39400_denR = fields.Char(
        string="denR", xsd_required=True,
        xsd_type="string")
    D39400_functie_reprez = fields.Char(
        string="functie_reprez",
        xsd_required=True,
        xsd_type="string")
    D39400_adresaR = fields.Char(
        string="adresaR", xsd_required=True,
        xsd_type="string")
    D39400_telefonR = fields.Char(
        string="telefonR",
        xsd_type="string")
    D39400_faxR = fields.Char(
        string="faxR",
        xsd_type="string")
    D39400_mailR = fields.Char(
        string="mailR",
        xsd_type="string")
    D39400_tip_intocmit = fields.Integer(
        string="tip_intocmit",
        xsd_required=True,
        xsd_type="integer")
    D39400_den_intocmit = fields.Char(
        string="den_intocmit",
        xsd_required=True,
        xsd_type="string")
    D39400_cif_intocmit = fields.Integer(
        string="cif_intocmit",
        xsd_required=True,
        xsd_type="integer")
    D39400_calitate_intocmit = fields.Char(
        string="calitate_intocmit",
        xsd_type="string")
    D39400_functie_intocmit = fields.Char(
        string="functie_intocmit",
        xsd_type="string")
    D39400_optiune = fields.Integer(
        string="optiune", xsd_required=True,
        xsd_type="integer")
    D39400_schimb_optiune = fields.Integer(
        string="schimb_optiune",
        xsd_type="integer")
    D39400_prsAfiliat = fields.Char(
        string="prsAfiliat", xsd_required=True,
        xsd_type="string")
    D39400_informatii = fields.Many2one(
        "D394.00.informatii",
        string="informatii", xsd_required=True)
    D39400_rezumat1 = fields.One2many(
        "D394.00.rezumat1",
        "D39400_rezumat1_Declaratie394_id",
        string="rezumat1"
    )
    D39400_rezumat2 = fields.One2many(
        "D394.00.rezumat2",
        "D39400_rezumat2_Declaratie394_id",
        string="rezumat2"
    )
    D39400_serieFacturi = fields.One2many(
        "D394.00.seriefacturi",
        "D39400_serieFacturi_Declaratie394_id",
        string="serieFacturi"
    )
    D39400_lista = fields.One2many(
        "D394.00.lista",
        "D39400_lista_Declaratie394_id",
        string="lista"
    )
    D39400_facturi = fields.One2many(
        "D394.00.facturi",
        "D39400_facturi_Declaratie394_id",
        string="facturi"
    )
    D39400_op1 = fields.One2many(
        "D394.00.op1",
        "D39400_op1_Declaratie394_id",
        string="op1"
    )
    D39400_op2 = fields.One2many(
        "D394.00.op2",
        "D39400_op2_Declaratie394_id",
        string="op2"
    )


class Detaliu(models.AbstractModel):
    _description = 'detaliu'
    _name = 'D394.00.detaliu'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'DetaliuType'
    _concrete_rec_name = 'D39400_bun'

    D39400_detaliu_Rezumat1_id = fields.Many2one(
        "D394.00.rezumat1")
    D39400_bun = fields.Integer(
        string="bun", xsd_required=True,
        xsd_type="integer")
    D39400_nrLivV = fields.Integer(
        string="nrLivV",
        xsd_type="integer")
    D39400_bazaLivV = fields.Integer(
        string="bazaLivV",
        xsd_type="integer")
    D39400_nrAchizC = fields.Integer(
        string="nrAchizC",
        xsd_type="integer")
    D39400_bazaAchizC = fields.Integer(
        string="bazaAchizC",
        xsd_type="integer")
    D39400_tvaAchizC = fields.Integer(
        string="tvaAchizC",
        xsd_type="integer")
    D39400_nrN = fields.Integer(
        string="nrN",
        xsd_type="integer")
    D39400_valN = fields.Integer(
        string="valN",
        xsd_type="integer")


class Facturi(models.AbstractModel):
    _description = 'facturi'
    _name = 'D394.00.facturi'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'FacturiType'
    _concrete_rec_name = 'D39400_tip_factura'

    D39400_facturi_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_tip_factura = fields.Integer(
        string="tip_factura", xsd_required=True,
        xsd_type="integer")
    D39400_serie = fields.Char(
        string="serie",
        xsd_type="string")
    D39400_nr = fields.Char(
        string="nr", xsd_required=True,
        xsd_type="string")
    D39400_baza24 = fields.Integer(
        string="baza24",
        xsd_type="integer")
    D39400_baza20 = fields.Integer(
        string="baza20",
        xsd_type="integer")
    D39400_baza19 = fields.Integer(
        string="baza19",
        xsd_type="integer")
    D39400_baza9 = fields.Integer(
        string="baza9",
        xsd_type="integer")
    D39400_baza5 = fields.Integer(
        string="baza5",
        xsd_type="integer")
    D39400_tva5 = fields.Integer(
        string="tva5",
        xsd_type="integer")
    D39400_tva19 = fields.Integer(
        string="tva19",
        xsd_type="integer")
    D39400_tva9 = fields.Integer(
        string="tva9",
        xsd_type="integer")
    D39400_tva20 = fields.Integer(
        string="tva20",
        xsd_type="integer")
    D39400_tva24 = fields.Integer(
        string="tva24",
        xsd_type="integer")


class Informatii(models.AbstractModel):
    _description = 'informatii'
    _name = 'D394.00.informatii'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'InformatiiType'
    _concrete_rec_name = 'D39400_nrCui1'

    D39400_nrCui1 = fields.Integer(
        string="nrCui1", xsd_required=True,
        xsd_type="integer")
    D39400_nrCui2 = fields.Integer(
        string="nrCui2", xsd_required=True,
        xsd_type="integer")
    D39400_nrCui3 = fields.Integer(
        string="nrCui3", xsd_required=True,
        xsd_type="integer")
    D39400_nrCui4 = fields.Integer(
        string="nrCui4", xsd_required=True,
        xsd_type="integer")
    D39400_nr_BF_i1 = fields.Integer(
        string="nr_BF_i1", xsd_required=True,
        xsd_type="integer")
    D39400_incasari_i1 = fields.Integer(
        string="incasari_i1", xsd_required=True,
        xsd_type="integer")
    D39400_incasari_i2 = fields.Integer(
        string="incasari_i2", xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturi_terti = fields.Integer(
        string="nrFacturi_terti",
        xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturi_benef = fields.Integer(
        string="nrFacturi_benef",
        xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturi = fields.Integer(
        string="nrFacturi", xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturiL_PF = fields.Integer(
        string="nrFacturiL_PF",
        xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturiLS_PF = fields.Integer(
        string="nrFacturiLS_PF",
        xsd_required=True,
        xsd_type="integer")
    D39400_val_LS_PF = fields.Integer(
        string="val_LS_PF", xsd_required=True,
        xsd_type="integer")
    D39400_tvaDed24 = fields.Integer(
        string="tvaDed24",
        xsd_type="integer")
    D39400_tvaDed20 = fields.Integer(
        string="tvaDed20",
        xsd_type="integer")
    D39400_tvaDed19 = fields.Integer(
        string="tvaDed19",
        xsd_type="integer")
    D39400_tvaDed9 = fields.Integer(
        string="tvaDed9",
        xsd_type="integer")
    D39400_tvaDed5 = fields.Integer(
        string="tvaDed5",
        xsd_type="integer")
    D39400_tvaDedAI24 = fields.Integer(
        string="tvaDedAI24", xsd_required=True,
        xsd_type="integer")
    D39400_tvaDedAI20 = fields.Integer(
        string="tvaDedAI20", xsd_required=True,
        xsd_type="integer")
    D39400_tvaDedAI19 = fields.Integer(
        string="tvaDedAI19", xsd_required=True,
        xsd_type="integer")
    D39400_tvaDedAI9 = fields.Integer(
        string="tvaDedAI9", xsd_required=True,
        xsd_type="integer")
    D39400_tvaDedAI5 = fields.Integer(
        string="tvaDedAI5", xsd_required=True,
        xsd_type="integer")
    D39400_tvaCol24 = fields.Integer(
        string="tvaCol24",
        xsd_type="integer")
    D39400_tvaCol20 = fields.Integer(
        string="tvaCol20",
        xsd_type="integer")
    D39400_tvaCol19 = fields.Integer(
        string="tvaCol19",
        xsd_type="integer")
    D39400_tvaCol9 = fields.Integer(
        string="tvaCol9",
        xsd_type="integer")
    D39400_tvaCol5 = fields.Integer(
        string="tvaCol5",
        xsd_type="integer")
    D39400_incasari_ag = fields.Integer(
        string="incasari_ag",
        xsd_type="integer")
    D39400_costuri_ag = fields.Integer(
        string="costuri_ag",
        xsd_type="integer")
    D39400_marja_ag = fields.Integer(
        string="marja_ag",
        xsd_type="integer")
    D39400_tva_ag = fields.Integer(
        string="tva_ag",
        xsd_type="integer")
    D39400_pret_vanzare = fields.Integer(
        string="pret_vanzare",
        xsd_type="integer")
    D39400_pret_cumparare = fields.Integer(
        string="pret_cumparare",
        xsd_type="integer")
    D39400_marja_antic = fields.Integer(
        string="marja_antic",
        xsd_type="integer")
    D39400_tva_antic = fields.Integer(
        string="tva_antic",
        xsd_type="integer")
    D39400_solicit = fields.Integer(
        string="solicit", xsd_required=True,
        xsd_type="integer")
    D39400_achizitiiPE = fields.Integer(
        string="achizitiiPE",
        xsd_type="integer")
    D39400_achizitiiCR = fields.Integer(
        string="achizitiiCR",
        xsd_type="integer")
    D39400_achizitiiCB = fields.Integer(
        string="achizitiiCB",
        xsd_type="integer")
    D39400_achizitiiCI = fields.Integer(
        string="achizitiiCI",
        xsd_type="integer")
    D39400_achizitiiA = fields.Integer(
        string="achizitiiA",
        xsd_type="integer")
    D39400_achizitiiB24 = fields.Integer(
        string="achizitiiB24",
        xsd_type="integer")
    D39400_achizitiiB20 = fields.Integer(
        string="achizitiiB20",
        xsd_type="integer")
    D39400_achizitiiB19 = fields.Integer(
        string="achizitiiB19",
        xsd_type="integer")
    D39400_achizitiiB9 = fields.Integer(
        string="achizitiiB9",
        xsd_type="integer")
    D39400_achizitiiB5 = fields.Integer(
        string="achizitiiB5",
        xsd_type="integer")
    D39400_achizitiiS24 = fields.Integer(
        string="achizitiiS24",
        xsd_type="integer")
    D39400_achizitiiS20 = fields.Integer(
        string="achizitiiS20",
        xsd_type="integer")
    D39400_achizitiiS19 = fields.Integer(
        string="achizitiiS19",
        xsd_type="integer")
    D39400_achizitiiS9 = fields.Integer(
        string="achizitiiS9",
        xsd_type="integer")
    D39400_achizitiiS5 = fields.Integer(
        string="achizitiiS5",
        xsd_type="integer")
    D39400_importB = fields.Integer(
        string="importB",
        xsd_type="integer")
    D39400_acINecorp = fields.Integer(
        string="acINecorp",
        xsd_type="integer")
    D39400_livrariBI = fields.Integer(
        string="livrariBI",
        xsd_type="integer")
    D39400_BUN24 = fields.Integer(
        string="BUN24",
        xsd_type="integer")
    D39400_BUN20 = fields.Integer(
        string="BUN20",
        xsd_type="integer")
    D39400_BUN19 = fields.Integer(
        string="BUN19",
        xsd_type="integer")
    D39400_BUN9 = fields.Integer(
        string="BUN9",
        xsd_type="integer")
    D39400_BUN5 = fields.Integer(
        string="BUN5",
        xsd_type="integer")
    D39400_valoareScutit = fields.Integer(
        string="valoareScutit",
        xsd_type="integer")
    D39400_BunTI = fields.Integer(
        string="BunTI",
        xsd_type="integer")
    D39400_Prest24 = fields.Integer(
        string="Prest24",
        xsd_type="integer")
    D39400_Prest20 = fields.Integer(
        string="Prest20",
        xsd_type="integer")
    D39400_Prest19 = fields.Integer(
        string="Prest19",
        xsd_type="integer")
    D39400_Prest9 = fields.Integer(
        string="Prest9",
        xsd_type="integer")
    D39400_Prest5 = fields.Integer(
        string="Prest5",
        xsd_type="integer")
    D39400_PrestScutit = fields.Integer(
        string="PrestScutit",
        xsd_type="integer")
    D39400_LIntra = fields.Integer(
        string="LIntra",
        xsd_type="integer")
    D39400_PrestIntra = fields.Integer(
        string="PrestIntra",
        xsd_type="integer")
    D39400_Export = fields.Integer(
        string="Export",
        xsd_type="integer")
    D39400_livINecorp = fields.Integer(
        string="livINecorp",
        xsd_type="integer")
    D39400_efectuat = fields.Integer(
        string="efectuat",
        xsd_type="integer")


class Lista(models.AbstractModel):
    _description = 'lista'
    _name = 'D394.00.lista'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'ListaType'
    _concrete_rec_name = 'D39400_caen'

    D39400_lista_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_caen = fields.Integer(
        string="caen", xsd_required=True,
        xsd_type="integer")
    D39400_cota = fields.Integer(
        string="cota", xsd_required=True,
        xsd_type="integer")
    D39400_operat = fields.Integer(
        string="operat", xsd_required=True,
        xsd_type="integer")
    D39400_valoare = fields.Integer(
        string="valoare", xsd_required=True,
        xsd_type="integer")
    D39400_tva = fields.Integer(
        string="tva", xsd_required=True,
        xsd_type="integer")


class Op11(models.AbstractModel):
    _description = 'op11'
    _name = 'D394.00.op11'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Op11Type'
    _concrete_rec_name = 'D39400_nrFactPR'

    D39400_op11_Op1_id = fields.Many2one(
        "D394.00.op1")
    D39400_nrFactPR = fields.Integer(
        string="nrFactPR", xsd_required=True,
        xsd_type="integer")
    D39400_codPR = fields.Char(
        string="codPR", xsd_required=True,
        xsd_type="string")
    D39400_bazaPR = fields.Integer(
        string="bazaPR", xsd_required=True,
        xsd_type="integer")
    D39400_tvaPR = fields.Integer(
        string="tvaPR",
        xsd_type="integer")


class Op1(models.AbstractModel):
    _description = 'op1'
    _name = 'D394.00.op1'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Op1Type'
    _concrete_rec_name = 'D39400_tip'

    D39400_op1_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_tip = fields.Char(
        string="tip", xsd_required=True,
        xsd_type="string")
    D39400_tip_partener = fields.Integer(
        string="tip_partener",
        xsd_required=True,
        xsd_type="integer")
    D39400_cota = fields.Integer(
        string="cota", xsd_required=True,
        xsd_type="integer")
    D39400_cuiP = fields.Char(
        string="cuiP",
        xsd_type="string")
    D39400_denP = fields.Char(
        string="denP", xsd_required=True,
        xsd_type="string")
    D39400_taraP = fields.Char(
        string="taraP",
        xsd_type="string")
    D39400_locP = fields.Char(
        string="locP",
        xsd_type="string")
    D39400_judP = fields.Char(
        string="judP",
        xsd_type="string")
    D39400_strP = fields.Char(
        string="strP",
        xsd_type="string")
    D39400_nrP = fields.Char(
        string="nrP",
        xsd_type="string")
    D39400_blP = fields.Char(
        string="blP",
        xsd_type="string")
    D39400_apP = fields.Char(
        string="apP",
        xsd_type="string")
    D39400_detP = fields.Char(
        string="detP",
        xsd_type="string")
    D39400_tip_document = fields.Integer(
        string="tip_document",
        xsd_type="integer")
    D39400_nrFact = fields.Integer(
        string="nrFact", xsd_required=True,
        xsd_type="integer")
    D39400_baza = fields.Integer(
        string="baza", xsd_required=True,
        xsd_type="integer")
    D39400_tva = fields.Integer(
        string="tva",
        xsd_type="integer")
    D39400_op11 = fields.One2many(
        "D394.00.op11",
        "D39400_op11_Op1_id",
        string="op11"
    )


class Op2(models.AbstractModel):
    _description = 'op2'
    _name = 'D394.00.op2'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Op2Type'
    _concrete_rec_name = 'D39400_tip_op2'

    D39400_op2_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_tip_op2 = fields.Char(
        string="tip_op2", xsd_required=True,
        xsd_type="string")
    D39400_luna = fields.Integer(
        string="luna", xsd_required=True,
        xsd_type="integer")
    D39400_nrAMEF = fields.Integer(
        string="nrAMEF",
        xsd_type="integer")
    D39400_nrBF = fields.Integer(
        string="nrBF",
        xsd_type="integer")
    D39400_total = fields.Integer(
        string="total", xsd_required=True,
        xsd_type="integer")
    D39400_baza20 = fields.Integer(
        string="baza20", xsd_required=True,
        xsd_type="integer")
    D39400_baza9 = fields.Integer(
        string="baza9", xsd_required=True,
        xsd_type="integer")
    D39400_baza5 = fields.Integer(
        string="baza5", xsd_required=True,
        xsd_type="integer")
    D39400_TVA20 = fields.Integer(
        string="TVA20", xsd_required=True,
        xsd_type="integer")
    D39400_TVA9 = fields.Integer(
        string="TVA9", xsd_required=True,
        xsd_type="integer")
    D39400_TVA5 = fields.Integer(
        string="TVA5", xsd_required=True,
        xsd_type="integer")
    D39400_baza19 = fields.Integer(
        string="baza19", xsd_required=True,
        xsd_type="integer")
    D39400_TVA19 = fields.Integer(
        string="TVA19", xsd_required=True,
        xsd_type="integer")


class Rezumat1(models.AbstractModel):
    _description = 'rezumat1'
    _name = 'D394.00.rezumat1'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Rezumat1Type'
    _concrete_rec_name = 'D39400_tip_partener'

    D39400_rezumat1_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_tip_partener = fields.Integer(
        string="tip_partener",
        xsd_required=True,
        xsd_type="integer")
    D39400_cota = fields.Integer(
        string="cota", xsd_required=True,
        xsd_type="integer")
    D39400_facturiL = fields.Integer(
        string="facturiL",
        xsd_type="integer")
    D39400_bazaL = fields.Integer(
        string="bazaL",
        xsd_type="integer")
    D39400_tvaL = fields.Integer(
        string="tvaL",
        xsd_type="integer")
    D39400_facturiLS = fields.Integer(
        string="facturiLS",
        xsd_type="integer")
    D39400_bazaLS = fields.Integer(
        string="bazaLS",
        xsd_type="integer")
    D39400_facturiA = fields.Integer(
        string="facturiA",
        xsd_type="integer")
    D39400_bazaA = fields.Integer(
        string="bazaA",
        xsd_type="integer")
    D39400_tvaA = fields.Integer(
        string="tvaA",
        xsd_type="integer")
    D39400_facturiAI = fields.Integer(
        string="facturiAI",
        xsd_type="integer")
    D39400_bazaAI = fields.Integer(
        string="bazaAI",
        xsd_type="integer")
    D39400_tvaAI = fields.Integer(
        string="tvaAI",
        xsd_type="integer")
    D39400_facturiAS = fields.Integer(
        string="facturiAS",
        xsd_type="integer")
    D39400_bazaAS = fields.Integer(
        string="bazaAS",
        xsd_type="integer")
    D39400_facturiV = fields.Integer(
        string="facturiV",
        xsd_type="integer")
    D39400_bazaV = fields.Integer(
        string="bazaV",
        xsd_type="integer")
    D39400_facturiC = fields.Integer(
        string="facturiC",
        xsd_type="integer")
    D39400_bazaC = fields.Integer(
        string="bazaC",
        xsd_type="integer")
    D39400_tvaC = fields.Integer(
        string="tvaC",
        xsd_type="integer")
    D39400_facturiN = fields.Integer(
        string="facturiN",
        xsd_type="integer")
    D39400_document_N = fields.Integer(
        string="document_N",
        xsd_type="integer")
    D39400_bazaN = fields.Integer(
        string="bazaN",
        xsd_type="integer")
    D39400_detaliu = fields.One2many(
        "D394.00.detaliu",
        "D39400_detaliu_Rezumat1_id",
        string="detaliu"
    )


class Rezumat2(models.AbstractModel):
    _description = 'rezumat2'
    _name = 'D394.00.rezumat2'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'Rezumat2Type'
    _concrete_rec_name = 'D39400_cota'

    D39400_rezumat2_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_cota = fields.Integer(
        string="cota",
        xsd_type="integer")
    D39400_bazaFSLcod = fields.Integer(
        string="bazaFSLcod", xsd_required=True,
        xsd_type="integer")
    D39400_TVAFSLcod = fields.Integer(
        string="TVAFSLcod", xsd_required=True,
        xsd_type="integer")
    D39400_bazaFSL = fields.Integer(
        string="bazaFSL", xsd_required=True,
        xsd_type="integer")
    D39400_TVAFSL = fields.Integer(
        string="TVAFSL", xsd_required=True,
        xsd_type="integer")
    D39400_bazaFSA = fields.Integer(
        string="bazaFSA", xsd_required=True,
        xsd_type="integer")
    D39400_TVAFSA = fields.Integer(
        string="TVAFSA", xsd_required=True,
        xsd_type="integer")
    D39400_bazaFSAI = fields.Integer(
        string="bazaFSAI", xsd_required=True,
        xsd_type="integer")
    D39400_TVAFSAI = fields.Integer(
        string="TVAFSAI", xsd_required=True,
        xsd_type="integer")
    D39400_bazaBFAI = fields.Integer(
        string="bazaBFAI", xsd_required=True,
        xsd_type="integer")
    D39400_TVABFAI = fields.Integer(
        string="TVABFAI", xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturiL = fields.Integer(
        string="nrFacturiL", xsd_required=True,
        xsd_type="integer")
    D39400_bazaL = fields.Integer(
        string="bazaL", xsd_required=True,
        xsd_type="integer")
    D39400_tvaL = fields.Integer(
        string="tvaL", xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturiA = fields.Integer(
        string="nrFacturiA", xsd_required=True,
        xsd_type="integer")
    D39400_bazaA = fields.Integer(
        string="bazaA", xsd_required=True,
        xsd_type="integer")
    D39400_tvaA = fields.Integer(
        string="tvaA", xsd_required=True,
        xsd_type="integer")
    D39400_nrFacturiAI = fields.Integer(
        string="nrFacturiAI", xsd_required=True,
        xsd_type="integer")
    D39400_bazaAI = fields.Integer(
        string="bazaAI", xsd_required=True,
        xsd_type="integer")
    D39400_tvaAI = fields.Integer(
        string="tvaAI", xsd_required=True,
        xsd_type="integer")
    D39400_baza_incasari_i1 = fields.Integer(
        string="baza_incasari_i1",
        xsd_type="integer")
    D39400_tva_incasari_i1 = fields.Integer(
        string="tva_incasari_i1",
        xsd_type="integer")
    D39400_baza_incasari_i2 = fields.Integer(
        string="baza_incasari_i2",
        xsd_type="integer")
    D39400_tva_incasari_i2 = fields.Integer(
        string="tva_incasari_i2",
        xsd_type="integer")
    D39400_bazaL_PF = fields.Integer(
        string="bazaL_PF", xsd_required=True,
        xsd_type="integer")
    D39400_tvaL_PF = fields.Integer(
        string="tvaL_PF", xsd_required=True,
        xsd_type="integer")


class SerieFacturi(models.AbstractModel):
    _description = 'seriefacturi'
    _name = 'D394.00.seriefacturi'
    _inherit = 'spec.mixin.D394'
    _generateds_type = 'SerieFacturiType'
    _concrete_rec_name = 'D39400_tip'

    D39400_serieFacturi_Declaratie394_id = fields.Many2one(
        "D394.00.declaratie394")
    D39400_tip = fields.Integer(
        string="tip", xsd_required=True,
        xsd_type="integer")
    D39400_serieI = fields.Char(
        string="serieI",
        xsd_type="string")
    D39400_nrI = fields.Char(
        string="nrI", xsd_required=True,
        xsd_type="string")
    D39400_nrF = fields.Char(
        string="nrF",
        xsd_type="string")
    D39400_den = fields.Char(
        string="den",
        xsd_type="string")
    D39400_cui = fields.Char(
        string="cui",
        xsd_type="token")
