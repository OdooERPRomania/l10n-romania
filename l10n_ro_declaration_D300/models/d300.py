# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class RunDeclaration(models.TransientModel):
    _name = "anaf.d300"
    _inherit = "anaf.mixin"
    _description = "Declaratie D300"

    succesor_id = fields.Many2one(
        "res.partner",
        string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din "
        "Legea nr.207/2015 privind Codul de procedură fiscală",
    )
    temei = fields.Selection(
        [
            ("0", "Normal"),
            ("2", "Cf art. 105 alin. (6) lit. b) din Legea nr. 207/2015."),
        ],
        string="Temei",
        default="0",
    )
    bifa_interne = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Simplified"),
        ],
        string="Declaration Type",
        default="0",
    )
    solicit_ramb = fields.Selection(
        [
            ("N", "NU"),
            ("D", "DA"),
        ],
        string="Solicit rambursare",
        default="N",
    )
    pro_rata = fields.Integer(string="Pro Rata", default=0)
    bifa_cereale = fields.Char(string="Bifa cereale", compute="_compute_operations")
    bifa_mob = fields.Char(string="bifa_mob", compute="_compute_operations")
    bifa_disp = fields.Char(string="bifa_disp", compute="_compute_operations")
    bifa_cons = fields.Char(string="bifa_cons", compute="_compute_operations")

    R28_2 = fields.Integer(string="R28_2", compute="_compute_init_amounts")
    # Sold 4423
    R35_2_old = fields.Integer(string="Previous R35_2", compute="_compute_init_amounts")
    # Sold 4424
    R38_2_old = fields.Integer(string="Previous R38_2", compute="_compute_init_amounts")

    def _compute_operations(self):
        cereale_code = self.env.ref("l10n_ro_declaration.anaf_code_21")
        mob_code = self.env.ref("l10n_ro_declaration.anaf_code_29")
        disp_code = self.env.ref("l10n_ro_declaration.anaf_code_30")
        cons_code = self.env.ref("l10n_ro_declaration.anaf_code_31")
        for record in self:
            cust_invoices = self.get_period_invoices(
                ["out_invoice", "out_refund", "out_receipt"]
            )
            prod_codes = cust_invoices.mapped(
                "line_ids.product_id.product_tmpl_id.anaf_code_id"
            )
            record.bifa_cereale = "D" if cereale_code in prod_codes else "N"
            record.bifa_mob = "D" if mob_code in prod_codes else "N"
            record.bifa_disp = "D" if disp_code in prod_codes else "N"
            record.bifa_cons = "D" if cons_code in prod_codes else "N"

    def _compute_init_amounts(self):
        R35_2_old = 0
        R38_2_old = 0
        for record in self:
            acc_4423 = self.env["account.account"].search(
                [("code", "=", "442300"), ("company_id", "=", record.company_id.id)]
            )
            acc_4424 = self.env["account.account"].search(
                [("code", "=", "442400"), ("company_id", "=", record.company_id.id)]
            )
            if acc_4423 and acc_4424:
                ml_lines_4423 = self.env["account.move.line"].search(
                    [
                        ("move_id.state", "=", "posted"),
                        (
                            "move_id.invoice_date",
                            ">",
                            self.company_id.account_opening_date,
                        ),
                        ("move_id.invoice_date", "<=", self.date_to),
                        ("company_id", "=", self.company_id.id),
                        ("account_id", "=", acc_4423.id),
                    ]
                )
                R35_2_old = sum(ml_lines_4423.mapped("balance"))
                ml_lines_4424 = self.env["account.move.line"].search(
                    [
                        ("move_id.state", "=", "posted"),
                        (
                            "move_id.invoice_date",
                            ">",
                            self.company_id.account_opening_date,
                        ),
                        ("move_id.invoice_date", "<=", self.date_to),
                        ("company_id", "=", self.company_id.id),
                        ("account_id", "=", acc_4423.id),
                    ]
                )
                R38_2_old = sum(ml_lines_4424.mapped("balance"))
        record.R28_2 = 0
        record.R35_2_old = R35_2_old
        record.R38_2_old = R38_2_old

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

                tag_amount = (
                    type_multiplicator * (tag.tax_negate and -1 or 1) * record.balance
                )
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
