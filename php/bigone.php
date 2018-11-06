<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception as Exception; // a common import

class bigone extends Exchange {

    public function describe () {
        return array_replace_recursive (parent::describe (), array (
            'id' => 'bigone',
            'name' => 'BigONE',
            'countries' => array ( 'GB' ),
            'version' => 'v2',
            'has' => array (
                'fetchTickers' => true,
                'fetchOpenOrders' => true,
                'fetchMyTrades' => true,
                'fetchDepositAddress' => true,
                'withdraw' => true,
                'fetchOHLCV' => false,
                'createMarketOrder' => false,
            ),
            'urls' => array (
                'logo' => 'https://user-images.githubusercontent.com/1294454/42803606-27c2b5ec-89af-11e8-8d15-9c8c245e8b2c.jpg',
                'api' => array (
                    'public' => 'https://big.one/api/v2',
                    'private' => 'https://big.one/api/v2/viewer',
                ),
                'www' => 'https://big.one',
                'doc' => 'https://open.big.one/docs/api.html',
                'fees' => 'https://help.big.one/hc/en-us/articles/115001933374-BigONE-Fee-Policy',
                'referral' => 'https://b1.run/users/new?code=D3LLBVFT',
            ),
            'api' => array (
                'public' => array (
                    'get' => array (
                        'ping', // timestamp in nanoseconds
                        'markets',
                        'markets/{symbol}/depth',
                        'markets/{symbol}/trades',
                        'markets/{symbol}/ticker',
                        'orders',
                        'orders/{id}',
                        'tickers',
                        'trades',
                    ),
                ),
                'private' => array (
                    'get' => array (
                        'accounts',
                        'orders',
                        'orders/{order_id}',
                        'trades',
                        'withdrawals',
                        'deposits',
                    ),
                    'post' => array (
                        'orders',
                        'orders/{order_id}/cancel',
                        'orders/cancel_all',
                    ),
                ),
            ),
            'fees' => array (
                'trading' => array (
                    'maker' => 0.1 / 100,
                    'taker' => 0.1 / 100,
                ),
                'funding' => array (
                    // HARDCODING IS DEPRECATED THE FEES BELOW ARE TO BE REMOVED SOON
                    'withdraw' => array (
                        'BTC' => 0.002,
                        'ETH' => 0.01,
                        'EOS' => 0.01,
                        'ZEC' => 0.002,
                        'LTC' => 0.01,
                        'QTUM' => 0.01,
                        // 'INK' => 0.01 QTUM,
                        // 'BOT' => 0.01 QTUM,
                        'ETC' => 0.01,
                        'GAS' => 0.0,
                        'BTS' => 1.0,
                        'GXS' => 0.1,
                        'BITCNY' => 1.0,
                    ),
                ),
            ),
            'exceptions' => array (
                'codes' => array (
                    '401' => '\\ccxt\\AuthenticationError',
                    '10030' => '\\ccxt\\InvalidNonce', // array ("message":"invalid nonce, nonce should be a 19bits number","code":10030)
                ),
                'detail' => array (
                    'Internal server error' => '\\ccxt\\ExchangeNotAvailable',
                ),
            ),
        ));
    }

    public function fetch_markets () {
        $response = $this->publicGetMarkets ();
        $markets = $response['data'];
        $result = array ();
        $this->options['marketsByUuid'] = array ();
        for ($i = 0; $i < count ($markets); $i++) {
            //
            //      {       $uuid =>   "550b34db-696e-4434-a126-196f827d9172",
            //        quoteScale =>    3,
            //        quoteAsset => array (   $uuid => "17082d1c-0195-4fb6-8779-2cdbcb9eeb3c",
            //                      $symbol => "USDT",
            //                        name => "TetherUS"                              ),
            //              name =>   "BTC-USDT",
            //         baseScale =>    5,
            //         baseAsset => {   $uuid => "0df9c3c3-255a-46d7-ab82-dedae169fba9",
            //                      $symbol => "BTC",
            //                        name => "Bitcoin"                               }  } }
            //
            $market = $markets[$i];
            $id = $market['name'];
            $uuid = $market['uuid'];
            $baseId = $market['baseAsset']['symbol'];
            $quoteId = $market['quoteAsset']['symbol'];
            $base = $this->common_currency_code($baseId);
            $quote = $this->common_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
            $precision = array (
                'amount' => $market['baseScale'],
                'price' => $market['quoteScale'],
            );
            $entry = array (
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'active' => true,
                'precision' => $precision,
                'limits' => array (
                    'amount' => array (
                        'min' => pow (10, -$precision['amount']),
                        'max' => pow (10, $precision['amount']),
                    ),
                    'price' => array (
                        'min' => pow (10, -$precision['price']),
                        'max' => pow (10, $precision['price']),
                    ),
                    'cost' => array (
                        'min' => null,
                        'max' => null,
                    ),
                ),
                'info' => $market,
            );
            $this->options['marketsByUuid'][$uuid] = $entry;
            $result[] = $entry;
        }
        return $result;
    }

    public function parse_ticker ($ticker, $market = null) {
        //
        //     array (
        //         {
        //             "volume" => "190.4925000000000000",
        //             "open" => "0.0777371200000000",
        //             "market_uuid" => "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        //             "market_id" => "ETH-BTC",
        //             "low" => "0.0742925600000000",
        //             "high" => "0.0789150000000000",
        //             "daily_change_perc" => "-0.3789180767180466680525339760",
        //             "daily_change" => "-0.0002945600000000",
        //             "$close" => "0.0774425600000000", // last price
        //             "bid" => array (
        //                 "price" => "0.0764777900000000",
        //                 "amount" => "6.4248000000000000"
        //             ),
        //             "ask" => {
        //                 "price" => "0.0774425600000000",
        //                 "amount" => "1.1741000000000000"
        //             }
        //         }
        //     )
        //
        if ($market === null) {
            $marketId = $this->safe_string($ticker, 'market_id');
            if (is_array ($this->markets_by_id) && array_key_exists ($marketId, $this->markets_by_id)) {
                $market = $this->markets_by_id[$marketId];
            }
        }
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $timestamp = $this->milliseconds ();
        $close = $this->safe_float($ticker, 'close');
        return array (
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'high' => $this->safe_float($ticker, 'high'),
            'low' => $this->safe_float($ticker, 'low'),
            'bid' => $this->safe_float($ticker['bid'], 'price'),
            'bidVolume' => $this->safe_float($ticker['bid'], 'amount'),
            'ask' => $this->safe_float($ticker['ask'], 'price'),
            'askVolume' => $this->safe_float($ticker['ask'], 'amount'),
            'vwap' => null,
            'open' => $this->safe_float($ticker, 'open'),
            'close' => $close,
            'last' => $close,
            'previousClose' => null,
            'change' => $this->safe_float($ticker, 'daily_change'),
            'percentage' => $this->safe_float($ticker, 'daily_change_perc'),
            'average' => null,
            'baseVolume' => $this->safe_float($ticker, 'volume'),
            'quoteVolume' => null,
            'info' => $ticker,
        );
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $response = $this->publicGetMarketsSymbolTicker (array_merge (array (
            'symbol' => $market['id'],
        ), $params));
        return $this->parse_ticker($response['data'], $market);
    }

    public function fetch_tickers ($symbols = null, $params = array ()) {
        $this->load_markets();
        $response = $this->publicGetTickers ($params);
        $tickers = $response['data'];
        $result = array ();
        for ($i = 0; $i < count ($tickers); $i++) {
            $ticker = $this->parse_ticker($tickers[$i]);
            $symbol = $ticker['symbol'];
            $result[$symbol] = $ticker;
        }
        return $result;
    }

    public function fetch_order_book ($symbol, $limit = null, $params = array ()) {
        $this->load_markets();
        $response = $this->publicGetMarketsSymbolDepth (array_merge (array (
            'symbol' => $this->market_id($symbol),
        ), $params));
        return $this->parse_order_book($response['data'], null, 'bids', 'asks', 'price', 'amount');
    }

    public function parse_trade ($trade, $market = null) {
        //
        //     {   $node => array (  taker_side => "ASK",
        //                       $price => "0.0694071600000000",
        //                 market_uuid => "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        //                   market_id => "ETH-BTC",
        //                 inserted_at => "2018-07-14T09:22:06Z",
        //                          id => "19913306",
        //                      $amount => "0.8800000000000000"                    ),
        //       cursor =>   "Y3Vyc29yOnYxOjE5OTEzMzA2"                              }
        //
        $node = $trade['node'];
        $timestamp = $this->parse8601 ($node['inserted_at']);
        $price = $this->safe_float($node, 'price');
        $amount = $this->safe_float($node, 'amount');
        if ($market === null) {
            $marketId = $this->safe_string($node, 'market_id');
            if (is_array ($this->markets_by_id) && array_key_exists ($marketId, $this->markets_by_id)) {
                $market = $this->markets_by_id[$marketId];
            }
        }
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $cost = $this->cost_to_precision($symbol, $price * $amount);
        $side = null;
        if ($node['taker_side'] === 'ASK') {
            $side = 'sell';
        } else {
            $side = 'buy';
        }
        return array (
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $symbol,
            'id' => $this->safe_string($node, 'id'),
            'order' => null,
            'type' => 'limit',
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => floatval ($cost),
            'fee' => null,
            'info' => $trade,
        );
    }

    public function fetch_trades ($symbol, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'symbol' => $market['id'],
        );
        if ($limit !== null) {
            $request['first'] = $limit;
        }
        $response = $this->publicGetMarketsSymbolTrades (array_merge ($request, $params));
        //
        //     { data => { page_info => array (      start_cursor => "Y3Vyc29yOnYxOjE5OTEzMzA2",
        //                            has_previous_page =>  true,
        //                                has_next_page =>  false,
        //                                   end_cursor => "Y3Vyc29yOnYxOjIwMDU0NzIw"  ),
        //                   edges => [ array (   node => array (  taker_side => "ASK",
        //                                              price => "0.0694071600000000",
        //                                        market_uuid => "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        //                                          market_id => "ETH-BTC",
        //                                        inserted_at => "2018-07-14T09:22:06Z",
        //                                                 id => "19913306",
        //                                             amount => "0.8800000000000000"                    ),
        //                              cursor =>   "Y3Vyc29yOnYxOjE5OTEzMzA2"                              ),
        //                            array (   node => array (  taker_side => "ASK",
        //                                              price => "0.0694071600000000",
        //                                        market_uuid => "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        //                                          market_id => "ETH-BTC",
        //                                        inserted_at => "2018-07-14T09:22:07Z",
        //                                                 id => "19913307",
        //                                             amount => "0.3759000000000000"                    ),
        //                              cursor =>   "Y3Vyc29yOnYxOjE5OTEzMzA3"                              ),
        //                            array (   node => array (  taker_side => "ASK",
        //                                              price => "0.0694071600000000",
        //                                        market_uuid => "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        //                                          market_id => "ETH-BTC",
        //                                        inserted_at => "2018-07-14T09:22:08Z",
        //                                                 id => "19913321",
        //                                             amount => "0.2197000000000000"                    ),
        //                              cursor =>   "Y3Vyc29yOnYxOjE5OTEzMzIx"                              ),
        //
        return $this->parse_trades($response['data']['edges'], $market, $since, $limit);
    }

    public function fetch_balance ($params = array ()) {
        $this->load_markets();
        $response = $this->privateGetAccounts ($params);
        //
        //     { data => [ array ( locked_balance => "0",
        //                        $balance => "0",
        //                     asset_uuid => "04479958-d7bb-40e4-b153-48bd63f2f77f",
        //                       asset_id => "NKC"                                   ),
        //               array ( locked_balance => "0",
        //                        $balance => "0",
        //                     asset_uuid => "04c8da0e-44fd-4d71-aeb0-8f4d54a4a907",
        //                       asset_id => "UBTC"                                  ),
        //               array ( locked_balance => "0",
        //                        $balance => "0",
        //                     asset_uuid => "05bc0d34-4809-4a39-a3c8-3a1851c8d224",
        //                       asset_id => "READ"                                  ),
        //
        $result = array ( 'info' => $response );
        $balances = $response['data'];
        for ($i = 0; $i < count ($balances); $i++) {
            $balance = $balances[$i];
            $currencyId = $balance['asset_id'];
            $code = $this->common_currency_code($currencyId);
            if (is_array ($this->currencies_by_id) && array_key_exists ($currencyId, $this->currencies_by_id)) {
                $code = $this->currencies_by_id[$currencyId]['code'];
            }
            $total = $this->safe_float($balance, 'balance');
            $used = $this->safe_float($balance, 'locked_balance');
            $free = null;
            if ($total !== null && $used !== null) {
                $free = $total - $used;
            }
            $account = array (
                'free' => $free,
                'used' => $used,
                'total' => $total,
            );
            $result[$code] = $account;
        }
        return $this->parse_balance($result);
    }

    public function parse_order ($order, $market = null) {
        //
        //     {
        //       "$id" => 10,
        //       "market_uuid" => "d2185614-50c3-4588-b146-b8afe7534da6",
        //       "market_uuid" => "BTC-EOS", // not sure which one is correct
        //       "market_id" => "BTC-EOS",   // not sure which one is correct
        //       "$price" => "10.00",
        //       "$amount" => "10.00",
        //       "filled_amount" => "9.0",
        //       "avg_deal_price" => "12.0",
        //       "$side" => "ASK",
        //       "state" => "FILLED"
        //     }
        //
        $id = $this->safe_string($order, 'id');
        if ($market === null) {
            $marketId = $this->safe_string($order, 'market_id');
            if (is_array ($this->markets_by_id) && array_key_exists ($marketId, $this->markets_by_id)) {
                $market = $this->markets_by_id[$marketId];
            } else {
                $marketUuid = $this->safe_string($order, 'market_uuid');
                if (is_array ($this->options['marketsByUuid']) && array_key_exists ($marketUuid, $this->options['marketsByUuid'])) {
                    $market = $this->options['marketsByUuid'][$marketUuid];
                }
            }
        }
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $timestamp = $this->parse8601 ($this->safe_string($order, 'inserted_at'));
        $price = $this->safe_float($order, 'price');
        $amount = $this->safe_float($order, 'amount');
        $filled = $this->safe_float($order, 'filled_amount');
        $remaining = max (0, $amount - $filled);
        $status = $this->parse_order_status($this->safe_string($order, 'state'));
        $side = $this->safe_string($order, 'side');
        if ($side === 'BID') {
            $side = 'buy';
        } else {
            $side = 'sell';
        }
        return array (
            'id' => $id,
            'datetime' => $this->iso8601 ($timestamp),
            'timestamp' => $timestamp,
            'status' => $status,
            'symbol' => $symbol,
            'type' => null,
            'side' => $side,
            'price' => $price,
            'cost' => null,
            'amount' => $amount,
            'filled' => $filled,
            'remaining' => $remaining,
            'trades' => null,
            'fee' => null,
            'info' => $order,
        );
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $side = ($side === 'buy') ? 'BID' : 'ASK';
        $request = array (
            'market_id' => $market['id'], // $market uuid d2185614-50c3-4588-b146-b8afe7534da6, required
            'side' => $side, // $order $side one of "ASK"/"BID", required
            'amount' => $this->amount_to_precision($symbol, $amount), // $order $amount, string, required
            'price' => $this->price_to_precision($symbol, $price), // $order $price, string, required
        );
        $response = $this->privatePostOrders (array_merge ($request, $params));
        //
        //     {
        //       "data":
        //         {
        //           "id" => 10,
        //           "market_uuid" => "BTC-EOS",
        //           "$price" => "10.00",
        //           "$amount" => "10.00",
        //           "filled_amount" => "9.0",
        //           "avg_deal_price" => "12.0",
        //           "$side" => "ASK",
        //           "state" => "FILLED"
        //         }
        //     }
        //
        $order = $this->safe_value($response, 'data');
        return $this->parse_order($order, $market);
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $request = array ( 'order_id' => $id );
        $response = $this->privatePostOrdersOrderIdCancel (array_merge ($request, $params));
        //
        //     {
        //       "data":
        //         {
        //           "$id" => 10,
        //           "market_uuid" => "BTC-EOS",
        //           "price" => "10.00",
        //           "amount" => "10.00",
        //           "filled_amount" => "9.0",
        //           "avg_deal_price" => "12.0",
        //           "side" => "ASK",
        //           "state" => "FILLED"
        //         }
        //     }
        //
        $order = $response['data'];
        return $this->parse_order($order);
    }

    public function cancel_all_orders ($symbols = null, $params = array ()) {
        $this->load_markets();
        $response = $this->privatePostOrdersOrderIdCancel ($params);
        //
        //     array (
        //         array (
        //             "id" => 10,
        //             "market_uuid" => "d2185614-50c3-4588-b146-b8afe7534da6",
        //             "price" => "10.00",
        //             "amount" => "10.00",
        //             "filled_amount" => "9.0",
        //             "avg_deal_price" => "12.0",
        //             "side" => "ASK",
        //             "state" => "FILLED"
        //         ),
        //         array (
        //             ...
        //         ),
        //     )
        //
        return $this->parse_orders($response);
    }

    public function fetch_order ($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $request = array ( 'order_id' => $id );
        $response = $this->privateGetOrdersOrderId (array_merge ($request, $params));
        //
        //     {
        //       "data":
        //         {
        //           "$id" => 10,
        //           "market_uuid" => "BTC-EOS",
        //           "price" => "10.00",
        //           "amount" => "10.00",
        //           "filled_amount" => "9.0",
        //           "avg_deal_price" => "12.0",
        //           "side" => "ASK",
        //           "state" => "FILLED"
        //         }
        //     }
        //
        $order = $this->safe_value($response, 'data');
        return $this->parse_order($order);
    }

    public function fetch_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        // NAME      DESCRIPTION                                           EXAMPLE         REQUIRED
        // market_id $market id                                             ETH-BTC         true
        // after     ask for the server to return $orders after the cursor  dGVzdGN1cmVzZQo false
        // before    ask for the server to return $orders before the cursor dGVzdGN1cmVzZQo false
        // first     slicing count                                         20              false
        // last      slicing count                                         20              false
        // side      order side one of                                     "ASK"/"BID"     false
        // state     order state one of                      "CANCELED"/"FILLED"/"PENDING" false
        if ($symbol === null) {
            throw new ArgumentsRequired ($this->id . ' fetchOrders requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'market_id' => $market['id'],
        );
        if ($limit !== null) {
            $request['first'] = $limit;
        }
        $response = $this->privateGetOrders (array_merge ($request, $params));
        //
        //     {
        //          "$data" => {
        //              "edges" => array (
        //                  {
        //                      "node" => array (
        //                          "id" => 10,
        //                          "market_id" => "ETH-BTC",
        //                          "price" => "10.00",
        //                          "amount" => "10.00",
        //                          "filled_amount" => "9.0",
        //                          "avg_deal_price" => "12.0",
        //                          "side" => "ASK",
        //                          "state" => "FILLED"
        //                      ),
        //                      "cursor" => "dGVzdGN1cmVzZQo="
        //                  }
        //              ),
        //              "page_info" => {
        //                  "end_cursor" => "dGVzdGN1cmVzZQo=",
        //                  "start_cursor" => "dGVzdGN1cmVzZQo=",
        //                  "has_next_page" => true,
        //                  "has_previous_page" => false
        //              }
        //          }
        //     }
        //
        $data = $this->safe_value($response, 'data', array ());
        $orders = $this->safe_value($data, 'edges', array ());
        $result = array ();
        for ($i = 0; $i < count ($orders); $i++) {
            $result[] = $this->parse_order($orders[$i]['node'], $market);
        }
        return $this->filter_by_symbol_since_limit($result, $symbol, $since, $limit);
    }

    public function parse_order_status ($status) {
        $statuses = array (
            'PENDING' => 'open',
            'FILLED' => 'closed',
            'CANCELED' => 'canceled',
        );
        return $this->safe_string($statuses, $status);
    }

    public function fetch_open_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        return $this->fetch_orders($symbol, $since, $limit, array_merge (array (
            'state' => 'PENDING',
        ), $params));
    }

    public function fetch_closed_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        return $this->fetch_orders($symbol, $since, $limit, array_merge (array (
            'state' => 'FILLED',
        ), $params));
    }

    public function nonce () {
        return $this->microseconds () * 1000;
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $query = $this->omit ($params, $this->extract_params($path));
        $url = $this->urls['api'][$api] . '/' . $this->implode_params($path, $params);
        if ($api === 'public') {
            if ($query)
                $url .= '?' . $this->urlencode ($query);
        } else {
            $this->check_required_credentials();
            $nonce = $this->nonce ();
            $request = array (
                'type' => 'OpenAPI',
                'sub' => $this->apiKey,
                'nonce' => $nonce,
            );
            $jwt = $this->jwt ($request, $this->secret);
            $headers = array (
                'Authorization' => 'Bearer ' . $jwt,
            );
            if ($method === 'GET') {
                if ($query)
                    $url .= '?' . $this->urlencode ($query);
            } else if ($method === 'POST') {
                $headers['Content-Type'] = 'application/json';
                $body = $this->json ($query);
            }
        }
        return array ( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function handle_errors ($httpCode, $reason, $url, $method, $headers, $body) {
        if (gettype ($body) !== 'string')
            return; // fallback to default $error handler
        if (strlen ($body) < 2)
            return; // fallback to default $error handler
        if (($body[0] === '{') || ($body[0] === '[')) {
            $response = json_decode ($body, $as_associative_array = true);
            //
            //      array ("$errors":{"detail":"Internal server $error")}
            //      array ("$errors":[{"message":"invalid nonce, nonce should be a 19bits number","$code":10030)],"$data":null}
            //
            $error = $this->safe_value($response, 'error');
            $errors = $this->safe_value($response, 'errors');
            $data = $this->safe_value($response, 'data');
            if ($error !== null || $errors !== null || $data === null) {
                $feedback = $this->id . ' ' . $this->json ($response);
                $code = null;
                if ($error !== null) {
                    $code = $this->safe_integer($error, 'code');
                }
                $exceptions = $this->exceptions['codes'];
                if ($errors !== null) {
                    if (gettype ($errors) === 'array' && count (array_filter (array_keys ($errors), 'is_string')) == 0) {
                        $code = $this->safe_string($errors[0], 'code');
                    } else {
                        $code = $this->safe_string($errors, 'detail');
                        $exceptions = $this->exceptions['detail'];
                    }
                }
                if (is_array ($exceptions) && array_key_exists ($code, $exceptions)) {
                    throw new $exceptions[$code] ($feedback);
                } else {
                    throw new ExchangeError ($feedback);
                }
            }
        }
    }
}
