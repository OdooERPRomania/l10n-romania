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
SEQUENCE_TYPE = [
     ("normal", "Invoice"),
     ("autoinv1", "Customer Auto Invoicing"),
     ("autoinv2", "Supplier  Auto Invoicing"),]


class AccountMove(models.Model):
    _inherit = "account.move"


    def _check_special_taxes(self):
        self.ensure_one()
        check = False
        for line in self.invoice_line_ids:
            for tax_line in line.tax_ids:
                if any(i in tax_line.name for i in (' 9', ' 5')):
                    check = True
        return check

    def _get_inv_number(self):
        regex1 = re.compile("[^0-9]")
        for inv in self:
            if (
                inv.move_type
                in (
                    "out_invoice",
                    "out_refund",
                )
                or inv.sequence_type in ("autoinv1", "autoinv2")
            ):
                inv.inv_number = int(10
                    # regex1.sub(
                    #     "", inv.name.replace('inv.sequence_type.prefix', '10'))
                )
            else:
                if inv.ref:
                    val = inv.ref
                else:
                    val = inv.name
                if val:
                    inv.inv_number = int(10
                        # regex1.sub(
                        #     "", val.replace('inv.sequence_type.prefix', '11'))
                    )
        return True


    def _get_operation_type(self):
        for inv in self:
            partner = inv.partner_id
            country_ro = self.env.ref("base.ro")
            if inv.move_type in ("out_invoice", "out_refund"):
                if inv.fiscal_position_id and (
                    "Taxare Inversa" in inv.fiscal_position_id.name
                ):
                    oper_type = "V"
                elif not inv.fiscal_position_id or (
                    inv.fiscal_position_id and ("National" in inv.fiscal_position_id.name)
                ):
                    if inv._check_special_taxes():
                        oper_type = "LS"
                    elif partner.country_id and partner.country_id.id != country_ro.id:
                        oper_type = "V"
                    else:
                        oper_type = "L"
                else:
                    oper_type = "L"
            else:
                if not partner.is_company and inv.invoice_origin:
                    oper_type = "N"
                elif inv.fiscal_position_id and (
                    ("Taxare Inversa" in inv.fiscal_position_id.name)
                    or ("Comunitar" in inv.fiscal_position_id.name)
                ):
                    oper_type = "C"
                elif inv.fiscal_position_id and ("Scutite" in inv.fiscal_position_id.name):
                    if partner.country_id and partner.country_id.id == country_ro.id:
                        if inv._check_special_taxes():
                            oper_type = "AS"
                        else:
                            oper_type = "A"
                    else:
                        oper_type = "C"
                elif not inv.fiscal_position_id or (
                    inv.fiscal_position_id and ("National" in inv.fiscal_position_id.name)
                ):
                    if inv._check_special_taxes():
                        oper_type = "AS"
                    elif inv.fiscal_position_id=="vat la incasare ":
                        oper_type = "AI"
                    else:
                        oper_type = "A"
                elif inv.fiscal_position_id=="vat la incasare":
                    oper_type = "AI"
                else:
                    oper_type = "A"
            inv.operation_type = oper_type
        return True

    def _get_partner_type(self):
        for inv in self:
            partner = inv.partner_id
            eur_countries = []
            eur_grp = self.env.ref('base.europe')
            if eur_grp:
                eur_countries = [country.id for country in eur_grp.country_ids]
            if partner.country_id and \
                partner.country_id.id == self.env.ref('base.ro').id:
                if partner.vat_subjected:
                    new_type = '1'
                else:
                    new_type = '2'
            elif partner.country_id.id in eur_countries:
                new_type = '3'
            else:
                new_type = '4'
            inv.partner_type = new_type
        return True

    sequence_type = fields.Selection(
        SEQUENCE_TYPE, string="Sequence Type"
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
