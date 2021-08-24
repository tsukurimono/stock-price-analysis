from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
from decimal import Decimal, ROUND_UP
from datetime import date
from enum import IntEnum, auto

class Interval(IntEnum):
    DAILY:   ClassVar[int] = auto()
    UNKNOWN: ClassVar[int] = auto()

@dataclass(order = True)
class Candlestick:
    code:        str
    market:      str
    date:        date

    open_price:  Decimal
    close_price: Decimal
    high_price:  Decimal
    low_price:   Decimal
    volume:      int

    interval:    Interval
    patched:     bool = field(compare = False, default = False)

    def __init__(self, code, market, date, open_price, close_price, high_price, low_price, volume, interval, patched=False):
        self.code        = code
        self.market      = market
        self.date        = date

        self.open_price  = open_price.quantize(Decimal('.0000001'), rounding=ROUND_UP)
        self.close_price = close_price.quantize(Decimal('.0000001'), rounding=ROUND_UP)
        self.high_price  = high_price.quantize(Decimal('.0000001'), rounding=ROUND_UP)
        self.low_price   = low_price.quantize(Decimal('.0000001'), rounding=ROUND_UP)
        self.volume      = volume

        self.interval    = interval
        self.patched     = patched

@dataclass
class Atr:
    candlesticks: List[Candlestick]

    def calculate(self) -> List[Decimal]:
        previous = self.candlesticks[0]

        result = list()
        for value in self.candlesticks:
            result.append(
                    max([abs(value.high_price - previous.close_price), abs(value.low_price - previous.close_price), abs(value.high_price - value.low_price)])
                    )
            
        return result

    def average(self, term:int) -> List[Decimal]:
        atr_list = self.calculate()
        return [sum(atr_list[i:i+term])/Decimal(term) for i in range(len(atr_list) - term + 1)]


@dataclass
class Stock:
    code:   str
    market: str
    tags:   List[str]

@dataclass
class Term:
    code:       str
    market:     str
    first_date: date
    last_date:  date
