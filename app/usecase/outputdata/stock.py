from dataclasses import dataclass
from datetime import date
from typing import List, Dict

from app.domain.stock import *
from app.domain.analyze import *
from app.domain.simulator import *

@dataclass
class CreateCandlestickOutput:
    pass

@dataclass
class CreateTagOutput:
    pass

@dataclass
class GetCandlesticksOutput:
    candlesticks: List[Candlestick]

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
class CalcurateSmaOutput:
    @dataclass
    class Unit:
        date:       date
        price:      Decimal
        price_sma:  Decimal
        volume:     Decimal
        volume_sma: Decimal
    
    data: List[Unit]

@dataclass
class CalcurateWmaOutput:
    @dataclass
    class Unit:
        date:       date
        price:      Decimal
        price_wma:  Decimal
        volume:     Decimal
        volume_wma: Decimal
    
    data: List[Unit]

@dataclass
class CalcurateEmaOutput:
    @dataclass
    class Unit:
        date:       date
        price:      Decimal
        price_ema:  Decimal
        volume:     Decimal
        volume_ema: Decimal
    
    data: List[Unit]

@dataclass
class GetRankingPriceOutput:
    data: List[PerformanceData]

@dataclass
class GetRankingVolumeOutput:
    data: List[PerformanceData]

@dataclass
class GetRankingRsOutput:
    data: List[RelativeStrengthCalcurator.RelativeStrength]

@dataclass
class GetRankingDeviationOutput:
    data: List[PerformanceData]

@dataclass
class GetTrendPriceOutput:
    data: List[TrendData]

@dataclass
class GetTrendVolumeOutput:
    data: List[TrendData]

@dataclass
class GetTrendMomentumOutput:
    data: List[TrendData]

@dataclass
class ReflectStocksplitOutput:
    pass

@dataclass
class ClearCachedataOutput:
    pass

@dataclass
class MultipleCachedataOutput:
    pass

@dataclass
class GetCachedataOutput:
    @dataclass
    class StockScore:
        code:  str
        score: Decimal

    scores: List[StockScore]

@dataclass
class GetAthOutput:
    candlesticks: List[Candlestick]

@dataclass
class GetAtlOutput:
    candlesticks: List[Candlestick]

@dataclass
class GetAverageAtrOutput:
    average_atr: Decimal

@dataclass
class SimulateTradeRuleOutput:
    report: SimulationReport

@dataclass
class PredictSetupSignalOutput:
    candlesticks: List[Candlestick]

@dataclass
class DelistingStockOutput:
    pass

@dataclass
class ListingStockOutput:
    pass

@dataclass
class GetEachFirststickOutput:
    terms: List[Term]

@dataclass
class GetEachLaststickOutput:
    terms: List[Term]

@dataclass
class MakeCachetagOutput:
    pass
