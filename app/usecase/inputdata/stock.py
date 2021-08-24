from dataclasses import dataclass
from datetime import date
from typing import List

from app.domain.stock import *
from app.domain.analyze import *
from app.domain.invest import *

@dataclass
class CreateCandlestickInput:
    safe:         bool
    candlesticks: List[Candlestick]

@dataclass
class CreateTagInput:
    stocks: List[Stock]

@dataclass
class GetCandlesticksInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date

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
class CalcurateSmaInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date
    term:      int

@dataclass
class CalcurateWmaInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date
    term:      int

@dataclass
class CalcurateEmaInput:
    code:      str
    market:    str
    from_date: date
    to_date:   date
    term:      int

@dataclass
class GetRankingPriceInput:
    market:   str
    tags:     List[str]
    today:    date
    term:     int
    order:    RankingOrder
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class GetRankingVolumeInput:
    market:   str
    tags:     List[str]
    today:    date
    term:     int
    order:    RankingOrder
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class GetRankingRsInput:
    market:   str
    tags:     List[str]
    today:    date
    order:    RankingOrder
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class GetRankingDeviationInput:
    market:    str
    tags:      List[str]
    today:     date
    longterm:  int
    shortterm: int
    order:     RankingOrder
    limit:     int
    offset:    int
    cache:     bool = False
    cachekey:  str = ''

@dataclass
class GetTrendPriceInput:
    market:   str
    tags:     List[str]
    today:    date
    sorttype: TrendType
    margin:   int
    term:     int
    smaterm:  int
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class GetTrendVolumeInput:
    market:   str
    tags:     List[str]
    today:    date
    sorttype: TrendType
    margin:   int
    term:     int
    smaterm:  int
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class GetTrendMomentumInput:
    market:   str
    tags:     List[str]
    today:    date
    sorttype: TrendType
    margin:   int
    term:     int
    smaterm:  int
    limit:    int
    offset:   int
    cache:    bool = False
    cachekey: str = ''

@dataclass
class ReflectStocksplitInput:
    code:          str
    market:        str
    present_price: Decimal
    newer_price:   Decimal
    target_date:   date

@dataclass
class ClearCachedataInput:
    cachekey: str

@dataclass
class MultipleCachedataInput:
    cachekey: str
    coefficient:        Decimal
    additional_ranking: List[str]

@dataclass
class GetCachedataInput:
    cachekey: str
    limit:    int
    offset:   int

@dataclass
class GetAthInput:
    market:    str
    tags:      List[str]
    term:      int
    base_date: date

@dataclass
class GetAtlInput:
    market:    str
    tags:      List[str]
    term:      int
    base_date: date

@dataclass
class GetAverageAtrInput:
    code:   str
    market: str
    term:   int
    today:  date

@dataclass
class SimulateTradeRuleInput:
    rule_type:    InvestRuleType
    code:         str
    market:       str
    tags:         List[str]
    unit:         int
    losscut_rate: Decimal
    today:        date
    term:         int
    principal:    Decimal
    commission:   Commission

@dataclass
class PredictSetupSignalInput:
    rule_type: InvestRuleType
    code:      str
    market:    str
    tags:      List[str]
    today:     date

@dataclass
class DelistingStockInput:
    code:   str
    market: str

@dataclass
class ListingStockInput:
    code:   str
    market: str

@dataclass
class GetEachFirststickInput:
    order:  RankingOrder
    limit:  int
    offset: int

@dataclass
class GetEachLaststickInput:
    order:  RankingOrder
    limit:  int
    offset: int

@dataclass
class MakeCachetagInput:
    cachekey: str
    limit:    int
