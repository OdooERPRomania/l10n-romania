# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


def _partner_split_name(partner_name):
    return [" ".join(partner_name.split()[:-1]), " ".join(partner_name.split()[-1:])]


class AnafSignature(models.Model):
    _name = "anaf.signature"
    _description = "Anaf Signature"

    name = fields.Char(string="Name", required=True)
    first_name = fields.Char(string="First Name", compute="_compute_partner_name")
    last_name = fields.Char(string="Last Name", compute="_compute_partner_name")
    type = fields.Selection(
        [("person", "Fizical Person"), ("company", "Company")],
        string="Type",
        required=True,
        default="person",
    )
    function = fields.Char(string="Function", required=True)
    vat = fields.Char(string="VAT", required=True)
    quality = fields.Char(string="Quality", required=True)

    @api.depends("name")
    def _compute_partner_name(self):
        for partner in self:
            partner.first_name = _partner_split_name(partner.name)[0]
            partner.last_name = _partner_split_name(partner.name)[1]
