# Copyright (C) 2018 Terrabit
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Romania - D300 ANAF Declarations",
    "summary": "Romania - D300 ANAF Declaration",
    "version": "13.0.1.0.0",
    "development_status": "Mature",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-romania",
    "author": "NextERP Romania," "Terrabit," "Odoo Community Association (OCA)",
    "maintainers": ["feketemihai", "dhongu"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_ro_declaration"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/run_declaration_view.xml"
    ],
}
