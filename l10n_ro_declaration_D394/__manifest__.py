# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Romania - D394 ANAF Declarations",
    "summary": "Romania - D394 ANAF Declarations",
    "version": "14.0.1.0.0",
    "development_status": "Mature",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-romania",
    "author": "NextERP Romania," "Odoo Community Association (OCA)",
    "maintainers": ["feketemihai"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ["l10n_ro_declaration"],
    "data": [
        "data/anaf_d394.xml",
        "security/ir.model.access.csv",
        "views/d394_declaration_view.xml",
    ],
}
