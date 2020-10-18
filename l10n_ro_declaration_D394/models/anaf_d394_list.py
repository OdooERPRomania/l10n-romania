# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394List(models.Model):
    _name = "anaf.d394.list"
    _description = "Anaf Declaration D394 List"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    caen = fields.Integer(required=True, default=0)
    cota = fields.Integer(required=True, default=0)
    operat = fields.Integer(required=True, default=0)
    valoare = fields.Integer(required=True, default=0)
    tva = fields.Integer(required=True, default=0)
