from collections import defaultdict
from datetime import date, timedelta
from urllib.request import urlopen
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCurrencyRateProviderBNR(models.Model):
    _inherit = 'res.currency.rate.provider'

    service = fields.Selection(
        selection_add=[('BNR', 'Romanian National Bank only api that gives only today rate')],
        ondelete={'BNR':'cascade'})

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != 'BNR':
            return super()._get_supported_currencies()  # pragma: no cover

        # List of currencies obrained from: https://www.bnr.ro/nbrfxrates.xml
        return ['AED', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK',
              'DKK', 'EGP', 'EUR', 'GBP', 'HRK', 'HUF', 'INR', 'JPY',
               'KRW', 'MDL', 'MXN', 'NOK', 'NZD', 'PLN', 'RSD', 'RUB', 
               'SEK', 'THB', 'TRY', 'UAH', 'USD', 'XAU', 'XDR', 'ZAR']

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != 'BNR':
            return super()._obtain_rates(base_currency, currencies, date_from,
                                         date_to)  # pragma: no cover

        # This provider only serves RON-to-??? exchange rates
        if base_currency != 'RON':  # pragma: no cover   will create a message
            raise UserError(_(
                'Romanian National Bank is suitable only for companies'
                ' with RON as base currency!'
            ))

        returned_content = defaultdict(dict)
        url = 'https://www.bnr.ro/nbrfxrates.xml'  # BNR has only today rates 
        with urlopen(url) as xmlfile:
            tree = etree.parse(xmlfile)
            root = tree.getroot()   
            body = root.find('{http://www.bnr.ro/xsd}Body')
            cube = body.find('{http://www.bnr.ro/xsd}Cube')
            date = fields.Date.from_string(cube.attrib['date'])
            for element in cube.getchildren():
                rate = float(element.text)
                currency = element.attrib.get('currency',False)
                multiplier = float(element.attrib.get('multiplier', 1))
                rate_multip = rate * multiplier 
                if currency in currencies: # we are doing this because we do not want to install also the inverse currency, 
                    returned_content[date][currency] = 1/rate_multip

        return returned_content

