# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394OP1(models.Model):
    _name = "anaf.d394.op1"
    _description = "Anaf Declaration D394 OP1"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    tip_op2 = fields.Char(required=True)
    luna = fields.Integer(required=True, default=0)
    nrAMEF = fields.Integer(required=True, default=0)
    nrBF = fields.Integer(required=True, default=0)
    total = fields.Integer(required=True, default=0)
    baza20 = fields.Integer(required=True, default=0)
    baza9 = fields.Integer(required=True, default=0)
    baza5 = fields.Integer(required=True, default=0)
    TVA20 = fields.Integer(required=True, default=0)
    TVA9 = fields.Integer(required=True, default=0)
    TVA5 = fields.Integer(required=True, default=0)
    baza19 = fields.Integer(required=True, default=0)
    TVA19 = fields.Integer(required=True, default=0)
