# ©  2020 Forest and Biomass Romania
# See README.rst file on addons root folder for license details

from odoo import fields, models


class IRSequence(models.Model):
    _inherit = "ir.sequence"

    number_first = fields.Integer("Serie First Number")
    number_last = fields.Integer("Serie Last Number")


class IrSequenceDateRange(models.Model):
    _inherit = "ir.sequence.date_range"

    number_first = fields.Integer("Serie First Number")
    number_last = fields.Integer("Serie Last Number")
