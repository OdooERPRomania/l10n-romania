# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394Summary2(models.Model):
    _name = "anaf.d394.summary2"
    _description = "Anaf Declaration D394 Summary2"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    cota = fields.Integer(required=True, default=0)
    bazaFSLcod = fields.Integer(required=True, default=0)
    TVAFSLcod = fields.Integer(required=True, default=0)
    bazaFSL = fields.Integer(required=True, default=0)
    TVAFSL = fields.Integer(required=True, default=0)
    bazaFSA = fields.Integer(required=True, default=0)
    TVAFSA = fields.Integer(required=True, default=0)
    bazaFSAI = fields.Integer(required=True, default=0)
    TVAFSAI = fields.Integer(required=True, default=0)
    bazaBFAI = fields.Integer(required=True, default=0)
    TVABFAI = fields.Integer(required=True, default=0)
    nrFacturiL = fields.Integer(required=True, default=0)
    bazaL = fields.Integer(required=True, default=0)
    tvaL = fields.Integer(required=True, default=0)
    nrFacturiA = fields.Integer(required=True, default=0)
    bazaA = fields.Integer(required=True, default=0)
    tvaA = fields.Integer(required=True, default=0)
    nrFacturiAI = fields.Integer(required=True, default=0)
    bazaAI = fields.Integer(required=True, default=0)
    tvaAI = fields.Integer(required=True, default=0)
    baza_incasari_i1 = fields.Integer(required=True, default=0)
    tva_incasari_i1 = fields.Integer(required=True, default=0)
    baza_incasari_i2 = fields.Integer(required=True, default=0)
    tva_incasari_i2 = fields.Integer(required=True, default=0)
    bazaL_PF = fields.Integer(required=True, default=0)
    tvaL_PF = fields.Integer(required=True, default=0)
