from dataclasses import dataclass
from typing import List, Dict

from app.domain.stock import *

@dataclass
class FindOutput:
    candlestick: Candlestick

@dataclass
class FindTagOutput:
    tags: List[str]

@dataclass
class SaveOutput:
    pass

@dataclass
class SaveTagOutput:
    pass

@dataclass
class GetOutput:
    candlesticks: List[Candlestick]

@dataclass
class GetOnesAllOutput:
    candlesticks: List[Candlestick]

@dataclass
class GetAllOutput:
    candlesticks: Dict[str, List[Candlestick]]

@dataclass
class GetEachOutput:
    candlesticks: Dict[str, Candlestick]

@dataclass
class GetRangeOutput:
    candlesticks: Dict[str, Candlestick]

@dataclass
class SearchTickersOutput:
    @dataclass
    class Ticker:
        code:   str
        market: str

    tickers: List[Ticker]

@dataclass
class SearchMarketsOutput:
    markets: List[str]

@dataclass
class SearchTagsOutput:
    tags: List[str]

@dataclass
class GetStockdatainfoOutput:
    first_date:      date
    last_date:       date
    close_price_ath: Decimal
    close_price_atl: Decimal
    high_price_ath:  Decimal
    low_price_atl:   Decimal

@dataclass
class GetTickersOutput:
    @dataclass
    class Ticker:
        code:   str
        market: str

    tickers: List[Ticker]

@dataclass
class SaveDelistingOutput:
    pass

@dataclass
class FindDelistingOutput:
    delisting: Candlestick

@dataclass
class RemoveOnesAllOutput:
    pass

@dataclass
class GetDelistingsOnesAllOutput:
    delistings: List[Candlestick]

@dataclass
class RemoveDelistingsOnesAllOutput:
    pass

@dataclass
class GetAllTermOutput:
    terms: List[Term]

@dataclass
class RemoveTagOutput:
    pass
