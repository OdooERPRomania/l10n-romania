# ©  2018 Terrabit
# See README.rst file on addons root folder for license details

from odoo import models


class RunDeclaration(models.TransientModel):
    _name = "l10n_ro.run.declaration"
    _inherit = "anaf.mixin"
    _description = "RunDeclaration"
