# ©  2018 Terrabit
# See README.rst file on addons root folder for license details

from odoo import fields, models


class RunDeclaration(models.TransientModel):
    _name = "l10n_ro.run.d300"
    _inherit = "anaf.mixin"
    _description = "RunDeclaration"

    nr_evid = fields.Char()
    succesor_id = fields.Many2one(
        "res.partner",
        string="Succesor",
        help="Declarație depusă potrivit art.90 alin.(4) din "
             "Legea nr.207/2015 privind Codul de procedură fiscală",
    )
    R28_2 = fields.Integer(string="R28_2", default=0)
    R35_2_old = fields.Integer(string="Previous R35_2", default=0)
    R42_2_old = fields.Integer(string="Previous R42_2", default=0)

    R36_2 = fields.Integer(string="R36_2", default=0)
    R39_2 = fields.Integer(string="R39_2", default=0)
    R43_2 = fields.Integer(string="R43_2", default=0)
    R44_2 = fields.Integer(string="R44_2", default=0)
