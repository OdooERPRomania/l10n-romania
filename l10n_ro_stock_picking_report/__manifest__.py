# -*- coding: utf-8 -*-
# ©  2008-2019 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

{
    "name": "Romania - Picking Reports",
    "version": "1.0",
    "author": "Dorin Hongu",
    "website": "",

    "description": """

Romania - Picking Report layout
------------------------------------------
 - Reports for Reception, Delivery and Internal Transfer
 - Referinta din comanda de achizitie este copiata in NIR si factura

    """,

    "category": "Localization",
    "depends": [
        "base",
        "stock",
        'l10n_ro_config',

        'purchase',

        #'l10n_ro_stock_account'
    ],

    "data": [
        'views/l10n_ro_stock_picking_report.xml',
        'report/report_picking.xml',
        'views/stock_picking_view.xml'

    ],
    "active": False,
    "installable": True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
