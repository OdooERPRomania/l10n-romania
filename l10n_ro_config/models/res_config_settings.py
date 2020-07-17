# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

from odoo import models, fields, api, tools
import os
import csv


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


#   in original invoice section near other currency update
    module_currency_rate_update_RO_BNR = fields.Boolean('Currency Rate Update BNR',
                                                 help='This allows you to manage the update of currency rate based on different provider, use BNR site.')

#others section
    module_l10n_ro_address_extended = fields.Boolean('Extended Address with staircase ..',
                                                         help='')
#accounting section
    module_l10n_ro_fiscal_validation = fields.Boolean('Partners Fiscal Validation',
                                                      help='This allows you to manage the vat subjected and vat on payment fields update:\n'
                                                           'For Romanian partners based on ANAF data and www.openapi.ro webservice.\n'
                                                           'For European partners based on VIES data.')
    module_l10n_ro_partner_create_by_vat = fields.Boolean('Create Partners by VAT',
                                                          help='This allows you to create partners based on VAT:\n'
                                                               'Romanian partners will be create based on Ministry of Finance / openapi.ro Webservices Datas\n'
                                                               'European partners will be create based on VIES Website Datas (for countries that allow). \n')
    module_l10n_ro_vat_on_payment = fields.Boolean('VAT_on_payment',
                                           help='This module will download data from ANAF site and when you give or receive a invoice will set fiscal position for VAT on payment')

    module_l10n_ro_account_report_journal = fields.Boolean('Account report journal (Sale Purchase report)',
                                           help='')
    module_l10n_ro_account_period_close = fields.Boolean('Romania Account Period Close',
                                                         help='This allows you to close accounts on periods based on templates: Income, Expense, VAT...')

    module_l10n_ro_partner_unique = fields.Boolean('Partners unique by Company, VAT, NRC',
                                                   help='This allows you to set unique partners by company, VAT and NRC.')

    module_l10n_ro_account_balance = fields.Boolean('Romanian account balance',
                                                   help='')
    property_customer_advance_account_id = fields.Many2one('account.account', related='company_id.property_customer_advance_account_id',readonly=False,)
    property_supplier_advance_account_id = fields.Many2one('account.account', related='company_id.property_supplier_advance_account_id',readonly=False,)

    property_undeductible_tax_account_id = fields.Many2one('account.account', related='company_id.property_undeductible_tax_account_id',readonly=False,)
    property_tax_cash_basis_journal_default_debit_account_id = fields.Many2one('account.account', related='company_id.property_tax_cash_basis_journal_default_debit_account_id',readonly=False,)

    
# here must be some company related fields for type of compnay to know what type of balance to use

    module_l10n_ro_currency_reevaluation = fields.Boolean('Currency Reevaluation',
                                                          help='This allows you to manage currency reevaluation of move lines recorded on foreign currency.\n'
                                                               'To evaluate you have to check the "Allow Reevaluation" field on accounts.')

#stock section
    use_anglo_saxon = fields.Boolean(string='Anglo-Saxon Accounting', related='company_id.anglo_saxon_accounting', readonly=True)
    module_l10n_ro_stock = fields.Boolean('Romanian Stock',
                                          help='Methods of usage giving and consumption')
    module_l10n_ro_stock_picking_report = fields.Boolean('Romanian Stock picking report', help="Romanian legal documents at picking")
    module_l10n_ro_stock_account = fields.Boolean('Romanian Stock Accounting',
                                                  help='This allows you to manage the Romanian adaptation for stock, including:\n'
                                                       'New stock accounts on location to allow moving entry in accounting based on the stock move.\n'
                                                       'The account entry will be generated from stock move instead of stock quant, link with the generated \n'
                                                       'account move lines on the picking\n'
                                                       'Inventory account move lines...')

    property_stock_usage_giving_account_id = fields.Many2one('account.account', related='company_id.property_stock_usage_giving_account_id',readonly=False,)
    property_stock_picking_payable_account_id = fields.Many2one('account.account', related='company_id.property_stock_picking_payable_account_id',readonly=False,)
    property_stock_picking_receivable_account_id = fields.Many2one('account.account', related='company_id.property_stock_picking_receivable_account_id',readonly=False,)
    property_stock_picking_custody_account_id = fields.Many2one('account.account', related='company_id.property_stock_picking_custody_account_id',readonly=False,)

    property_uneligible_tax_account_id = fields.Many2one('account.account', related='company_id.property_uneligible_tax_account_id',readonly=False,)
    property_stock_transfer_account_id = fields.Many2one('account.account', related='company_id.property_stock_transfer_account_id',readonly=False,)



#     module_account_storno = fields.Boolean('Storno Accounting',
#                                            help='This allows you to manage the storno behaviour in accounting.')

#     module_l10n_ro_account_bank_statement = fields.Boolean('Bank Statement Invoices',
#                                                            help='This allows you to manage imports in bank statement line of the invoices only.')
    module_l10n_ro_account_compensation_currency_update = fields.Boolean('Currency Difference on Compensations',
                                                                         help='This allows you to manage currency difference amounts on compensation.')
    module_l10n_ro_account_constrains = fields.Boolean('Account Constrains',
                                                       help='This will remove the constrains related to account journal, accounts with secondary currency.')
    module_l10n_ro_account_report = fields.Boolean('Romania Accounting Reports',
                                                   help='This allows you to print reports according to legislation like: Sale/Purchase Journals, Trial Balance, D394..\n')
    module_l10n_ro_account_voucher_cash = fields.Boolean('Voucher to Cash Statement',
                                                         help='This allows you to directly input in Cash Statement payments/receipts from Pay Invoice.')
    module_l10n_ro_account_voucher_currency_update = fields.Boolean('Currency Difference on Partial Payments/Receipts',
                                                                    help='This allows you to manage currency difference amounts on partial payments/receipts.')
    module_l10n_ro_asset = fields.Boolean('Romanian Asset',
                                          help='This allows you to manage the Romanian adaptation for assets, including:\n'
                                               'Split assets in fixed assets and services (financials).\n'
                                               'Fixed assets will be created / sold from stock moves, services assets from invoices,\n'
                                               'also include history of creation of the asset.\n'
                                               'Method of reevaluation of assets.'
                                               'Import of the Chart of Asset Categories according with the legislation')
    module_l10n_ro_invoice_line_not_deductible = fields.Boolean('Not Deductible Invoice Line',
                                                                help='This allows you to manage not deductible supplier invoice line.')
    module_l10n_ro_invoice_report = fields.Boolean('Invoice and Voucher Report',
                                                   help='This allows you to print invoice report based on romanian layout.\n'
                                                        'Invoice includes voucher if payment is on the same day.\n'
                                                        'Voucher report with amount in word')
    module_l10n_ro_siruta = fields.Boolean('Romanian Cities',
                                           help='This allows you to manage the Romanian Zones, States, Communes, Cities:\n'
                                                'The address fields will contain city, commune, state, zone, country, zip.')
    module_l10n_ro_stock_picking_report = fields.Boolean('Stock Picking Report',
                                                         help='This allows you to print Reports for Reception and Delivery')
    module_l10n_ro_zipcode = fields.Boolean('Romanian Zipcodes',
                                            help='This allows you to manage the Romanian zipcodes on addreses:\n'
                                                 'The address fields will be replaced by one location field including city, commune, state, zone, country, zip.')

    property_undeductible_account_id = fields.Many2one('account.account', related='company_id.property_undeductible_account_id',readonly=False,)
    property_asset_reevaluation_account_id = fields.Many2one('account.account', related='company_id.property_asset_reevaluation_account_id',readonly=False,)

    siruta_update = fields.Boolean('Update Siruta Data')


    def execute(self):
        self.ensure_one()
        res = super(ResConfigSettings, self).execute()
        data_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data')

        # Load SIRUTA datas if field is checked

        if self.siruta_update:
            # First check if module is installed
            installed = self.env['ir.module.module'].search(
                [('name', '=', 'l10n_ro_siruta'),
                 ('state', '=', 'installed')])
            if installed:
                path = data_dir + '/l10n_ro_siruta/'
                files = ['res.country.zone.csv',
                         'res.country.state.csv',
                         'res.country.commune.csv',
                         'res.country.city.csv']
                for file1 in files:
                    with tools.file_open(path + file1) as fp:
                        tools.convert_csv_import(self._cr,
                                                 'l10n_ro_config',
                                                 file1,
                                                 fp.read(),
                                                 {},
                                                 mode="init",
                                                 noupdate=True)

        return res