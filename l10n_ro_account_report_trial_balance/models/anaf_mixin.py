# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from base64 import b64decode, b64encode

from dateutil.relativedelta import relativedelta
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

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
    bank_account_id = fields.Many2one(
        "res.partner.bank",
        string="Bank Account",
        # domain=[("id", "in", company_id.partner_id.bank_ids.ids)]
    )

    declaration_id = fields.Many2one(
        "anaf.declaration",
        string="ANAF Declaration",
        required=True,
        default=_get_default_date_to,
    )
    version_id = fields.Many2one(
        "anaf.declaration.version", string="ANAF Declaration Version", required=True
    )
    signature_id = fields.Many2one(
        "anaf.signature",
        string="SSL Signature",
        help="SSL Signature of the Document",
        required=True,
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

    @api.model
    def validate_report(self, xsd_schema_doc, content):
        """
        Validate final xml file against xsd_schema`

        Args:
         * xsd_schema_doc(byte-string) - report validation schema
         * content(str) - report content for validation

        Raises:
         * odoo.exceptions.ValidationError - Syntax of final report is wrong

        Returns:
         * bool - True
        """
        if xsd_schema_doc:
            # create validation parser
            decoded_xsd_schema_doc = b64decode(xsd_schema_doc)
            parsed_xsd_schema = etree.XML(decoded_xsd_schema_doc)
            xsd_schema = etree.XMLSchema(parsed_xsd_schema)
            parser = etree.XMLParser(schema=xsd_schema)

            try:
                # check content
                etree.fromstring(content, parser)
            except etree.XMLSyntaxError as error:
                raise ValidationError(error.msg)
        return True

    @api.depends("declaration_id", "company_id")
    def get_anaf_filename(self):
        self.name = "{} - {}.{}".format(
            self.declaration_id.name, self.company_id.vat, "xml"
        )

    def get_report(self):
        model = self.version_id.model
        validator = self.version_id.validator
        xmldict = self.env[model.model].build_file()
        if validator:
            self.validate_report(validator, xmldict)
        self.file = b64encode(xmldict)
