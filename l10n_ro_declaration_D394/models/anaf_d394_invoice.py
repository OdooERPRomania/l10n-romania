# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394Invoice(models.Model):
    _name = "anaf.d394.invoice"
    _description = "Anaf Declaration D394 Invoices"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    tip_factura = fields.Integer(required=True, default=0)
    serie = fields.Char(required=True)
    nr = fields.Char(required=True)
    baza24 = fields.Integer(required=True, default=0)
    baza20 = fields.Integer(required=True, default=0)
    baza19 = fields.Integer(required=True, default=0)
    baza9 = fields.Integer(required=True, default=0)
    baza5 = fields.Integer(required=True, default=0)
    tva5 = fields.Integer(required=True, default=0)
    tva19 = fields.Integer(required=True, default=0)
    tva9 = fields.Integer(required=True, default=0)
    tva20 = fields.Integer(required=True, default=0)
    tva24 = fields.Integer(required=True, default=0)
