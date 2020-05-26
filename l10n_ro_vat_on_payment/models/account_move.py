# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 OdooERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"
    print('xxxx')

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        """ Check if invoice is with VAT on Payment.
            Romanian law specify that the VAT on payment is applied only
            for internal invoices (National or not specified fiscal position)
        """
        result = super(AccountMove, self)._onchange_partner_id()
        fp_model = self.env["account.fiscal.position"]
        vatp = False
        ctx = dict(self._context)
        company = self.company_id
        partner = (
            self.env["res.partner"]._find_accounting_partner(self.partner_id)
            or self.partner_id
        )
        if self.invoice_date:
            ctx.update({"check_date": self.invoice_date})
        if "out" in self.move_type:
            vatp = company.partner_id.with_context(ctx)._check_vat_on_payment()
        else:
            if partner:
                vatp = partner.with_context(ctx)._check_vat_on_payment()
        if vatp:
            fptvainc = fp_model.search([("name", "ilike", "Regim TVA la Incasare")])
            if fptvainc:
                self.fiscal_position_id = fptvainc
        return result
    
    @api.constrains('state')
    def _check_all_lines_wiht_exigibility_or_without(self):
        "if one line has vat on payment ( tax.tax_exigibility ='on_payment' <=> tax_exigible=False) all must be the same "
        for record in self:
            if record.is_invoice( include_receipts=True):
                exigibility = 0 
                for line in record.invoice_line_ids:
                    if line.display_type in ['line_section', 'line_note']:
                        continue
                    else:
                        if line.tax_exigible:
                            if exigibility<0:
                                raise ValidationError(f"At invoice_nr={record.name}, invoice_date={record.invoice_date}, invoice_partner={record.partner_id.name} you have lines with vat_on_payment and some lines without")
                            exigibility += 1
                        else:
                            if exigibility>0:
                                raise ValidationError(f"At invoice_nr={record.name}, invoice_date={record.invoice_date}, invoice_partner={record.partner_id.name} you have lines with vat_on_payment and some lines without")
                            exigibility -= 1
    
