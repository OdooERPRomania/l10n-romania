# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

SEQUENCE_TYPE = [
    ("normal", "Invoice"),
    ("autoinv1", "Customer Auto Invoicing"),
    ("autoinv2", "Supplier  Auto Invoicing"),
]


class AccountJournal(models.Model):
    _inherit = "account.journal"

    fiscal_receipt = fields.Boolean("Fiscal Receipts Journal")
    partner_id = fields.Many2one(
        "res.partner", "Partner", related="sequence_id.partner_id"
    )
    sequence_type = fields.Selection(
        SEQUENCE_TYPE, related="sequence_id.sequence_type", string="Sequence Type"
    )
