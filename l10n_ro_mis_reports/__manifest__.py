# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Romania MIS Builder templates",
    "summary": """
        MIS Builder templates for the Romanian P&L,
        Balance Sheets and VAT Declaration""",
    "author": "NextERP Romania SRL," "Odoo Community Association (OCA)",
    "website": "http://nexterp.ro",
    "category": "Reporting",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "mis_builder",  # OCA/account-financial-reporting
        "l10n_ro",
    ],
    "data": [
        "data/mis_report_styles.xml",
        "data/mis_report_pl.xml",
        "data/mis_report_bs.xml",
        "data/mis_report_vat.xml",
    ],
    "installable": True,
}
