# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import api, fields, models

OPERATION_TYPE = [
    ("L", "Customer Invoice"),
    ("A", "Supplier Invoice"),
    ("LS", "Special Customer Invoice"),
    ("AS", "Special Supplier Invoice"),
    ("AI", "VAT on Payment Supplier Invoice"),
    ("V", "Inverse Taxation Customer Invoice"),
    ("C", "Inverse Taxation Supplier Invoice"),
    ("N", "Fizical Persons Supplier Invoice"),
]


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_inv_number(self):
        regex1 = re.compile("[^0-9]")
        for inv in self:
            if (
                inv.move_type
                in (
                    "out_invoice",
                    "out_refund",
                )
                or inv.journal_id.sequence_type in ("autoinv1", "autoinv2")
            ):
                inv.inv_number = int(
                    regex1.sub(
                        "", inv.name.replace(inv.journal_id.sequence_id.prefix, "")
                    )
                )
            else:
                if inv.supplier_invoice_number:
                    val = inv.supplier_invoice_number
                else:
                    val = inv.internal_number
                if val:
                    inv.inv_number = int(
                        regex1.sub(
                            "", val.replace(inv.journal_id.sequence_id.prefix, "")
                        )
                    )
        return True


    def _get_operation_type(self):
        for inv in self:
            partner = inv.partner_id
            country_ro = self.env.ref("base.ro")
            if inv.type in ("out_invoice", "out_refund"):
                if inv.fiscal_position and (
                    "Taxare Inversa" in inv.fiscal_position.name
                ):
                    oper_type = "V"
                elif not inv.fiscal_position or (
                    inv.fiscal_position and ("National" in inv.fiscal_position.name)
                ):
                    if inv.special_taxes:
                        oper_type = "LS"
                    elif partner.country_id and partner.country_id.id != country_ro.id:
                        oper_type = "V"
                    else:
                        oper_type = "L"
                else:
                    oper_type = "L"
            else:
                if not partner.is_company and inv.origin_type:
                    oper_type = "N"
                elif inv.fiscal_position and (
                    ("Taxare Inversa" in inv.fiscal_position.name)
                    or ("Comunitar" in inv.fiscal_position.name)
                ):
                    oper_type = "C"
                elif inv.fiscal_position and ("Scutite" in inv.fiscal_position.name):
                    if partner.country_id and partner.country_id.id == country_ro.id:
                        if inv.special_taxes:
                            oper_type = "AS"
                        else:
                            oper_type = "A"
                    else:
                        oper_type = "C"
                elif not inv.fiscal_position or (
                    inv.fiscal_position and ("National" in inv.fiscal_position.name)
                ):
                    if inv.special_taxes:
                        oper_type = "AS"
                    elif inv.vat_on_payment:
                        oper_type = "AI"
                    else:
                        oper_type = "A"
                elif inv.vat_on_payment:
                    oper_type = "AI"
                else:
                    oper_type = "A"
            inv.operation_type = oper_type
        return True

    sequence_type = fields.Selection(
        related="journal_id.sequence_type", string="Sequence Type"
    )
    operation_type = fields.Selection(
        OPERATION_TYPE,
        compute="_get_operation_type",
        string="Operation Type",
        store=True,
        index=True,
    )
    inv_number = fields.Char(
        "Invoice Number", compute="_get_inv_number", store=True, index=True
    )
    partner_type = fields.Char(
        "D394 Partner Type", compute="_get_partner_type", store=True, index=True
    )
