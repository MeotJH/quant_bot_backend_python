from dataclasses import dataclass

@dataclass
class Stock:
    symbol: str
    name: str
    lastsale: str
    netchange: str
    pctchange: str
    volume: str
    market_cap: str
    country: str
    ipo_year: str
    industry: str
    sector: str
    url: str

    def __init__(self, stock):
        self.symbol = stock.get('symbol', None)
        self.name = stock.get('name', None)
        self.lastsale = stock.get('lastsale', None)
        self.netchange = stock.get('netchange', None)
        self.pctchange = stock.get('pctchange', None)
        self.volume = stock.get('volume', None)
        self.market_cap = stock.get('marketCap', '0')
        self.country = stock.get('country', None)
        self.ipo_year = stock.get('ipoyear', None)
        self.industry = stock.get('industry', None)
        self.sector = stock.get('sector', None)
        self.url = stock.get('url', None)