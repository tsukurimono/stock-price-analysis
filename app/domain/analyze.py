from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import ClassVar, List

from enum import IntEnum, auto
from app.domain.stock import Candlestick

@dataclass
class ScoreCalcurator:
    def faster_better(self, data:List[str]) -> Dict[str:Decimal]: 
        """
        Input:  ['ZM', 'AAPL', ...]
        Output: {'ZM': 1, 'AAPL': 0.99,...}
        """
        return {datum:  Decimal(1) - Decimal(idx)/Decimal(len(data)) for (idx, datum) in list(enumerate(data))}

class RankingOrder(IntEnum):
    ASC:  ClassVar[int] = auto()
    DESC: ClassVar[int] = auto()

class TrendType(IntEnum):
    UP:   ClassVar[int] = auto()
    DOWN: ClassVar[int] = auto()

@dataclass
class TrendData:
    code:      str
    market:    str
    from_date: date
    to_date:   date
    up:        int
    down:      int

@dataclass
class PerformanceData:
    code:          str
    market:        str
    base_value:    Decimal
    base_date:     date
    present_value: Decimal
    present_date:  date

    def change_rate(self) -> Decimal:
        return Decimal(0) if self.base_value == Decimal(0) else (self.present_value - self.base_value)/self.base_value

    def rate(self) -> Decimal:
        return Decimal(0) if self.base_value == Decimal(0) else self.present_value / self.base_value

@dataclass
class RelativeStrengthCalcurator:
    @dataclass
    class RawScore: 
        code:     str 
        market:   str 
        stick:    Candlestick
        stick63:  Candlestick
        stick126: Candlestick
        stick189: Candlestick
        stick252: Candlestick

        def score(self) -> Decimal:
            return 2*self.stick.close_price/self.stick63.close_price + self.stick.close_price/self.stick126.close_price + self.stick.close_price/self.stick189.close_price + self.stick.close_price/self.stick252.close_price

    @dataclass
    class RelativeStrength:
        code:     str
        market:   str
        stick:    Candlestick
        stick63:  Candlestick
        stick126: Candlestick
        stick189: Candlestick
        stick252: Candlestick
        rawscore: Decimal
        point:    int

    raw_scores: List[RawScore]

    def relative_strength(self) -> List[RelativeStrength]:
        sorted_scores = sorted(self.raw_scores, key=lambda x: x.score(), reverse=True)

        result = list()
        for (idx, score) in enumerate(sorted_scores):
            result.append( self.RelativeStrength(
                code     = score.code,
                market   = score.market,
                stick    = score.stick,
                stick63  = score.stick63,
                stick126 = score.stick126,
                stick189 = score.stick189,
                stick252 = score.stick252,
                rawscore = score.score(),
                point = 100 - int(idx/len(sorted_scores)*100) - 1
                ))

        return result

