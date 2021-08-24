from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar, List
from abc import ABCMeta, abstractmethod
from enum import IntEnum, auto
import random

from app.domain.stock import Candlestick
from app.domain.statistics import Statistics

@dataclass
class History:
    open_date:     date
    close_date:    date
    open_price:    Decimal
    close_price:   Decimal
    volume:        int
    position_type: PositionType

    def profit(self) -> Decimal:
        return (self.close_price - self.open_price)*self.volume if self.position_type == PositionType.BUY else (self.open_price - self.close_price) * self.volume

class PositionType(IntEnum):
    BUY:  ClassVar[int] = auto()
    SELL: ClassVar[int] = auto()

@dataclass
class InvestCondition:
    position_type: PositionType
    price:         Decimal
    volume:        int
    date:          date
    losscut_price: Decimal

class InvestRuleType(IntEnum):
    TURTLE:              ClassVar[int] = auto()
    RANDOM:              ClassVar[int] = auto()
    RANDOM_LONG:         ClassVar[int] = auto()
    RANDOM_TRAIL:        ClassVar[int] = auto()
    GOLDEN_TRAIL:        ClassVar[int] = auto()
    SERIAL_STEPUP_TRAIL: ClassVar[int] = auto()
    TRIPLE_STEPUP_TRAIL: ClassVar[int] = auto()
    BUYHOLD:             ClassVar[int] = auto()

class Commission(metaclass=ABCMeta):
    @abstractmethod
    def amount(self, delivery_price:Decimal) -> Decimal:
        """
        delivery_price: Decimal
        return (amount: Decimal)
        """
        raise NotImplementedError

class StandardCommission(Commission):
    minimum: Decimal
    maximum: Decimal
    rate:    Decimal

    def __init__(self, minimum: Decimal, maximum: Decimal, rate: Decimal):
        self.minimum = minimum
        self.maximum = maximum
        self.rate    = rate

    def amount(self, delivery_price:Decimal) -> Decimal:
        return min(max(self.minimum, self.rate*delivery_price), self.maximum)

class InvestRule(metaclass=ABCMeta):
    @abstractmethod
    def required_number_of_histrical_data(self) -> int:
        """
        return (number: int)
        """
        raise NotImplementedError

    @abstractmethod
    def exposure_unit(self, conditions: List[InvestCondition], cash: Decimal) -> Decimal:
        """
        conditions: List[InvestCondition]
        cash:       Decimal
        return (amount: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        return (ok: bool)
        """
        raise NotImplementedError

    @abstractmethod
    def have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal, unit: Decimal) -> (bool, Decimal):
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        cash:       Decimal
        unit:       Decimal
        return (ok: bool, cash: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        sticks: List[Candlestick]
        return (ok: bool)
        """
        raise NotImplementedError

    @abstractmethod
    def closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        cash :      Decimal
        return (ok: bool, history: List[History], cash: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def losscut_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        cash:       Decimal
        return (ok: bool, history: List[History], cash: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        return (ok: bool)
        """
        raise NotImplementedError

    @abstractmethod
    def have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal, unit: Decimal) -> (bool, Decimal):
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        cash:       Decimal
        unit:       Decimal
        return (ok: bool, cash: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        sticks:     List[Candlestick]
        conditions: List[InvestCondition]
        return (ok: bool)
        """
        raise NotImplementedError

    @abstractmethod
    def closedup_short(self, sticks: List[Candlestick], condition: InvestCondition, cash: Decimal) -> (bool, List[History], Decimal):
        """
        sticks:    List[Candlestick]
        condition: InvestCondition
        cash:      Decimal
        return (ok: bool, history: List[History], cash: Decimal)
        """
        raise NotImplementedError

    @abstractmethod
    def losscut_short(self, sticks: List[Candlestick], condition: InvestCondition, cash: Decimal) -> (bool, List[History], Decimal):
        """
        sticks:    List[Candlestick]
        condition: InvestCondition
        cash:      Decimal
        return (ok: bool, history: List[History], cash: Decimal)
        """
        raise NotImplementedError

class BaseInvestRule(InvestRule):
    unit_number:   int
    losscut_rate:  Decimal

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        self.unit_number   = unit_number
        self.losscut_rate  = losscut_rate

    @abstractmethod
    def required_number_of_histrical_data(self) -> int:
        raise NotImplementedError

    def exposure_unit(self, conditions: List[InvestCondition], cash: Decimal) -> Decimal:
        """
        Invest unit at risk free.
        """
        amount = cash

        for c in conditions:
            if c.position_type == PositionType.SELL:
                amount -= c.price * c.volume if c.position_type == PositionType.SELL else Decimal('0')

        available_num = self.unit_number - len(conditions) + len([c for c in conditions if c.position_type == PositionType.SELL])
        return Decimal('0') if available_num == 0 else amount / Decimal(available_num)

    @abstractmethod
    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal, unit: Decimal) -> (bool, Decimal):
        """
        Buy at the close price.
        """
        volume = int(unit/sticks[0].close_price)
        if volume <= 0:
            return (False, cash)

        conditions.append(InvestCondition(
            position_type = PositionType.BUY, 
            price         = sticks[0].close_price, 
            volume        = volume, 
            date          = sticks[0].date, 
            losscut_price = sticks[0].close_price * (1 - self.losscut_rate)
            ))

        return (True, cash - sticks[0].close_price * volume)

    @abstractmethod
    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        """
        Closed up at the close price.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) == 0: # Nothing to close up.
            (False, [], cash)

        removal   = list()
        histories = list()
        returned  = Decimal(0)

        for (index, condition) in enumerate(conditions): 
            if condition.position_type == PositionType.BUY:
                histories.append(History(
                    open_date     = condition.date,
                    close_date    = sticks[0].date,
                    open_price    = condition.price,
                    close_price   = sticks[0].close_price,
                    volume        = condition.volume,
                    position_type = PositionType.BUY
                    ))
                returned += sticks[0].close_price * condition.volume
                removal.append(index)

        for r in sorted(removal, reverse=True):
            del conditions[r]

        return (len(removal)>0, histories, cash + returned)

    def losscut_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        removal   = list()
        histories = list()
        returned  = Decimal(0)

        for (index, condition) in enumerate(conditions): 
            if condition.position_type == PositionType.BUY and sticks[0].low_price <= condition.losscut_price: 
                histories.append(History(
                    open_date     = condition.date,
                    close_date    = sticks[0].date,
                    open_price    = condition.price,
                    close_price   = condition.losscut_price,
                    volume        = condition.volume,
                    position_type = PositionType.BUY
                    ))
                returned += condition.losscut_price * condition.volume
                removal.append(index)

        for r in sorted(removal, reverse=True):
            del conditions[r]

        return (len(removal)>0, histories, cash + returned)

    @abstractmethod
    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal, unit: Decimal) -> (bool, Decimal):
        """
        Sell at the close price.
        """
        volume = int(unit/sticks[0].close_price)
        if volume <= 0:
            return (False, cash)

        conditions.append(InvestCondition(
                position_type = PositionType.SELL,
                price         = sticks[0].close_price,
                volume        = volume,
                date          = sticks[0].date,
                losscut_price = sticks[0].close_price * (1 + self.losscut_rate)
                ))

        return (True, cash + sticks[0].close_price * volume)

    @abstractmethod
    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        """
        Closed up at the close price.
        """
        if len([c for c in conditions if c.position_type == PositionType.SELL]) == 0: # Nothing to close up.
            (False, [], cash)

        removal   = list()
        histories = list()
        returned  = Decimal(0)

        for (index, condition) in enumerate(conditions): 
            if condition.position_type == PositionType.SELL:
                histories.append(History(
                    open_date     = condition.date,
                    close_date    = sticks[0].date,
                    open_price    = condition.price,
                    close_price   = sticks[0].close_price,
                    volume        = condition.volume,
                    position_type = PositionType.SELL
                    ))
                returned += sticks[0].close_price * condition.volume
                removal.append(index)

        for r in sorted(removal, reverse=True):
            del conditions[r]

        return (len(removal)>0, histories, cash - returned)

    def losscut_short(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        removal   = list()
        histories = list()
        returned  = Decimal(0)

        for (index, condition) in enumerate(conditions): 
            if condition.position_type == PositionType.SELL and  sticks[0].high_price >= condition.losscut_price: 
                histories.append(History(
                    open_date     = condition.date,
                    close_date    = sticks[0].date,
                    open_price    = condition.price,
                    close_price   = condition.losscut_price,
                    volume        = condition.volume,
                    position_type = PositionType.SELL
                    ))
                returned += condition.losscut_price * condition.volume
                removal.append(index)

        for r in sorted(removal, reverse=True):
            del conditions[r]

        return (len(removal)>0, histories, cash - returned)


class TurtleInvestRule(BaseInvestRule):
    setup_term:    int
    closedup_term: int
    setup_rate:    Decimal

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.setup_term    = 20
        self.closedup_term = 10
        self.setup_rate    = Decimal('0.1')

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return self.setup_term

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Newest close price is ATH in the recent 20 day.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) > 0: 
            # Don't have position, if you already have another LONG position.
            return False

        target_list = sticks[:self.setup_term]
        return (len(target_list) == self.setup_term) and (max([s.close_price for s in sticks]) == sticks[0].close_price) and random.random() < self.setup_rate

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Newest close price is ATL in the recent 10 day.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) == 0: # Nothing to close up.
            return False

        target_list = sticks[:self.closedup_term]
        return (len(target_list) == self.closedup_term) and (min([s.close_price for s in sticks]) == sticks[0].close_price)

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Newest close price is ATL in the recent 20 day.
        """
        if len([c for c in conditions if c.position_type == PositionType.SELL]) > 0: 
            # Don't have position, if you already have another SHORT position.
            return False

        target_list = sticks[:self.setup_term]
        return (len(target_list) == self.setup_term) and (min([s.close_price for s in sticks]) == sticks[0].close_price) and random.random() < self.setup_rate

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Newest close price is ATH in the recent 10 day.
        """
        if len([c for c in conditions if c.position_type == PositionType.SELL]) == 0: # Nothing to close up.
            return False

        target_list = sticks[:self.closedup_term]
        return (len(target_list) == self.closedup_term) and (max([s.close_price for s in sticks]) == sticks[0].close_price)

class RandomInvestRule(BaseInvestRule):
    setup_rate:    Decimal
    closedup_rate: Decimal
    tickers:       List[str]
    targets:       Dict[str, PositionType]
    target_number: int
    counter:       int
    buy_ratio:     float

    def __init__(self, unit_number:int, losscut_rate:Decimal, tickers:List[str], buy_ratio:Decimal = 0.5):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.setup_rate    = Decimal('0.1')
        self.closedup_rate = Decimal('0.1')
        self.tickers       = tickers
        self.target_number = min(unit_number, len(tickers))
        self.targets       = dict()
        self.counter       = int(0)
        self.buy_ratio     = buy_ratio

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return int(1)

    def _clear_targets(self):
        self.targets = dict()
        while len(self.targets) < self.target_number: 
            ticker = self.tickers[int(len(self.tickers)*random.random())]
            if ticker in self.targets:
                continue
            self.targets[ticker] = PositionType.BUY if random.random() < self.buy_ratio else PositionType.SELL
        self.counter = int(0)

    def _is_targets(self, ticker:str, position_type:PositionType) -> bool:
        if self.counter >= self.target_number:
            self._clear_targets()

        self.counter += 1
        return ticker in self.targets.keys() and self.targets[ticker] == position_type

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Random. Just under the setup rate.
        """
        if len(sticks) == 0 or not(self._is_targets(ticker = sticks[0].code, position_type = PositionType.BUY)) or len([c for c in conditions if c.position_type == PositionType.BUY]) > 0: 
            # Don't have position, if you already have another LONG position.
            return False

        return random.random() < self.setup_rate

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Random. Just under the setup rate.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) == 0: # Nothing to close up.
            return False

        return random.random() < self.closedup_rate

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Random. Just under the setup rate.
        """
        if len(sticks) == 0 or not(self._is_targets(ticker = sticks[0].code, position_type = PositionType.SELL)) or len([c for c in conditions if c.position_type == PositionType.SELL]) > 0: 
            # Don't have position, if you already have another SHORT position.
            return False

        return random.random() < self.setup_rate

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Random. Just under the setup rate.
        """
        if len([c for c in conditions if c.position_type == PositionType.SELL]) == 0: # Nothing to close up.
            return False

        return random.random() < self.closedup_rate

class RandomLongInvestRule(RandomInvestRule):

    def __init__(self, unit_number:int, losscut_rate:Decimal, tickers:List[str]):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate, tickers = tickers, buy_ratio = 1.0)

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

class BaseTrailInvestRule(BaseInvestRule):

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)

    @abstractmethod
    def required_number_of_histrical_data(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def losscut_long(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        for (index, condition) in enumerate(conditions): 
            # Trailing stop.
            if condition.position_type == PositionType.BUY and (sticks[0].low_price * (1 - self.losscut_rate)) > condition.losscut_price:
                condition.losscut_price = max(sticks[0].low_price * (1 - self.losscut_rate), condition.losscut_price)

        return super().losscut_long(sticks = sticks, conditions = conditions, cash = cash)

    @abstractmethod
    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        raise NotImplementedError

    def losscut_short(self, sticks: List[Candlestick], conditions: List[InvestCondition], cash: Decimal) -> (bool, List[History], Decimal):
        for (index, condition) in enumerate(conditions): 
            # Trailing stop.
            if condition.position_type == PositionType.SELL and (sticks[0].high_price * (1 + self.losscut_rate)) < condition.losscut_price:
                condition.losscut_price = min(sticks[0].high_price * (1 + self.losscut_rate), condition.losscut_price)

        return super().losscut_short(sticks = sticks, conditions = conditions, cash = cash)

class RandomTrailLongInvestRule(BaseTrailInvestRule):
    random_rule: RandomInvestRule

    def __init__(self, unit_number:int, losscut_rate:Decimal, tickers:List[str]):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.random_rule = RandomInvestRule(unit_number = unit_number, losscut_rate = losscut_rate, tickers = tickers, buy_ratio = 1.0)

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return self.random_rule.required_number_of_histrical_data()

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Random. Just under the setup rate.
        """
        return self.random_rule.reaching_have_long(sticks = sticks, conditions = conditions)

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

class GoldenTrailLongInvestRule(BaseTrailInvestRule):
    long_sma_term:  int
    short_sma_term: int
    setup_rate:     Decimal

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.long_sma_term  = int(25)
        self.short_sma_term = int(5)
        self.setup_rate     = Decimal('0.1')

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return self.long_sma_term + 1

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Under the Golden Cross.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) > 0: 
            # Don't have position, if you already have another LONG position.
            return False

        previous_statistics = Statistics(values = [s.close_price for s in sticks[1:]])
        current_statistics  = Statistics(values = [s.close_price for s in sticks])

        return previous_statistics.sma(25) > previous_statistics.sma(5) and current_statistics.sma(25) <= current_statistics.sma(5) and random.random() < self.setup_rate

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

class SerialStepupTrailLongInvestRule(BaseTrailInvestRule):
    term:       int
    number:     int
    setup_rate: Decimal

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.term       = int(3)
        self.number     = int(3)
        self.setup_rate = Decimal('0.1')

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return self.term * self.number

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Under the Golden Cross.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) > 0: 
            # Don't have position, if you already have another LONG position.
            return False

        if len(sticks) != self.required_number_of_histrical_data():
            return False

        ath_of_high = []
        atl_of_low  = []
        for index in range(self.number):
            window = sticks[(self.number - index - 1)*self.term:(self.number - index)*self.term]
            ath_of_high.append(max([s.high_price for s in window]))
            atl_of_low.append(min([s.low_price for s in window]))

        return all([a < b for (a, b) in list(zip(ath_of_high[0:-1], ath_of_high[1:]))]) and all([a < b for (a, b) in list(zip(atl_of_low[0:-1], atl_of_low[1:]))]) and random.random() < self.setup_rate

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

class BuyholdInvestRule(BaseInvestRule):
    stick_numbers: int
    exec_indexes:  Dict[str,int]
    counters:      Dict[str,int]

    def __init__(self, unit_number:int, losscut_rate:Decimal, stick_numbers:Dict[str,int]):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)
        self.stick_numbers = stick_numbers

        self.exec_indexes = {}
        self.counters = {}
        while len(self.exec_indexes.keys()) < min(unit_number, len(stick_numbers.keys())):
            target_num = int(len(stick_numbers.keys()) * random.random())
            for (index, (ticker, numbers)) in enumerate(stick_numbers.items()):
                if index == target_num and not (ticker in self.exec_indexes):
                    self.exec_indexes[ticker] = int(numbers * random.random())
                    self.counters[ticker]     = int(0)

    def required_number_of_histrical_data(self) -> int:
        """
        Required number of histrical data.
        """
        return int(1)

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Newest close price is ATH in the recent 20 day.
        """
        if len([c for c in conditions if c.position_type == PositionType.BUY]) > 0: 
            # Don't have position, if you already have another LONG position.
            return False

        if len(sticks) == 0:
            return False

        ticker = sticks[0].code
        result = False
        if ticker in self.exec_indexes:
            if self.exec_indexes[ticker] == self.counters[ticker]:
                result = True 
            self.counters[ticker] += 1
        return result

    def reaching_closedup_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_have_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

    def reaching_closedup_short(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Disabled.
        """
        return False

class TripleStepupTrailLongInvestRule(SerialStepupTrailLongInvestRule):

    def __init__(self, unit_number:int, losscut_rate:Decimal):
        super().__init__(unit_number = unit_number, losscut_rate = losscut_rate)

    def reaching_have_long(self, sticks: List[Candlestick], conditions: List[InvestCondition]) -> bool:
        """
        Under the Golden Cross.
        """
        result = super().reaching_have_long(sticks = sticks, conditions = conditions) # This inherits randomness.

        volumes  = []
        for index in range(self.number):
            window = sticks[(self.number - index - 1)*self.term:(self.number - index)*self.term]
            volumes.append([s.volume for s in window])

        result &=  all([a < b for (a, b) in list(zip(volumes[0:-1], volumes[1:]))])
        return result

