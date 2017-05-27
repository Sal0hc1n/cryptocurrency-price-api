#!/bin/python3
import requests
import grequests

assets = ['USD', 'USDT', 'EUR', 'BTC', 'XRP', 'ETH', 'HKD', 'LTC', 'RUR']

#btce
def btc_e(assets):
    retval = []
    r = requests.get('https://btc-e.com/api/3/info').json()
    urls=[]
    pairs = []
    for k, v in r['pairs'].items():
        k1, k2 = k.upper().split("_")
        if k1 in assets and k2 in assets:
            pairs.append(k)
            urls.append('https://btc-e.com/api/3/ticker/' + k)
    rs = [grequests.get(u) for u in urls]
    for i in zip(pairs, grequests.map(rs)):
        r = i[1].json()
        k = i[0]
        k1, k2 = k.upper().split("_")
        retval.append({'from': k1,
                       'to': k2,
                       'bid': r[k]['buy'],
                       'ask': r[k]['sell']})
    return retval


def gatecoin(assets):
    retval = []
    r = requests.get('https://api.gatecoin.com/Public/LiveTickers').json()
    for k in r['tickers']:
        s = k['currencyPair']
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 in assets and k2 in assets:
            retval.append({'from': k1,
                           'to': k2,
                           'bid': k['bid'],
                           'ask': k['ask']})
    return retval

def poloniex(assets):
    """Poloniex assets"""
    retval = []
    r = requests.get('https://poloniex.com/public?command=returnTicker')
    d = r.json()
    for k, v in d.items():
        k1, k2 = k.split("_")
        if k1 in assets and k2 in assets:
            retval.append({'from': k1,
                           'to': k2,
                           'bid': v['highestBid'],
                           'ask': v['lowestAsk']})
    return retval

def bitfinex(assets):
    """Bitfinex assets"""
    retval = []
    urls = []
    pairs = []
    bitfinex_url = 'https://api.bitfinex.com/v1'
    symbols = requests.get(bitfinex_url + '/symbols').json()
    for s in symbols:
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 in assets or k2 in assets:
            pairs.append(s)
            urls.append(bitfinex_url + '/pubticker/' + s)
    rs = [grequests.get(u) for u in urls]
    for i in zip(symbols, grequests.map(rs)):
        r = i[1].json()
        k = i[0]
        k1 = k[0:3].upper()
        k2 = k[3:].upper()
        retval.append({'from': k1,
                       'to': k2,
                       'bid': r['bid'],
                       'ask': r['ask']})
    return retval

def bitstamp(assets):
    """Bitstamp assets"""
    retval = []
    bitstamp_url = 'https://www.bitstamp.net/api/v2/ticker/'
    for s in ['btcusd', 'btceur',
              'eurusd', 'xrpusd', 'xrpeur',
              'xrpbtc']:
        d = requests.get(bitstamp_url + s +"/").json()
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 not in assets or k2 not in assets:
            retval.append({'from': k1,
                           'to': k2,
                           'bid': d['bid'],
                           'ask': d['ask']})
    return retval
    
#add tag
def add_tag(d, tag):
    d['from'] = d['from'] + ":" + tag
    d['to'] = d['to'] + ":" + tag
    return d
 
for k,v in [
    ['bitfinex', bitfinex],
    ['btce', btc_e],
    ['gatecoin', gatecoin],
    ['poloniex', poloniex],
    ['bitstamp', bitstamp]
    ]:
    for j in v(assets):
        if j['from'] not in assets or j['to'] not in assets:
            continue
        j = add_tag(j,k)
        print(','.join([j['from'], j['to'], str(j['bid']), str(j['ask'])]))



#bitfinex

#bitstamp

#anx

