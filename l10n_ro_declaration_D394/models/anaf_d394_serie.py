# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AnafD394Summary(models.Model):
    _name = "anaf.d394.summary"
    _description = "Anaf Declaration D394 Informations"

    report_id = fields.Many2one("anaf.d394", required=True, ondelete="cascade")
    tip = fields.Integer(required=True, default=0)
    serieI = fields.Char(required=True)
    nrI = fields.Char(required=True)
    nrF = fields.Char(required=True)
    den = fields.Char(required=True)
    cui = fields.Integer(required=True)
