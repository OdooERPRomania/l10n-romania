# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394OP1(models.Model):
    _name = "anaf.d394.op1"
    _description = "Anaf Declaration D394 OP1"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", required=True, ondelete="restrict")
    tax_id = fields.Many2one("account.tax", required=True, ondelete="restrict")
    tip = fields.Integer(required=True, default=0)
    tip_partener = fields.Integer(required=True, default=0)
    cota = fields.Integer(required=True, default=0)
    cuiP = fields.Char(required=True)
    denP = fields.Char(required=True)
    taraP = fields.Char(required=True)
    locP = fields.Char(required=True)
    judP = fields.Char(required=True)
    strP = fields.Char(required=True)
    nrP = fields.Char(required=True)
    blP = fields.Char(required=True)
    apP = fields.Char(required=True)
    detP = fields.Char(required=True)
    tip_document = fields.Integer(required=True, default=0)
    nrFact = fields.Integer(required=True, default=0)
    baza = fields.Integer(required=True, default=0)
    tva = fields.Integer(required=True, default=0)
    op11_ids = fields.One2many("anaf.d394.op11", "op1_id")


class AnafD394OP11(models.Model):
    _name = "anaf.d394.op11"
    _description = "Anaf Declaration D394 OP11"

    op1_id = fields.Many2one("anaf.d394.op1", required=True, ondelete="cascade")
    nrFactPR = fields.Integer(required=True, default=0)
    codPR = fields.Char(required=True)
    bazaPR = fields.Integer(required=True, default=0)
    tvaPR = fields.Integer(required=True, default=0)
