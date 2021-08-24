from dataclasses import dataclass
from typing import List
from datetime import date

from app.domain.stock import *

@dataclass
class FindInput:
    code:   str
    market: str
    date:   date

@dataclass
class FindTagInput:
    code:   str
    market: str

@dataclass
class SaveInput:
    candlestick: Candlestick

@dataclass
class SaveTagInput:
    stock: Stock

@dataclass
class GetInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date

@dataclass
class GetOnesAllInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date

@dataclass
class GetAllInput:
    market:    str
    tags:      List[str]
    from_date: date
    to_date:   date

@dataclass
class GetEachInput:
    market: str
    tags:   List[str]
    offset: int
    today:  date

@dataclass
class GetRangeInput:
    code:    str
    market:  str
    tags:    List[str]
    to_date: date
    limit:   str

@dataclass
class SearchTickersInput:
    keyword: str

@dataclass
class SearchMarketsInput:
    keyword: str

@dataclass
class SearchTagsInput:
    keyword: str

@dataclass
class GetStockdatainfoInput:
    code:   str
    market: str

@dataclass
class GetTickersInput:
    market: str

@dataclass
class SaveDelistingInput:
    delisting: Candlestick

@dataclass
class FindDelistingInput:
    code:   str
    market: str
    date:   date

@dataclass
class RemoveOnesAllInput:
    code:   str
    market: str

@dataclass
class GetDelistingsOnesAllInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date

@dataclass
class RemoveDelistingsOnesAllInput:
    code:   str
    market: str

@dataclass
class GetAllTermInput:
    pass

@dataclass
class RemoveTagInput:
    tagname: str
