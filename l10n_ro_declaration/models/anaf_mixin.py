# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import logging

from dateutil.relativedelta import relativedelta
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import xml_utils

_logger = logging.getLogger(__name__)


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

    declaration_id = fields.Many2one("anaf.declaration", string="ANAF Declaration")
    version_id = fields.Many2one(
        "anaf.declaration.version", string="ANAF Declaration Version"
    )
    signature_id = fields.Many2one(
        "anaf.signature", string="SSL Signature", help="SSL Signature of the Document"
    )
    bank_account_id = fields.Many2one("res.partner.bank", string="Bank Account")

    date_range_id = fields.Many2one(
        comodel_name="date.range",
        string="Date range",
        domain="['|',('company_id','=',company_id)," "('company_id','=',False)]",
    )
    date_from = fields.Date("Start Date", required=True, default=_get_default_date_from)
    date_to = fields.Date("End Date", required=True, default=_get_default_date_to)
    date_next = fields.Date("Next Date", compute="_compute_next_date")
    name = fields.Char("File Name", compute="_compute_anaf_filename", default="")
    file_save = fields.Binary(string="Report File", readonly=True)

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for fy in self:
            # Starting date must be prior to the ending date
            date_from = fy.date_from
            date_to = fy.date_to
            if date_to < date_from:
                raise ValidationError(
                    _("The ending date must not be prior to the starting " "date.")
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
        r = relativedelta(self.date_to, self.date_from)
        months = r.months + 12 * r.years + 1
        return months

    @api.model
    def get_year_month(self):
        year = month = ""
        if self.date_to:
            year = fields.Date.from_string(self.date_to).year
            month = fields.Date.from_string(self.date_to).month
            month = "{:2s}".format(str(month).zfill(2))
        return year, month

    def _compute_next_date(self):
        for record in self:
            months = record.get_months_number()
            if record.date_to:
                record.date_next = self.date_to + relativedelta(day=25, months=months)

    @api.depends("declaration_id", "company_id")
    def _compute_anaf_filename(self):
        year, month = self.get_year_month()
        self.name = "{} - {} - {}-{}.{}".format(
            self.declaration_id.name, self.company_id.vat, year, month, "xml"
        )

    @api.model
    def get_period_invoices_by_tags(self, types, tags):
        invoices = (
            self.env["account.move.line"]
            .search(
                [
                    ("move_id.state", "=", "posted"),
                    ("move_id.move_type", "in", types),
                    ("move_id.invoice_date", ">=", self.date_from),
                    ("move_id.invoice_date", "<=", self.date_to),
                    ("move_id.company_id", "=", self.company_id.id),
                    ("tax_tag_ids", "in", tags),
                ],
            )
            .mapped("move_id")
        )
        return invoices.sorted(key=lambda r: r.invoice_date)

    @api.model
    def get_period_invoices(self, types):
        invoices = self.env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("move_type", "in", types),
                ("invoice_date", ">=", self.date_from),
                ("invoice_date", "<=", self.date_to),
                ("company_id", "=", self.company_id.id),
            ],
            order="invoice_date, name, ref",
        )
        return invoices

    @api.model
    def get_period_vatp_invoices(self, types):
        fp = self.company_id.property_vat_on_payment_position_id
        if not fp:
            fp = self.env["account.fiscal.position"].search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("name", "=", "Regim TVA la Incasare"),
                ]
            )
        invoices = self.env["account.move"]
        if fp:
            vatp_invoices = self.env["account.move"].search(
                [
                    ("state", "in", ["posted", "cancel"]),
                    ("move_type", "in", types),
                    ("invoice_date", ">", self.company_id.account_opening_date),
                    ("invoice_date", "<=", self.date_to),
                    ("company_id", "=", self.company_id.id),
                    ("fiscal_position_id", "=", fp.id),
                ]
            )
            for inv in vatp_invoices:
                if inv.payment_state not in ["paid", "reversed", "invoicing_legacy"]:
                    invoices |= inv
                elif inv.payment_state == "paid":
                    for payment in self._get_reconciled_invoices_partials():
                        if (
                            payment.date >= self.date_from
                            and payment.date <= self.date_to
                        ):
                            invoices |= inv
        return invoices

    def value_to_string(self, value):
        return '"' + str(value) + '"'

    @api.model
    def _get_tax_report_domain(self, company_id, date_from, date_to):
        domain = [
            ("company_id", "=", company_id),
            ("date", ">=", date_from),
            ("date", "<=", date_to),
            ("tax_exigible", "=", True),
            ("tax_tag_ids", "!=", False),
            ("move_id.state", "=", "posted"),
        ]
        if self.env.context.get("move_id", False):
            domain += [("move_id.id", "=", self.env.context["move_id"])]
        return domain

    def _get_vat_report_data(self, company_id, date_from, date_to):
        mv_line_obj = self.env["account.move.line"]
        vat_report = {}
        tax_domain = self._get_tax_report_domain(company_id, date_from, date_to)
        tax_move_lines = mv_line_obj.search(tax_domain)
        for record in tax_move_lines:
            for tag in record.tax_tag_ids:
                if record.move_id.tax_cash_basis_rec_id:
                    # Cash basis entries are always treated as misc operations, applying the tag sign directly to the balance
                    type_multiplicator = 1
                    if record.tax_ids and record.tax_ids[0].type_tax_use == "sale":
                        type_multiplicator = -1
                else:
                    type_multiplicator = (
                        record.journal_id.type == "sale" and -1 or 1
                    ) * (
                        mv_line_obj._get_refund_tax_audit_condition(record) and -1 or 1
                    )

                tag_amount = type_multiplicator * record.balance
                if tag.tax_report_line_ids:
                    # Then, the tag comes from a report line, and hence has a + or - sign (also in its name)
                    for report_line in tag.tax_report_line_ids:
                        tag_id = report_line.tag_name
                        if tag_id not in vat_report.keys():
                            vat_report[tag_id] = 0.0
                        vat_report[tag_id] += tag_amount
                else:
                    # Then, it's a financial tag (sign is always +, and never shown in tag name)
                    tag_id = tag.name
                    if tag_id not in vat_report.keys():
                        vat_report[tag_id] = 0.0
                    vat_report[tag_id] += tag_amount
        return vat_report

    def get_report(self):
        model = self.version_id.model
        validator = self.version_id.validator
        _logger.warning(model.model)
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
        _logger.warning(h)
        if validator:
            xml_utils._check_with_xsd(h, validator.name, self.env)
        self.file_save = base64.encodebytes(xmlfile)
        return {
            "name": _("Save"),
            "context": self.env.context,
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "type": "ir.actions.act_window",
            "target": "new",
            "res_id": self.id,
        }
