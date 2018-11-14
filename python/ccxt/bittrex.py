# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import AddressPending
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import DECIMAL_PLACES


class bittrex (Exchange):

    def describe(self):
        return self.deep_extend(super(bittrex, self).describe(), {
            'id': 'bittrex',
            'name': 'Bittrex',
            'countries': ['US'],
            'version': 'v1.1',
            'rateLimit': 1500,
            'certified': True,
            # new metainfo interface
            'has': {
                'CORS': True,
                'createMarketOrder': False,
                'fetchDepositAddress': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': True,
                'fetchMyTrades': False,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchTickers': True,
                'withdraw': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': False,
            },
            'timeframes': {
                '1m': 'oneMin',
                '5m': 'fiveMin',
                '30m': 'thirtyMin',
                '1h': 'hour',
                '1d': 'day',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766352-cf0b3c26-5ed5-11e7-82b7-f3826b7a97d8.jpg',
                'api': {
                    'public': 'https://bittrex.com/api',
                    'account': 'https://bittrex.com/api',
                    'market': 'https://bittrex.com/api',
                    'v2': 'https://bittrex.com/api/v2.0/pub',
                },
                'www': 'https://bittrex.com',
                'doc': [
                    'https://bittrex.com/Home/Api',
                    'https://www.npmjs.org/package/node.bittrex.api',
                ],
                'fees': [
                    'https://bittrex.com/Fees',
                    'https://support.bittrex.com/hc/en-us/articles/115000199651-What-fees-does-Bittrex-charge-',
                ],
            },
            'api': {
                'v2': {
                    'get': [
                        'currencies/GetBTCPrice',
                        'market/GetTicks',
                        'market/GetLatestTick',
                        'Markets/GetMarketSummaries',
                        'market/GetLatestTick',
                    ],
                },
                'public': {
                    'get': [
                        'currencies',
                        'markethistory',
                        'markets',
                        'marketsummaries',
                        'marketsummary',
                        'orderbook',
                        'ticker',
                    ],
                },
                'account': {
                    'get': [
                        'balance',
                        'balances',
                        'depositaddress',
                        'deposithistory',
                        'order',
                        'orders',
                        'orderhistory',
                        'withdrawalhistory',
                        'withdraw',
                    ],
                },
                'market': {
                    'get': [
                        'buylimit',
                        'buymarket',
                        'cancel',
                        'openorders',
                        'selllimit',
                        'sellmarket',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.0025,
                    'taker': 0.0025,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.001,
                        'LTC': 0.01,
                        'DOGE': 2,
                        'VTC': 0.02,
                        'PPC': 0.02,
                        'FTC': 0.2,
                        'RDD': 2,
                        'NXT': 2,
                        'DASH': 0.002,
                        'POT': 0.002,
                    },
                    'deposit': {
                        'BTC': 0,
                        'LTC': 0,
                        'DOGE': 0,
                        'VTC': 0,
                        'PPC': 0,
                        'FTC': 0,
                        'RDD': 0,
                        'NXT': 0,
                        'DASH': 0,
                        'POT': 0,
                    },
                },
            },
            'exceptions': {
                # 'Call to Cancel was throttled. Try again in 60 seconds.': DDoSProtection,
                # 'Call to GetBalances was throttled. Try again in 60 seconds.': DDoSProtection,
                'APISIGN_NOT_PROVIDED': AuthenticationError,
                'INVALID_SIGNATURE': AuthenticationError,
                'INVALID_CURRENCY': ExchangeError,
                'INVALID_PERMISSION': AuthenticationError,
                'INSUFFICIENT_FUNDS': InsufficientFunds,
                'QUANTITY_NOT_PROVIDED': InvalidOrder,
                'MIN_TRADE_REQUIREMENT_NOT_MET': InvalidOrder,
                'ORDER_NOT_OPEN': OrderNotFound,
                'INVALID_ORDER': InvalidOrder,
                'UUID_INVALID': OrderNotFound,
                'RATE_NOT_PROVIDED': InvalidOrder,  # createLimitBuyOrder('ETH/BTC', 1, 0)
                'WHITELIST_VIOLATION_IP': PermissionDenied,
            },
            'options': {
                # price precision by quote currency code
                'pricePrecisionByCode': {
                    'USD': 3,
                },
                'parseOrderStatus': False,
                'hasAlreadyAuthenticatedSuccessfully': False,  # a workaround for APIKEY_INVALID
            },
            'commonCurrencies': {
                'BITS': 'SWIFT',
                'CPC': 'CapriCoin',
            },
        })

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, TRUNCATE, self.markets[symbol]['precision']['price'], DECIMAL_PLACES)

    def fee_to_precision(self, symbol, fee):
        return self.decimal_to_precision(fee, TRUNCATE, self.markets[symbol]['precision']['price'], DECIMAL_PLACES)

    def fetch_markets(self):
        response = self.v2GetMarketsGetMarketSummaries()
        result = []
        for i in range(0, len(response['result'])):
            market = response['result'][i]['Market']
            id = market['MarketName']
            baseId = market['MarketCurrency']
            quoteId = market['BaseCurrency']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            pricePrecision = 8
            if quote in self.options['pricePrecisionByCode']:
                pricePrecision = self.options['pricePrecisionByCode'][quote]
            precision = {
                'amount': 8,
                'price': pricePrecision,
            }
            active = market['IsActive'] or market['IsActive'] == 'true'
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': market['MinTradeSize'],
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                },
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.accountGetBalances(params)
        balances = response['result']
        result = {'info': balances}
        indexed = self.index_by(balances, 'Currency')
        keys = list(indexed.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            currency = self.common_currency_code(id)
            account = self.account()
            balance = indexed[id]
            free = float(balance['Available'])
            total = float(balance['Balance'])
            used = total - free
            account['free'] = free
            account['used'] = used
            account['total'] = total
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        response = self.publicGetOrderbook(self.extend({
            'market': self.market_id(symbol),
            'type': 'both',
        }, params))
        orderbook = response['result']
        if 'type' in params:
            if params['type'] == 'buy':
                orderbook = {
                    'buy': response['result'],
                    'sell': [],
                }
            elif params['type'] == 'sell':
                orderbook = {
                    'buy': [],
                    'sell': response['result'],
                }
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'Rate', 'Quantity')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_string(ticker, 'TimeStamp')
        if isinstance(timestamp, basestring):
            if len(timestamp) > 0:
                timestamp = self.parse8601(timestamp)
        symbol = None
        if market:
            symbol = market['symbol']
        previous = self.safe_float(ticker, 'PrevDay')
        last = self.safe_float(ticker, 'Last')
        change = None
        percentage = None
        if last is not None:
            if previous is not None:
                change = last - previous
                if previous > 0:
                    percentage = (change / previous) * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume'),
            'quoteVolume': self.safe_float(ticker, 'BaseVolume'),
            'info': ticker,
        }

    def fetch_currencies(self, params={}):
        response = self.publicGetCurrencies(params)
        currencies = response['result']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['Currency']
            # todo: will need to rethink the fees
            # to add support for multiple withdrawal/deposit methods and
            # differentiated fees for each particular method
            code = self.common_currency_code(id)
            precision = 8  # default precision, todo: fix "magic constants"
            address = self.safe_value(currency, 'BaseAddress')
            result[code] = {
                'id': id,
                'code': code,
                'address': address,
                'info': currency,
                'type': currency['CoinType'],
                'name': currency['CurrencyLong'],
                'active': currency['IsActive'],
                'fee': self.safe_float(currency, 'TxFee'),  # todo: redesign
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['TxFee'],
                        'max': math.pow(10, precision),
                    },
                },
            }
        return result

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetMarketsummaries(params)
        tickers = response['result']
        result = {}
        for t in range(0, len(tickers)):
            ticker = tickers[t]
            id = ticker['MarketName']
            market = None
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                symbol = self.parse_symbol(id)
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMarketsummary(self.extend({
            'market': market['id'],
        }, params))
        ticker = response['result'][0]
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['TimeStamp'] + '+00:00')
        side = None
        if trade['OrderType'] == 'BUY':
            side = 'buy'
        elif trade['OrderType'] == 'SELL':
            side = 'sell'
        id = None
        if 'Id' in trade:
            id = str(trade['Id'])
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': 'limit',
            'side': side,
            'price': self.safe_float(trade, 'Price'),
            'amount': self.safe_float(trade, 'Quantity'),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMarkethistory(self.extend({
            'market': market['id'],
        }, params))
        if 'result' in response:
            if response['result'] is not None:
                return self.parse_trades(response['result'], market, since, limit)
        raise ExchangeError(self.id + ' fetchTrades() returned None response')

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['T'] + '+00:00')
        return [
            timestamp,
            ohlcv['O'],
            ohlcv['H'],
            ohlcv['L'],
            ohlcv['C'],
            ohlcv['V'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'tickInterval': self.timeframes[timeframe],
            'marketName': market['id'],
        }
        response = self.v2GetMarketGetTicks(self.extend(request, params))
        if 'result' in response:
            if response['result']:
                return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        response = self.marketGetOpenorders(self.extend(request, params))
        orders = self.parse_orders(response['result'], market, since, limit)
        return self.filter_by_symbol(orders, symbol)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        method = 'marketGet' + self.capitalize(side) + type
        order = {
            'market': market['id'],
            'quantity': self.amount_to_precision(symbol, amount),
            'rate': self.price_to_precision(symbol, price),
        }
        # if type == 'limit':
        #     order['rate'] = self.price_to_precision(symbol, price)
        response = getattr(self, method)(self.extend(order, params))
        orderIdField = self.get_order_id_field()
        result = {
            'info': response,
            'id': response['result'][orderIdField],
            'symbol': symbol,
            'type': type,
            'side': side,
            'status': 'open',
        }
        return result

    def get_order_id_field(self):
        return 'uuid'

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        orderIdField = self.get_order_id_field()
        request = {}
        request[orderIdField] = id
        response = self.marketGetCancel(self.extend(request, params))
        return self.extend(self.parse_order(response), {
            'status': 'canceled',
        })

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        # https://support.bittrex.com/hc/en-us/articles/115003723911
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.accountGetDeposithistory(self.extend(request, params))
        #
        #     {success:    True,
        #       message:   "",
        #        result: [{           Id:  22578097,
        #                           Amount:  0.3,
        #                         Currency: "ETH",
        #                    Confirmations:  15,
        #                      LastUpdated: "2018-06-10T07:12:10.57",
        #                             TxId: "0xf50b5ba2ca5438b58f93516eaa523eaf35b4420ca0f24061003df1be7…",
        #                    CryptoAddress: "0xb25f281fa51f1635abd4a60b0870a62d2a7fa404"                    }]}
        #
        # we cannot filter by `since` timestamp, as it isn't set by Bittrex
        # see https://github.com/ccxt/ccxt/issues/4067
        # return self.parseTransactions(response['result'], currency, since, limit)
        return self.parseTransactions(response['result'], currency, None, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        # https://support.bittrex.com/hc/en-us/articles/115003723911
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.accountGetWithdrawalhistory(self.extend(request, params))
        #
        #     {
        #         "success" : True,
        #         "message" : "",
        #         "result" : [{
        #                 "PaymentUuid" : "b32c7a5c-90c6-4c6e-835c-e16df12708b1",
        #                 "Currency" : "BTC",
        #                 "Amount" : 17.00000000,
        #                 "Address" : "1DfaaFBdbB5nrHj87x3NHS4onvw1GPNyAu",
        #                 "Opened" : "2014-07-09T04:24:47.217",
        #                 "Authorized" : True,
        #                 "PendingPayment" : False,
        #                 "TxCost" : 0.00020000,
        #                 "TxId" : null,
        #                 "Canceled" : True,
        #                 "InvalidAddress" : False
        #             }, {
        #                 "PaymentUuid" : "d193da98-788c-4188-a8f9-8ec2c33fdfcf",
        #                 "Currency" : "XC",
        #                 "Amount" : 7513.75121715,
        #                 "Address" : "TcnSMgAd7EonF2Dgc4c9K14L12RBaW5S5J",
        #                 "Opened" : "2014-07-08T23:13:31.83",
        #                 "Authorized" : True,
        #                 "PendingPayment" : False,
        #                 "TxCost" : 0.00002000,
        #                 "TxId" : "d8a575c2a71c7e56d02ab8e26bb1ef0a2f6cf2094f6ca2116476a569c1e84f6e",
        #                 "Canceled" : False,
        #                 "InvalidAddress" : False
        #             }
        #         ]
        #     }
        #
        return self.parseTransactions(response['result'], currency, since, limit)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #      {           Id:  72578097,
        #               Amount:  0.3,
        #             Currency: "ETH",
        #        Confirmations:  15,
        #          LastUpdated: "2018-06-17T07:12:14.57",
        #                 TxId: "0xb31b5ba2ca5438b58f93516eaa523eaf35b4420ca0f24061003df1be7…",
        #        CryptoAddress: "0x2d5f281fa51f1635abd4a60b0870a62d2a7fa404"                    }
        #
        # fetchWithdrawals
        #
        #     {
        #         "PaymentUuid" : "e293da98-788c-4188-a8f9-8ec2c33fdfcf",
        #         "Currency" : "XC",
        #         "Amount" : 7513.75121715,
        #         "Address" : "EVnSMgAd7EonF2Dgc4c9K14L12RBaW5S5J",
        #         "Opened" : "2014-07-08T23:13:31.83",
        #         "Authorized" : True,
        #         "PendingPayment" : False,
        #         "TxCost" : 0.00002000,
        #         "TxId" : "b4a575c2a71c7e56d02ab8e26bb1ef0a2f6cf2094f6ca2116476a569c1e84f6e",
        #         "Canceled" : False,
        #         "InvalidAddress" : False
        #     }
        #
        id = self.safe_string_2(transaction, 'Id', 'PaymentUuid')
        amount = self.safe_float(transaction, 'Amount')
        address = self.safe_string_2(transaction, 'CryptoAddress', 'Address')
        txid = self.safe_string(transaction, 'TxId')
        updated = self.parse8601(self.safe_value(transaction, 'LastUpdated'))
        timestamp = self.parse8601(self.safe_string(transaction, 'Opened'), updated)
        type = 'withdrawal' if (timestamp is not None) else 'deposit'
        code = None
        currencyId = self.safe_string(transaction, 'Currency')
        currency = self.safe_value(self.currencies_by_id, currencyId)
        if currency is not None:
            code = currency['code']
        else:
            code = self.common_currency_code(currencyId)
        status = 'pending'
        if type == 'deposit':
            if currency is not None:
                # deposits numConfirmations never reach the minConfirmations number
                # we set all of them to 'ok', otherwise they'd all be 'pending'
                #
                #     numConfirmations = self.safe_integer(transaction, 'Confirmations', 0)
                #     minConfirmations = self.safe_integer(currency['info'], 'MinConfirmation')
                #     if numConfirmations >= minConfirmations:
                #         status = 'ok'
                #     }
                #
                status = 'ok'
        else:
            authorized = self.safe_value(transaction, 'Authorized', False)
            pendingPayment = self.safe_value(transaction, 'PendingPayment', False)
            canceled = self.safe_value(transaction, 'Canceled', False)
            invalidAddress = self.safe_value(transaction, 'InvalidAddress', False)
            if invalidAddress:
                status = 'failed'
            elif canceled:
                status = 'canceled'
            elif pendingPayment:
                status = 'pending'
            elif authorized and(txid is not None):
                status = 'ok'
        feeCost = self.safe_float(transaction, 'TxCost')
        if feeCost is None:
            if type == 'deposit':
                # according to https://support.bittrex.com/hc/en-us/articles/115000199651-What-fees-does-Bittrex-charge-
                feeCost = 0  # FIXME: remove hardcoded value that may change any time
            elif type == 'withdrawal':
                raise ExchangeError('Withdrawal without fee detectednot ')
        return {
            'info': transaction,
            'id': id,
            'currency': code,
            'amount': amount,
            'address': address,
            'tag': None,
            'status': status,
            'type': type,
            'updated': updated,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'fee': {
                'currency': code,
                'cost': feeCost,
            },
        }

    def parse_symbol(self, id):
        quote, base = id.split('-')
        base = self.common_currency_code(base)
        quote = self.common_currency_code(quote)
        return base + '/' + quote

    def parse_order(self, order, market=None):
        side = self.safe_string(order, 'OrderType')
        if side is None:
            side = self.safe_string(order, 'Type')
        isBuyOrder = (side == 'LIMIT_BUY') or (side == 'BUY')
        isSellOrder = (side == 'LIMIT_SELL') or (side == 'SELL')
        if isBuyOrder:
            side = 'buy'
        if isSellOrder:
            side = 'sell'
        # We parse different fields in a very specific order.
        # Order might well be closed and then canceled.
        status = None
        if ('Opened' in list(order.keys())) and order['Opened']:
            status = 'open'
        if ('Closed' in list(order.keys())) and order['Closed']:
            status = 'closed'
        if ('CancelInitiated' in list(order.keys())) and order['CancelInitiated']:
            status = 'canceled'
        if ('Status' in list(order.keys())) and self.options['parseOrderStatus']:
            status = self.parse_order_status(self.safe_string(order, 'Status'))
        symbol = None
        if 'Exchange' in order:
            marketId = order['Exchange']
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                symbol = self.parse_symbol(marketId)
        else:
            if market is not None:
                symbol = market['symbol']
        timestamp = None
        if 'Opened' in order:
            timestamp = self.parse8601(order['Opened'] + '+00:00')
        if 'Created' in order:
            timestamp = self.parse8601(order['Created'] + '+00:00')
        lastTradeTimestamp = None
        if ('TimeStamp' in list(order.keys())) and(order['TimeStamp'] is not None):
            lastTradeTimestamp = self.parse8601(order['TimeStamp'] + '+00:00')
        if ('Closed' in list(order.keys())) and(order['Closed'] is not None):
            lastTradeTimestamp = self.parse8601(order['Closed'] + '+00:00')
        if timestamp is None:
            timestamp = lastTradeTimestamp
        fee = None
        commission = None
        if 'Commission' in order:
            commission = 'Commission'
        elif 'CommissionPaid' in order:
            commission = 'CommissionPaid'
        if commission:
            fee = {
                'cost': float(order[commission]),
            }
            if market is not None:
                fee['currency'] = market['quote']
            elif symbol is not None:
                currencyIds = symbol.split('/')
                quoteCurrencyId = currencyIds[1]
                if quoteCurrencyId in self.currencies_by_id:
                    fee['currency'] = self.currencies_by_id[quoteCurrencyId]['code']
                else:
                    fee['currency'] = self.common_currency_code(quoteCurrencyId)
        price = self.safe_float(order, 'Limit')
        cost = self.safe_float(order, 'Price')
        amount = self.safe_float(order, 'Quantity')
        remaining = self.safe_float(order, 'QuantityRemaining')
        filled = None
        if amount is not None and remaining is not None:
            filled = amount - remaining
        if not cost:
            if price and filled:
                cost = price * filled
        if not price:
            if cost and filled:
                price = cost / filled
        average = self.safe_float(order, 'PricePerUnit')
        id = self.safe_string(order, 'OrderUuid')
        if id is None:
            id = self.safe_string(order, 'OrderId')
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }
        return result

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = None
        try:
            orderIdField = self.get_order_id_field()
            request = {}
            request[orderIdField] = id
            response = self.accountGetOrder(self.extend(request, params))
        except Exception as e:
            if self.last_json_response:
                message = self.safe_string(self.last_json_response, 'message')
                if message == 'UUID_INVALID':
                    raise OrderNotFound(self.id + ' fetchOrder() error: ' + self.last_http_response)
            raise e
        if not response['result']:
            raise OrderNotFound(self.id + ' order ' + id + ' not found')
        return self.parse_order(response['result'])

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        response = self.accountGetOrderhistory(self.extend(request, params))
        orders = self.parse_orders(response['result'], market, since, limit)
        if symbol is not None:
            return self.filter_by_symbol(orders, symbol)
        return orders

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.accountGetDepositaddress(self.extend({
            'currency': currency['id'],
        }, params))
        address = self.safe_string(response['result'], 'Address')
        message = self.safe_string(response, 'message')
        if not address or message == 'ADDRESS_GENERATING':
            raise AddressPending(self.id + ' the address for ' + code + ' is being generated(pending, not ready yet, retry again later)')
        tag = None
        if (code == 'XRP') or (code == 'XLM') or (code == 'LSK'):
            tag = address
            address = currency['address']
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'quantity': amount,
            'address': address,
        }
        if tag:
            request['paymentid'] = tag
        response = self.accountGetWithdraw(self.extend(request, params))
        id = None
        if 'result' in response:
            if 'uuid' in response['result']:
                id = response['result']['uuid']
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        if api != 'v2':
            url += self.version + '/'
        if api == 'public':
            url += api + '/' + method.lower() + path
            if params:
                url += '?' + self.urlencode(params)
        elif api == 'v2':
            url += path
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            url += api + '/'
            if ((api == 'account') and(path != 'withdraw')) or (path == 'openorders'):
                url += method.lower()
            request = {
                'apikey': self.apiKey,
            }
            disableNonce = self.safe_value(self.options, 'disableNonce')
            if (disableNonce is None) or not disableNonce:
                request['nonce'] = self.nonce()
            url += path + '?' + self.urlencode(self.extend(request, params))
            signature = self.hmac(self.encode(url), self.encode(self.secret), hashlib.sha512)
            headers = {'apisign': signature}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if body[0] == '{':
            response = json.loads(body)
            # {success: False, message: "message"}
            success = self.safe_value(response, 'success')
            if success is None:
                raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
            if isinstance(success, basestring):
                # bleutrade uses string instead of boolean
                success = True if (success == 'true') else False
            if not success:
                message = self.safe_string(response, 'message')
                feedback = self.id + ' ' + self.json(response)
                exceptions = self.exceptions
                if message == 'APIKEY_INVALID':
                    if self.options['hasAlreadyAuthenticatedSuccessfully']:
                        raise DDoSProtection(feedback)
                    else:
                        raise AuthenticationError(feedback)
                if message == 'DUST_TRADE_DISALLOWED_MIN_VALUE_50K_SAT':
                    raise InvalidOrder(self.id + ' order cost should be over 50k satoshi ' + self.json(response))
                if message == 'INVALID_ORDER':
                    # Bittrex will return an ambiguous INVALID_ORDER message
                    # upon canceling already-canceled and closed orders
                    # therefore self special case for cancelOrder
                    # url = 'https://bittrex.com/api/v1.1/market/cancel?apikey=API_KEY&uuid=ORDER_UUID'
                    cancel = 'cancel'
                    indexOfCancel = url.find(cancel)
                    if indexOfCancel >= 0:
                        parts = url.split('&')
                        orderId = None
                        for i in range(0, len(parts)):
                            part = parts[i]
                            keyValue = part.split('=')
                            if keyValue[0] == 'uuid':
                                orderId = keyValue[1]
                                break
                        if orderId is not None:
                            raise OrderNotFound(self.id + ' cancelOrder ' + orderId + ' ' + self.json(response))
                        else:
                            raise OrderNotFound(self.id + ' cancelOrder ' + self.json(response))
                if message in exceptions:
                    raise exceptions[message](feedback)
                if message is not None:
                    if message.find('throttled. Try again') >= 0:
                        raise DDoSProtection(feedback)
                    if message.find('problem') >= 0:
                        raise ExchangeNotAvailable(feedback)  # 'There was a problem processing your request.  If self problem persists, please contact...')
                raise ExchangeError(feedback)

    def append_timezone_parse8601(self, x):
        length = len(x)
        lastSymbol = x[length - 1]
        if (lastSymbol == 'Z') or (x.find('+') >= 0):
            return self.parse8601(x)
        return self.parse8601(x + 'Z')

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        # a workaround for APIKEY_INVALID
        if (api == 'account') or (api == 'market'):
            self.options['hasAlreadyAuthenticatedSuccessfully'] = True
        return response
