# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Romania - ANAF Declarations",
    "summary": "Romania - ANAF Declaration",
    "version": "14.0.1.0.0",
    "development_status": "Mature",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-romania",
    "author": "NextERP Romania," "Odoo Community Association (OCA)",
    "maintainers": ["feketemihai", "dhongu"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ["l10n_ro_declaration"],
    "data": [
        "data/anaf_d390.xml",
        "security/ir.model.access.csv",
        "views/d390_declaration_view.xml",
        "views/view_move_form.xml",
    ],
}
