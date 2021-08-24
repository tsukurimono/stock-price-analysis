from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class EnvelopeData:
    top:     Decimal
    average: Decimal
    bottom:  Decimal

@dataclass
class Statistics:
    values: List[Decimal]

    def sma(self, term:int) -> List[Decimal]:
        result = list()

        if len(self.values) < term:
            return result

        for i in range(len(self.values)-term+1):
            value = Decimal('0')
            for j in range(term):
                value = value + self.values[i + j]/term
            result.append(value)
        
        return result

    def wma(self, term:int) -> List[Decimal]:
        result = list()

        if len(self.values) < term:
            return result

        for i in range(len(self.values)-term+1):
            value = Decimal('0')
            for j in range(term):
                value = value + self.values[i + j]*(j + 1)
            result.append(value/sum(range(1, term+1)))
        
        return result

    def ema(self, term:int) -> List[Decimal]:
        result = list()

        if len(self.values) < term:
            return result

        last_value = sum(self.values[0:term])/term
        result.append(last_value)
        for value in self.values[term:]:
            last_value = last_value + (Decimal('2')/(term + 1))*(value - last_value)
            result.append(last_value)

        return result

    def envelope_sma(self, term:int, percent:Decimal) -> [EnvelopeData]:
        result = list()
        sma = self.sma(term = term)

        for value in sma:
            result.append(EnvelopeData(top = value*(1 + percent/100), average = value, bottom = value*(1 - percent/100)))

        return result

    def mean(self) -> Decimal:
        return sum(self.values)/Decimal(len(self.values))

    def variance(self) -> Decimal:
        mean = self.mean()
        return sum([(value - mean)**2 for value in self.values])/Decimal(len(self.values))

    def standard_deviation(self) -> Decimal:
        return self.variance()**Decimal('0.5')
