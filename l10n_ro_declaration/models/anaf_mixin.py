# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from base64 import b64encode
from lxml import etree

from dateutil.relativedelta import relativedelta
import logging

from odoo import api, fields, models, _
from odoo.tools import xml_utils

logger = logging.getLogger(__name__)


class AnafMixin(models.AbstractModel):
    _name = "anaf.mixin"
    _description = "Anaf Declaration Mixin"

    def _get_default_date_from(self):
        today = fields.Date.from_string(fields.Date.today())
        return today + relativedelta(day=1, months=-1)

    def _get_default_date_to(self):
        today = fields.Date.from_string(fields.Date.today())
        return today + relativedelta(day=1, days=-1)

    def _get_default_declaration(self):
        return self.env["anaf.declaration"].search([], limit=1)

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env["res.company"]._company_default_get("anaf.mixin"),
    )
    bank_account_id = fields.Many2one("res.partner.bank", string="Bank Account")

    declaration_id = fields.Many2one("anaf.declaration", string="ANAF Declaration")
    version_id = fields.Many2one(
        "anaf.declaration.version", string="ANAF Declaration Version"
    )
    signature_id = fields.Many2one(
        "anaf.signature", string="SSL Signature", help="SSL Signature of the Document"
    )

    date_range_id = fields.Many2one(comodel_name="date.range", string="Date range")
    date_from = fields.Date("Start Date", required=True, default=_get_default_date_from)
    date_to = fields.Date("End Date", required=True, default=_get_default_date_to)
    name = fields.Char("File Name", compute="get_anaf_filename", default="")
    file = fields.Binary(
        string="File",
        readonly=True,
        help="Export file related to this batch",
        copy=False,
    )

    @api.onchange("declaration_id")
    def _onchange_declaration_id(self):
        if self.declaration_id:
            self.version_id = self.declaration_id.version_ids[0]
        else:
            self.version_id = False

    @api.onchange("date_range_id")
    def onchange_date_range_id(self):
        """Handle date range change."""
        if self.date_range_id:
            self.date_from = self.date_range_id.date_start
            self.date_to = self.date_range_id.date_end

    @api.model
    def get_months_number(self):
        r = relativedelta(self.date_from, self.date_to)
        months = r.months + 12 * r.years
        if r.days > 0:
            months += 1
        return months

    @api.model
    def get_year_month(self):
        year = month = ""
        if self.date_to:
            year = fields.Date.from_string(self.date_to).year
            month = fields.Date.from_string(self.date_to).month
            month = "{:2s}".format(str(month).zfill(2))
        return year, month

    @api.depends("declaration_id", "company_id")
    def get_anaf_filename(self):
        self.name = "{} - {}.{}".format(
            self.declaration_id.name, self.company_id.vat, "xml"
        )

    @api.model
    def get_period_invoices(self, types):
        invoices = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('move_type', 'in', types),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('company_id', '=', self.company_id.id)
        ])
        return invoices

    @api.model
    def get_period_vatp_invoices(self, types):
        fp = self.company_id.property_vat_on_payment_position_id
        invoices = self.env['account.move']
        if fp:
            vatp_invoices = self.env['account.move'].search([
                ('state', 'in', ['posted', 'cancel']),
                ('move_type', 'in', types),
                ('invoice_date', '>', self.company_id.account_opening_date),
                ('invoice_date', '<=', self.date_to),
                ('company_id', '=', self.company_id.id),
                ('fiscal_position_id', '=', fp.id)
            ])
            for inv in vatp_invoices:
                if inv.payment_state not in ['paid',
                                             'reversed',
                                             'invoicing_legacy']:
                    invoices |= inv
                elif inv.payment_state == 'paid':
                    for payment in self._get_reconciled_invoices_partials():
                        if payment.date >= self.date_from and \
                                payment.date <= self.date_to:
                            invoices |= inv
        return invoices

    def get_report(self):
        model = self.version_id.model
        validator = self.version_id.validator
        declaration = self.env[model.model].create(
            {
                "company_id": self.company_id.id,
                "bank_account_id": self.bank_account_id.id,
                "signature_id": self.signature_id.id,
                "date_from": self.date_from,
                "date_to": self.date_to,
            }
        )
        xmlfile = declaration.build_file().encode("utf-8")
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")
        h = etree.fromstring(xmlfile, parser=parser)
        print(xmlfile)
        print(h)
        if validator:
            xml_utils._check_with_xsd(h, validator)
        self.file = b64encode(xmlfile)
