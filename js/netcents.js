'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
const { InsufficientFunds, ArgumentsRequired, OrderNotFound, PermissionDenied, AuthenticationError, ExchangeNotAvailable } = require ('./base/errors');

//  ---------------------------------------------------------------------------

module.exports = class netcents extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'netcents',
            'name': 'NetCents',
            'countries': [ 'CA' ],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'CORS': true,
                'fetchTickers': true,
                'fetchMyTrades': true,
                'fetchOrder': true,
                'fetchOrders': true,
                'fetchOpenOrders': true,
            },
            'urls': {
                'logo': 'https://careers.net-cents.com/wp-content/uploads/2018/03/Netcents-LogoCorporate_Color-1.png',
                'api': 'https://serve.net-cents.com',
                'www': 'https://net-cents.com',
                'doc': 'https://developers.net-cents.com/exchange',
            },
            'api': {
                'public': {
                    'get': [
                        'markets', // Get all available markets
                        'order_book', // Get the order book of specified market
                        'order_book/{market}',
                        'tickers', // Get ticker of all markets
                        'tickers/{market}', // Get ticker of specific market
                        'timestamp', // Get server current time, in seconds since Unix epoch
                        'trade_history', // Get recent trades on market, each trade is included only once
                        'trade_history/{market}',
                        'currencies',
                    ],
                },
                'private': {
                    'get': [
                        'balances', // Get balances
                        'orders', // Get your orders, results is paginated
                        'order', // Get information of specified order
                        'trades', // Get your executed trades
                    ],
                    'post': [
                        'orders', // Create a Sell/Buy order
                        'orders/multi', // Create multiple sell/buy orders
                        'orders/clear', // Cancel all my orders
                        'order/delete', // Cancel an order
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': false,
                    'percentage': true,
                    'maker': 0.25 / 100,
                    'taker': 0.25 / 100,
                },
                'funding': {
                    'tierBased': false,
                    'percentage': false,
                    'withdraw': {},
                },
            },
            'exceptions': {
                '1001': OrderNotFound,
                '2002': InsufficientFunds,
                '2003': OrderNotFound,
                '2004': OrderNotFound,
                '2005': AuthenticationError,
                '2006': AuthenticationError,
                '2007': AuthenticationError,
                '2008': AuthenticationError,
                '2011': PermissionDenied,
                '2012': AuthenticationError,
                '3001': ExchangeNotAvailable,
            },
        });
    }

    async fetchMarkets () {
        let markets = await this.publicGetMarkets ();
        let result = [];
        for (let p = 0; p < markets.length; p++) {
            let market = markets[p];
            let id = market['id'];
            let baseId = this.safeString (market, 'base_unit');
            let quoteId = this.safeString (market, 'quote_unit');
            let base = baseId.toUpperCase ();
            let quote = quoteId.toUpperCase ();
            let symbol = base + '/' + quote;
            base = this.commonCurrencyCode (base);
            quote = this.commonCurrencyCode (quote);
            // todo: find out their undocumented precision and limits
            let precision = {
                'amount': this.safeFloat (market, 'quote_precision'),
                'price': this.safeFloat (market, 'base_precision'),
            };
            result.push ({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'info': market,
            });
        }
        return result;
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        let response = await this.privateGetBalances ();
        let result = { 'info': response };
        for (let b = 0; b < response.length; b++) {
            let balance = response[b];
            let currency = balance['currency'];
            let uppercase = currency.toUpperCase ();
            let account = {
                'free': parseFloat (balance['balance']),
                'used': parseFloat (balance['locked']),
                'total': 0.0,
            };
            account['total'] = this.sum (account['free'], account['used']);
            result[uppercase] = account;
        }
        return this.parseBalance (result);
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        await this.loadMarkets ();
        let market = this.market (symbol);
        let request = {
            'market': market['id'],
        };
        if (limit !== undefined)
            request['limit'] = limit; // default = 50
        let orderbook = await this.publicGetOrderBook (this.extend (request, params));
        let timestamp = orderbook['timestamp'] * 1000;
        return this.parseOrderBook (orderbook, timestamp);
    }

    parseTicker (ticker, market = undefined) {
        let timestamp = ticker['at'] * 1000;
        ticker = ticker['ticker'];
        let symbol = undefined;
        if (market)
            symbol = market['symbol'];
        let last = this.safeFloat (ticker, 'last');
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'high': this.safeFloat (ticker, 'high'),
            'low': this.safeFloat (ticker, 'low'),
            'bid': this.safeFloat (ticker, 'buy'),
            'bidVolume': undefined,
            'ask': this.safeFloat (ticker, 'sell'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': this.safeFloat (ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': undefined,
            'percentage': undefined,
            'average': undefined,
            'baseVolume': this.safeFloat (ticker, 'vol'),
            'quoteVolume': undefined,
            'info': ticker,
        };
    }

    async fetchTickers (symbols = undefined, params = {}) {
        await this.loadMarkets ();
        let tickers = await this.publicGetTickers (params);
        let ids = Object.keys (tickers);
        let result = {};
        for (let i = 0; i < ids.length; i++) {
            let id = ids[i];
            let market = undefined;
            let symbol = id;
            if (id in this.markets_by_id) {
                market = this.markets_by_id[id];
                symbol = market['symbol'];
            } else {
                let base = id.slice (0, 3);
                let quote = id.slice (3, 6);
                base = base.toUpperCase ();
                quote = quote.toUpperCase ();
                base = this.commonCurrencyCode (base);
                quote = this.commonCurrencyCode (quote);
                symbol = base + '/' + quote;
            }
            let ticker = tickers[id];
            result[symbol] = this.parseTicker (ticker, market);
        }
        return result;
    }

    async fetchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        let market = this.market (symbol);
        let response = await this.publicGetTickersMarket (this.extend ({
            'market': market['id'],
        }, params));
        return this.parseTicker (response, market);
    }

    parseTrade (trade, market = undefined) {
        let timestamp = this.parse8601 (trade['created_at']);
        return {
            'id': trade['id'].toString (),
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': this.safeString (market, 'symbol'),
            'type': undefined,
            'side': undefined,
            'price': this.safeFloat (trade, 'price'),
            'amount': this.safeFloat (trade, 'volume'),
            'cost': this.safeFloat (trade, 'funds'),
            'info': trade,
        };
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        let market = this.market (symbol);
        let response = await this.publicGetTradeHistory (this.extend ({
            'market': market['id'],
        }, params));
        return this.parseTrades (response, market, since, limit);
    }

    parseOrder (order, market = undefined) {
        let symbol = undefined;
        if (market !== undefined) {
            symbol = market['symbol'];
        } else {
            let marketId = order['market'];
            symbol = this.markets_by_id[marketId]['symbol'];
        }
        let timestamp = this.parse8601 (order['created_at']);
        let state = order['state'];
        let status = undefined;
        if (state === 'done') {
            status = 'closed';
        } else if (state === 'wait') {
            status = 'open';
        } else if (state === 'cancel') {
            status = 'canceled';
        }
        let trades = this.parseTrades (order['trades']);
        return {
            'id': order['id'].toString (),
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'lastTradeTimestamp': undefined,
            'status': status,
            'symbol': symbol,
            'type': order['ord_type'],
            'side': order['side'],
            'price': this.safeFloat (order, 'price'),
            'amount': this.safeFloat (order, 'volume'),
            'filled': this.safeFloat (order, 'executed_volume'),
            'remaining': this.safeFloat (order, 'remaining_volume'),
            'trades': trades,
            'fee': undefined,
            'info': order,
        };
    }

    async fetchOrder (id, symbol = undefined, params = {}) {
        await this.loadMarkets ();
        let response = await this.privateGetOrder (this.extend ({
            'id': parseInt (id),
        }, params));
        return this.parseOrder (response);
    }

    async fetchOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        if (symbol === undefined)
            throw new ArgumentsRequired (this.id + ' fetchOrders requires a symbol argument');
        await this.loadMarkets ();
        let market = this.market (symbol);
        let request = { 'market': market['id'] };
        if (limit !== undefined)
            request['limit'] = limit;
        let response = await this.privateGetOrders (this.extend (request, params));
        return this.parseOrders (response);
    }

    async fetchOpenOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        if (symbol === undefined)
            throw new ArgumentsRequired (this.id + ' fetchOpenOrders requires a symbol argument');
        await this.loadMarkets ();
        let request = { 'state': 'wait' };
        return this.fetchOrders (symbol, since, limit, this.extend (request, params));
    }

    async createOrder (symbol, type, side, amount, price = undefined, params = {}) {
        await this.loadMarkets ();
        let order = {
            'market': this.marketId (symbol),
            'side': side,
            'volume': amount.toString (),
            'ord_type': type,
        };
        if (type === 'limit') {
            order['price'] = price.toString ();
        }
        let response = await this.privatePostOrders (this.extend (order, params));
        let market = this.markets_by_id[response['market']];
        return this.parseOrder (response, market);
    }

    async cancelOrder (id, symbol = undefined, params = {}) {
        await this.loadMarkets ();
        let result = await this.privatePostOrderDelete ({ 'id': id });
        let order = this.parseOrder (result);
        let status = order['status'];
        if (status === 'closed' || status === 'canceled') {
            throw new OrderNotFound (this.id + ' ' + this.json (order));
        }
        return order;
    }

    async fetchMyTrades (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        if (symbol === undefined)
            throw new ArgumentsRequired (this.id + ' fetchMyTrades requires a symbol argument');
        await this.loadMarkets ();
        let market = this.market (symbol);
        let request = {
            'market': market['id'],
        };
        if (limit !== undefined)
            request['limit'] = limit;
        let response = await this.privateGetTrades (this.extend (request, params));
        return this.parseTrades (response, market, since, limit);
    }

    nonce () {
        return this.milliseconds ();
    }

    rawencodeParams (params) {
        // for privatePostOrdersMulti, should result in below string for each order in array:
        // orders[][ord_type]=limit&orders[][price]=5000&orders[][side]=buy&orders[][volume]=0.5
        if ('orders' in params) {
            let orders = params['orders'];
            let query = this.rawencode (this.keysort (this.omit (params, 'orders')));
            for (let i = 0; i < orders.length; i++) {
                let order = this.keysort (orders[i]);
                let keys = Object.keys (order);
                for (let k = 0; k < keys.length; k++) {
                    let key = keys[k];
                    let value = order[key];
                    query += '&orders[][' + key + ']=' + value.toString ();
                }
            }
            return query;
        }
        return this.rawencode (this.keysort (params));
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let request = '/api' + '/' + this.version + '/' + this.implodeParams (path, params);
        if ('extension' in this.urls)
            request += this.urls['extension'];
        let query = this.omit (params, this.extractParams (path));
        let url = this.urls['api'] + request;
        if (api === 'public') {
            if (Object.keys (query).length) {
                url += '?' + this.urlencode (query);
            }
        } else {
            this.checkRequiredCredentials ();
            let nonce = this.nonce ().toString ();
            params = this.extend ({
                'access_key': this.apiKey,
                'nonce': nonce,
            }, params);
            let query = this.rawencodeParams (params);
            let auth = method + '|' + request + '|' + query;
            let signed = this.hmac (this.encode (auth), this.encode (this.secret));
            let suffix = query + '&signature=' + signed;
            if (method === 'GET') {
                url += '?' + suffix;
            } else {
                body = this.json (this.extend (params, { 'signature': signed }));
                headers = { 'Content-Type': 'application/json' };
            }
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }

    handleErrors (code, reason, url, method, headers, body) {
        if (code === 400) {
            const response = JSON.parse (body);
            const error = this.safeValue (response, 'error');
            const errorCode = this.safeString (error, 'code');
            const feedback = this.id + ' ' + this.json (response);
            const exceptions = this.exceptions;
            if (errorCode in exceptions) {
                throw new exceptions[errorCode] (feedback);
            }
            // fallback to default error handler
        }
    }
};
