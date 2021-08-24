from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar, List, Dict

from app.domain.stock import Candlestick
from app.domain.invest import PositionType, InvestCondition, InvestRule, TurtleInvestRule, History, Commission

@dataclass
class SimulationReport:
    principal:         Decimal
    current_valuation: Decimal
    mean_profit:       Decimal
    mean_loss:         Decimal
    win_rate:          Decimal
    lose_rate:         Decimal
    payoff_ratio:      Decimal
    histories:         Dict[str,List[History]]
    positions:         Dict[str,List[InvestCondition]]
    commission:        Decimal

class InvestSimulator:
    principal:  Decimal
    rule:       InvestRule
    commission: Commission
    sticks:     Dict[str,List[Candlestick]]
    cash:       Decimal
    conditions: Dict[str,List[InvestCondition]]
    histories:  Dict[str,List[History]]

    def __init__(self, rule:InvestRule, sticks:Dict[str,List[Candlestick]], cash:Decimal, commission:Commission):
        self.rule       = rule
        self.sticks     = sticks
        self.cash       = cash
        self.principal  = cash
        self.conditions = {}
        self.histories  = {}
        self.commission = commission

    def simulate(self):
        required_list_number = self.rule.required_number_of_histrical_data()
        previous_target_sticks = {}

        for ticker in self.sticks.keys():
            self.conditions[ticker]        = list()
            self.histories[ticker]         = list()
            previous_target_sticks[ticker] = list()

        max_sticks = max([len(s) for s in self.sticks.values()])

        for i in range(max_sticks):
            for (ticker, sticks) in self.sticks.items():
                start_index = len(sticks) - i - required_list_number
                if start_index < 0:
                    continue

                target_sticks = sticks[start_index:start_index + required_list_number]
                unit = self.rule.exposure_unit(
                        conditions = [c for conditions in self.conditions.values() for c in conditions],
                        cash       = self.cash
                        )

                (_, histories, self.cash) = self.rule.losscut_long(target_sticks, self.conditions[ticker], self.cash)
                self.histories[ticker].extend(histories)

                (_, histories, self.cash) = self.rule.losscut_short(target_sticks, self.conditions[ticker], self.cash)
                self.histories[ticker].extend(histories)

                if self.rule.reaching_have_long(previous_target_sticks[ticker], self.conditions[ticker]):
                    (_, self.cash) = self.rule.have_long(target_sticks, self.conditions[ticker], self.cash, unit)

                if self.rule.reaching_have_short(previous_target_sticks[ticker], self.conditions[ticker]):
                    (_, self.cash) = self.rule.have_short(target_sticks, self.conditions[ticker], self.cash, unit)

                if self.rule.reaching_closedup_long(previous_target_sticks[ticker], self.conditions[ticker]):
                    (_, histories, self.cash) = self.rule.closedup_long(target_sticks, self.conditions[ticker], self.cash)
                    self.histories[ticker].extend(histories)

                if self.rule.reaching_closedup_short(previous_target_sticks[ticker], self.conditions[ticker]):
                    (_, histories, self.cash) = self.rule.closedup_short(target_sticks, self.conditions[ticker], self.cash)
                    self.histories[ticker].extend(histories)

                previous_target_sticks[ticker] = target_sticks

    def evaluate(self, sticks: Dict[str,Candlestick]) -> Decimal:
        long_value = short_value = Decimal('0')
        for (k, s) in sticks.items(): 
            long_value  += Decimal(sum([s.close_price * c.volume for c in self.conditions[k] if c.position_type == PositionType.BUY]))
            short_value += Decimal(sum([s.close_price * c.volume for c in self.conditions[k] if c.position_type == PositionType.SELL]))

        return self.cash + long_value - short_value

    def mean_profit(self) -> Decimal:
        profit_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() > 0]
        return Decimal('0') if len(profit_list) == 0 else sum(profit_list)/Decimal(len(profit_list))

    def mean_loss(self) -> Decimal:
        loss_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() < 0]
        return Decimal('0') if len(loss_list) == 0 else sum(loss_list)/Decimal(len(loss_list))

    def payoff_ratio(self) -> Decimal:
        return Decimal('0') if self.mean_loss() == Decimal('0') else self.mean_profit()/abs(self.mean_loss())

    def win_rate(self) -> Decimal:
        profit_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() > 0]
        loss_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() < 0]
        return Decimal('0') if len(profit_list)+len(loss_list) == 0 else Decimal(len(profit_list))/Decimal(len(profit_list)+len(loss_list))

    def lose_rate(self) -> Decimal:
        profit_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() > 0]
        loss_list = [h.profit() for histories in self.histories.values() for h in histories if h.profit() < 0]
        return Decimal('0') if len(profit_list)+len(loss_list) == 0 else Decimal(len(loss_list))/Decimal(len(profit_list)+len(loss_list))

    def commission_amount(self) -> Decimal:
        past_open  = sum([self.commission.amount(
            delivery_price = h.open_price*h.volume) for histories in self.histories.values() for h in histories]
            )
        past_close = sum([self.commission.amount(
            delivery_price = h.close_price*h.volume) for histories in self.histories.values() for h in histories]
            )
        current_open = sum([self.commission.amount(
            delivery_price = c.price*c.volume) for conditions in self.conditions.values() for c in conditions]
            )

        return past_open + past_close + current_open

    def report(self, sticks: Dict[str,Candlestick]) -> SimulationReport:
        return SimulationReport(
                principal         = self.principal,
                current_valuation = self.evaluate(sticks = sticks),
                mean_profit       = self.mean_profit(),
                mean_loss         = self.mean_loss(),
                win_rate          = self.win_rate(),
                lose_rate         = self.lose_rate(),
                payoff_ratio      = self.payoff_ratio(),
                histories         = self.histories,
                positions         = self.conditions,
                commission        = self.commission_amount()
                )
