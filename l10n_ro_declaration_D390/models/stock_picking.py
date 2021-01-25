# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

#gggg
    new_contact  = fields.Many2one(
        'res.partner', 'New Contact',
        check_company=True,
        help="The new partner to replace the first, the goods are sent to his earehouse"
        )

    date_transfer_new_contact = fields.Datetime('Date of Transfer',
                                help="Date at which the new partner replace the first")
