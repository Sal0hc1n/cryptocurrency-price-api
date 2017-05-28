from exchanges.base import Exchange

class Poloniex(Exchange):

    TICKER_URL = 'https://poloniex.com/public?command=returnTicker'
    SUPPORTED_UNDERLYINGS = ['BTCUSD', 'ETHBTC', 'XRPBTC']
    UNDERLYING_DICT = {
        'BTCUSD' : 'USDT_BTC',
        'ETHBTC' : 'BTC_ETH',
        'XRPBTC' : 'BTC_XRP'
    }
    QUOTE_DICT = {
        'bid' : 'highestBid',
        'ask' : 'lowestAsk',
        'last' : 'last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.UNDERLYING_DICT[underlying]).get(cls.QUOTE_DICT[quote])
