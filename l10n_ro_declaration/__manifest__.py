# Copyright (C) 2018 Terrabit
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
    "application": False,
    "installable": True,
    "depends": ["date_range", "l10n_ro_vat_on_payment"],
    "data": [
        "data/res.country.state.csv",
        "data/anaf_product_code.xml",
        "views/anaf_declaration_menu.xml",
        "views/anaf_declaration_view.xml",
        "views/anaf_product_code_view.xml",
        "views/anaf_signature_view.xml",
        "views/product_view.xml",
        "security/ir.model.access.csv",
    ],
}
