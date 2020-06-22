# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2018 Dorin Hongu <dhongu(@)gmail(.)com
# Copyright (C) 2019 OdooERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    usage = fields.Selection(selection_add=[('in_custody', 'In Custody'),
                                            ('usage_giving', 'Usage Giving'),
                                            ('consume', 'Consume')],

                             help="""* Supplier Location: Virtual location representing the source location for products coming from your suppliers
                       \n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products
                       \n* Internal Location: Physical locations inside your own warehouses,
                       \n* Customer Location: Virtual location representing the destination location for products sent to your customers
                       \n* Inventory: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)
                       \n* Procurement: Virtual location serving as temporary counterpart for procurement operations when the source (supplier or production) is not known yet. This location should be empty when the procurement scheduler has finished running.
                       \n* Production: Virtual counterpart location for production operations: this location consumes the raw material and produces finished products
                       \n* Transit Location: Counterpart location that should be used in inter-companies or inter-warehouses operations
                       \n* In Custody: Virtual location for products received in custody
                       \n* Usage Giving: Virtual location for products given in usage
                       \n* In Custody: Virtual location for products consumed beside production.
                      """, index=True,
                    ondelete={'in_custody':  lambda recs: recs.write({'usage': 'internal', 'active': False}),
                              'usage_giving':  lambda recs: recs.write({'usage': 'internal', 'active': False}),
                              'consume':  lambda recs: recs.write({'usage': 'internal', 'active': False}) },
                      )

    merchandise_type = fields.Selection(
        [("store", _("Store")), ("warehouse", _("Warehouse"))],
        string="Merchandise type",
        default="warehouse",
        help="Store represent a location where we keep the inventory at list price https://www.contzilla.ro/monografii-contabile-pentru-activitatea-unui-magazin-comert-cu-amanuntul/"
    )
