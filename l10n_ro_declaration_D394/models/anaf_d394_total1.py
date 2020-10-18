# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394Summary1(models.Model):
    _name = "anaf.d394.summary1"
    _description = "Anaf Declaration D394 Summary1"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    tip_partener = fields.Integer(required=True, default=0)
    cota = fields.Integer(required=True, default=0)
    facturiL = fields.Integer(required=True, default=0)
    bazaL = fields.Integer(required=True, default=0)
    tvaL = fields.Integer(required=True, default=0)
    facturiLS = fields.Integer(required=True, default=0)
    bazaLS = fields.Integer(required=True, default=0)
    facturiA = fields.Integer(required=True, default=0)
    bazaA = fields.Integer(required=True, default=0)
    tvaA = fields.Integer(required=True, default=0)
    facturiAI = fields.Integer(required=True, default=0)
    bazaAI = fields.Integer(required=True, default=0)
    tvaAI = fields.Integer(required=True, default=0)
    facturiAS = fields.Integer(required=True, default=0)
    bazaAS = fields.Integer(required=True, default=0)
    facturiV = fields.Integer(required=True, default=0)
    bazaV = fields.Integer(required=True, default=0)
    facturiC = fields.Integer(required=True, default=0)
    bazaC = fields.Integer(required=True, default=0)
    tvaC = fields.Integer(required=True, default=0)
    facturiN = fields.Integer(required=True, default=0)
    document_N = fields.Integer(required=True, default=0)
    bazaN = fields.Integer(required=True, default=0)
    detail_ids = fields.One2many("anaf.d394.total1.detail", "total_id")


class AnafD394Total1Detail(models.Model):
    _name = "anaf.d394.summary1.detail"
    _description = "Anaf Declaration D394 Summary1 Detail"

    total_id = fields.Many2one("anaf.d394.summary1", required=True, ondelete="cascade")
    bun = fields.Integer(required=True, default=0)
    nrLivV = fields.Integer(required=True, default=0)
    bazaLivV = fields.Integer(required=True, default=0)
    nrAchizC = fields.Integer(required=True, default=0)
    bazaAchizC = fields.Integer(required=True, default=0)
    tvaAchizC = fields.Integer(required=True, default=0)
    nrN = fields.Integer(required=True, default=0)
    valN = fields.Integer(required=True, default=0)
