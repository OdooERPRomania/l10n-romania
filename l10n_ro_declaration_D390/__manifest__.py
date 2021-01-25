# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Romania - D390 ANAF Declaration",
    "summary": "Romania - D390 ANAF Declaration",
    "version": "14.0.1.0.0",
    "development_status": "Mature",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-romania",
    "author": "NextERP Romania," "Odoo Community Association (OCA)",
    "maintainers": ["feketemihai"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_ro_declaration","l10n_ro_stock_account"],
    "data": [
        "data/anaf_d390.xml",
        "security/ir.model.access.csv",
        "views/stock_picking_view.xml",
        "views/d390_declaration_view.xml",
    ],
}
