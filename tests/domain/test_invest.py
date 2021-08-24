import unittest
from datetime import date
from decimal import Decimal

from app.domain.invest import *
from app.domain.stock import *

class TestCommnet(unittest.TestCase):

    def test_required_number_of_histrical_data(self):
        """
        required_number_of_histrical_data
        """
        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        self.assertEqual(20, rule.required_number_of_histrical_data())

    def test_exposure_unit(self):
        """
        exposure_unit
        """
        input_data = [
                {
                    'val': { 
                        'conditions': [],
                        'cash': Decimal('100000') 
                        }, 
                    'expected': Decimal('10000')
                    },
                {
                    'val': { 
                        'conditions': [ 
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = int(500), date = date(2019, 10, 20), losscut_price = Decimal('22')),
                            ],
                        'cash': Decimal('110000') 
                        }, 
                    'expected': Decimal('10000')
                    },
                {
                    'val': { 
                        'conditions': [ 
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = int(500), date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            ],
                        'cash': Decimal('90000') 
                        }, 
                    'expected': Decimal('10000')
                    }
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            self.assertEqual(data['expected'], rule.exposure_unit(conditions = data['val']['conditions'], cash = data['val']['cash'])) 

# TODO: Need to be mocked at random().
#
#    def test_reaching_have_long(self):
#        """
#        reaching_have_long
#        """
#        input_data = [
#                {'val': {'sticks': [ # ATH at the most recent date.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('21'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('11'), high_price = Decimal('12'), low_price = Decimal('13'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('10'), high_price = Decimal('11'), low_price = Decimal('12'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('9'),  high_price = Decimal('10'), low_price = Decimal('11'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('8'),  high_price = Decimal('9'),  low_price = Decimal('10'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('7'),  high_price = Decimal('8'),  low_price = Decimal('9'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('6'),  high_price = Decimal('7'),  low_price = Decimal('8'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('5'),  high_price = Decimal('6'),  low_price = Decimal('7'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('4'),  high_price = Decimal('5'),  low_price = Decimal('6'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('3'),  high_price = Decimal('4'),  low_price = Decimal('5'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('2'),  high_price = Decimal('3'),  low_price = Decimal('4'),  volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': []}, 'expected': True},
#                {'val': {'sticks': [ # ATH at the most recent date, and only have SHORT position.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('21'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('11'), high_price = Decimal('12'), low_price = Decimal('13'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('10'), high_price = Decimal('11'), low_price = Decimal('12'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('9'),  high_price = Decimal('10'), low_price = Decimal('11'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('8'),  high_price = Decimal('9'),  low_price = Decimal('10'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('7'),  high_price = Decimal('8'),  low_price = Decimal('9'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('6'),  high_price = Decimal('7'),  low_price = Decimal('8'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('5'),  high_price = Decimal('6'),  low_price = Decimal('7'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('4'),  high_price = Decimal('5'),  low_price = Decimal('6'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('3'),  high_price = Decimal('4'),  low_price = Decimal('5'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('2'),  high_price = Decimal('3'),  low_price = Decimal('4'),  volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal(0), volume = int(3), date = date(2019, 10, 20), losscut_price = Decimal(0))]}, 'expected': True},
#                {'val': {'sticks': [ # ATH at the most recent date, but already have LONG position.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('21'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('11'), high_price = Decimal('12'), low_price = Decimal('13'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('10'), high_price = Decimal('11'), low_price = Decimal('12'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('9'),  high_price = Decimal('10'), low_price = Decimal('11'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('8'),  high_price = Decimal('9'),  low_price = Decimal('10'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('7'),  high_price = Decimal('8'),  low_price = Decimal('9'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('6'),  high_price = Decimal('7'),  low_price = Decimal('8'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('5'),  high_price = Decimal('6'),  low_price = Decimal('7'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('4'),  high_price = Decimal('5'),  low_price = Decimal('6'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('3'),  high_price = Decimal('4'),  low_price = Decimal('5'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('2'),  high_price = Decimal('3'),  low_price = Decimal('4'),  volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal(0), volume = int(3), date = date(2019, 10, 20), losscut_price = Decimal(0))]}, 'expected': False},
#                {'val': {'sticks': [ # ATH on a date that is not the most recent.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('11'), high_price = Decimal('22'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('11'), high_price = Decimal('12'), low_price = Decimal('13'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('10'), high_price = Decimal('11'), low_price = Decimal('12'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('9'),  high_price = Decimal('10'), low_price = Decimal('11'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('8'),  high_price = Decimal('9'),  low_price = Decimal('10'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('7'),  high_price = Decimal('8'),  low_price = Decimal('9'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('6'),  high_price = Decimal('7'),  low_price = Decimal('8'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('5'),  high_price = Decimal('6'),  low_price = Decimal('7'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('4'),  high_price = Decimal('5'),  low_price = Decimal('6'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('3'),  high_price = Decimal('4'),  low_price = Decimal('5'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('2'),  high_price = Decimal('3'),  low_price = Decimal('4'),  volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': []}, 'expected': False},
#                ]
#
#        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
#        for data in input_data: 
#            self.assertEqual(data['expected'], rule.reaching_have_long(sticks = data['val']['sticks'], conditions = data['val']['conditions'])) 

    def test_have_long(self):
        """
        have_long
        """
        input_data = [
                {'val': {'cash': Decimal('100000'), 'sticks' : [  # Normal case.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [], 'unit': Decimal('10000')}, 'expected': {'return': (True, Decimal('90000')), 'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]}},
                {'val': {'cash': Decimal('110000'), 'sticks' : [  # Already have another position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [
                        InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('22'))
                        ], 'unit': Decimal('10000')}, 'expected': {'return': (True, Decimal('100000')), 'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('22')),
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')), 
                            ]}},
                {'val': {'cash': Decimal('100'), 'sticks' : [  # Error case (Cash is not enough).
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [], 'unit': Decimal('10')}, 'expected': {'return': (False, Decimal('100')), 'conditions': []}},
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.have_long(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'], unit = data['val']['unit'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

    def test_reaching_closedup_long(self):
        """
        reaching_closedup_long
        """
        input_data = [
                {'val': {'sticks': [ # ATL at the most recent date.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('11'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]}, 'expected': True},
                {'val': {'sticks': [ # ATL at the most recent date, but have no position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('11'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': []}, 'expected': False},
                {'val': {'sticks': [ # ATL at the most recent date, but have only SHORT position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('11'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]}, 'expected': False},
                {'val': {'sticks': [ # ATL on a date that is not the most recent.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('21'), high_price = Decimal('22'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': []}, 'expected': False},
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            got = rule.reaching_closedup_long(sticks = data['val']['sticks'], conditions = data['val']['conditions'])
            self.assertEqual(data['expected'], got) 

    def test_closedup_long(self):
        """
        closedup_long
        """
        input_data = [ 
                {
                    'val': { # Normal case.  
                        'cash':  Decimal('90000'), 
                        'conditions': [ 
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 19), losscut_price = Decimal('18'))
                            ], 
                        'sticks' : [ 
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {'return': (True, [History(open_date = date(2019, 10, 19), close_date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), volume = 500, position_type = PositionType.BUY)], Decimal('104000')), 'conditions': []}
                    },
                {
                    'val': { # Multiple position.
                        'cash':  Decimal('90000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 18), losscut_price = Decimal('18')),
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('21'), volume = 500, date = date(2019, 10, 19), losscut_price = Decimal('18')),
                            ],
                        'sticks' : [  
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [
                            History(open_date = date(2019, 10, 18), close_date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), volume = 500, position_type = PositionType.BUY),
                            History(open_date = date(2019, 10, 19), close_date = date(2019, 10, 20), open_price = Decimal('21'), close_price = Decimal('28'), volume = 500, position_type = PositionType.BUY),
                            ], Decimal('118000')), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            ]
                        }
                    },
                {
                    'val': { # No LONG position.
                        'cash':  Decimal('90000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            ],
                        'sticks' : [  
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (False, [], Decimal('90000')), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            ]
                        }
                    },
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.closedup_long(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

    def test_losscut_long(self):
        """
        losscut_long
        """
        input_data = [
                {
                    'val': { # Normal case.
                        'cash':  Decimal('90000'), 
                        'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 19), losscut_price = Decimal('18'))], 
                        'sticks' : [  
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('23'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [History(open_date = date(2019, 10, 19), close_date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('18'), volume = 500, position_type = PositionType.BUY)], Decimal('99000')),
                        'conditions': []
                        }
                    },
                {
                    'val': { # Multiple position.
                        'cash':  Decimal('90000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 18), losscut_price = Decimal('18')),
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 19), losscut_price = Decimal('18')),
                            ], 
                        'sticks' : [  
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('23'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [ 
                            History(open_date = date(2019, 10, 18), close_date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('18'), volume = 500, position_type = PositionType.BUY),
                            History(open_date = date(2019, 10, 19), close_date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('18'), volume = 500, position_type = PositionType.BUY),
                            ], Decimal('108000')),
                        'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]
                        }
                    },
                {
                    'val': {  # Hold case.
                        'cash':  Decimal('90000'), 
                        'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))], 
                        'sticks' : [
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('23'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (False, [], Decimal('90000')),
                        'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]
                        }
                    },
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.losscut_long(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

# TODO: Need to be mocked at random().
#
#    def test_reaching_have_short(self):
#        """
#        reaching_have_short
#        """
#        input_data = [
#                {'val': {'sticks': [ # ATL at the most recent date.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('23'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('24'), high_price = Decimal('21'), low_price = Decimal('24'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('25'), high_price = Decimal('20'), low_price = Decimal('25'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('26'), high_price = Decimal('19'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('27'), high_price = Decimal('18'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('28'), high_price = Decimal('17'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('27'), high_price = Decimal('16'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('26'), high_price = Decimal('15'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('27'), high_price = Decimal('14'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('28'), high_price = Decimal('13'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('30'), high_price = Decimal('12'), low_price = Decimal('30'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('31'), high_price = Decimal('11'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('31'), high_price = Decimal('10'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('31'), high_price = Decimal('9'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('31'), high_price = Decimal('8'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('31'), high_price = Decimal('7'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('31'), high_price = Decimal('6'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('31'), high_price = Decimal('5'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('31'), high_price = Decimal('4'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('31'), high_price = Decimal('3'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': []}, 'expected': True},
#                {'val': {'sticks': [ # ATL at the most recent date, and only have LONG position.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('23'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('24'), high_price = Decimal('21'), low_price = Decimal('24'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('25'), high_price = Decimal('20'), low_price = Decimal('25'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('26'), high_price = Decimal('19'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('27'), high_price = Decimal('18'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('28'), high_price = Decimal('17'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('27'), high_price = Decimal('16'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('26'), high_price = Decimal('15'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('27'), high_price = Decimal('14'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('28'), high_price = Decimal('13'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('30'), high_price = Decimal('12'), low_price = Decimal('30'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('31'), high_price = Decimal('11'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('31'), high_price = Decimal('10'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('31'), high_price = Decimal('9'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('31'), high_price = Decimal('8'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('31'), high_price = Decimal('7'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('31'), high_price = Decimal('6'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('31'), high_price = Decimal('5'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('31'), high_price = Decimal('4'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('31'), high_price = Decimal('3'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal(0), volume = int(3), date = date(2019, 10, 20), losscut_price = Decimal(0))]}, 'expected': True},
#                {'val': {'sticks': [ # ATL at the most recent date, but already have SHORT position.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('23'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('24'), high_price = Decimal('21'), low_price = Decimal('24'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('25'), high_price = Decimal('20'), low_price = Decimal('25'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('26'), high_price = Decimal('19'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('27'), high_price = Decimal('18'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('28'), high_price = Decimal('17'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('27'), high_price = Decimal('16'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('26'), high_price = Decimal('15'), low_price = Decimal('26'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('27'), high_price = Decimal('14'), low_price = Decimal('27'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('28'), high_price = Decimal('13'), low_price = Decimal('28'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('30'), high_price = Decimal('12'), low_price = Decimal('30'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('31'), high_price = Decimal('11'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('31'), high_price = Decimal('10'), low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('31'), high_price = Decimal('9'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('31'), high_price = Decimal('8'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('31'), high_price = Decimal('7'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('31'), high_price = Decimal('6'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('31'), high_price = Decimal('5'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('31'), high_price = Decimal('4'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('31'), high_price = Decimal('3'),  low_price = Decimal('31'), volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal(0), volume = int(3), date = date(2019, 10, 20), losscut_price = Decimal(0))]}, 'expected': False},
#                {'val': {'sticks': [ # ATL on a date that is not the most recent.
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('11'), high_price = Decimal('22'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 10), open_price = Decimal('10'), close_price = Decimal('11'), high_price = Decimal('12'), low_price = Decimal('13'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 9),  open_price = Decimal('9'),  close_price = Decimal('10'), high_price = Decimal('11'), low_price = Decimal('12'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 8),  open_price = Decimal('8'),  close_price = Decimal('9'),  high_price = Decimal('10'), low_price = Decimal('11'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 7),  open_price = Decimal('7'),  close_price = Decimal('8'),  high_price = Decimal('9'),  low_price = Decimal('10'), volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 6),  open_price = Decimal('6'),  close_price = Decimal('7'),  high_price = Decimal('8'),  low_price = Decimal('9'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 5),  open_price = Decimal('5'),  close_price = Decimal('6'),  high_price = Decimal('7'),  low_price = Decimal('8'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 4),  open_price = Decimal('4'),  close_price = Decimal('5'),  high_price = Decimal('6'),  low_price = Decimal('7'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 3),  open_price = Decimal('3'),  close_price = Decimal('4'),  high_price = Decimal('5'),  low_price = Decimal('6'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 2),  open_price = Decimal('2'),  close_price = Decimal('3'),  high_price = Decimal('4'),  low_price = Decimal('5'),  volume = int(100), interval = Interval.DAILY),
#                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 1),  open_price = Decimal('1'),  close_price = Decimal('2'),  high_price = Decimal('3'),  low_price = Decimal('4'),  volume = int(100), interval = Interval.DAILY),
#                    ], 'conditions': []}, 'expected': False},
#                ]
#
#        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
#        for data in input_data: 
#            self.assertEqual(data['expected'], rule.reaching_have_short(sticks = data['val']['sticks'], conditions = data['val']['conditions'])) 

    def test_have_short(self):
        """
        have_short
        """
        input_data = [
                {'val': {'cash': Decimal('100000'), 'sticks' : [  # Normal case.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('40'), close_price = Decimal('33'), high_price = Decimal('50'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [], 'unit': Decimal('10000')}, 'expected': {'return': (True, Decimal('109999')), 'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))]}},
                {'val': {'cash': Decimal('90000'), 'sticks' : [  # Already have another position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('40'), close_price = Decimal('33'), high_price = Decimal('50'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [ 
                        InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))
                        ], 'unit': Decimal('10000')}, 'expected': {'return': (True, Decimal('99999')), 'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18')),
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3')), 
                            ]}},
                {'val': {'cash': Decimal('100'), 'sticks' : [  # Error case (Cash is not enough).
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [], 'unit': Decimal('10')}, 'expected': {'return': (False, Decimal('100')), 'conditions': []}},
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.have_short(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'], unit = data['val']['unit'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

    def test_reaching_closedup_short(self):
        """
        reaching_closedup_short
        """
        input_data = [
                {'val': {'sticks': [ # ATH at the most recent date.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('25'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]}, 'expected': True},
                {'val': {'sticks': [ # ATH at the most recent date, but have no position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('25'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': []}, 'expected': False},
                {'val': {'sticks': [ # ATH at the most recent date, but have only LONG position.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('25'), high_price = Decimal('22'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': [InvestCondition(position_type = PositionType.BUY, price = Decimal('20'), volume = 500, date = date(2019, 10, 20), losscut_price = Decimal('18'))]}, 'expected': False},
                {'val': {'sticks': [ # ATH on a date that is not the most recent.
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('17'), high_price = Decimal('22'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 19), open_price = Decimal('19'), close_price = Decimal('20'), high_price = Decimal('21'), low_price = Decimal('22'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 18), open_price = Decimal('18'), close_price = Decimal('19'), high_price = Decimal('20'), low_price = Decimal('21'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 17), open_price = Decimal('17'), close_price = Decimal('18'), high_price = Decimal('19'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 16), open_price = Decimal('16'), close_price = Decimal('17'), high_price = Decimal('18'), low_price = Decimal('19'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 15), open_price = Decimal('15'), close_price = Decimal('16'), high_price = Decimal('17'), low_price = Decimal('18'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 14), open_price = Decimal('14'), close_price = Decimal('15'), high_price = Decimal('16'), low_price = Decimal('17'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 13), open_price = Decimal('13'), close_price = Decimal('14'), high_price = Decimal('15'), low_price = Decimal('16'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 12), open_price = Decimal('12'), close_price = Decimal('13'), high_price = Decimal('14'), low_price = Decimal('15'), volume = int(100), interval = Interval.DAILY),
                    Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 11), open_price = Decimal('11'), close_price = Decimal('12'), high_price = Decimal('13'), low_price = Decimal('14'), volume = int(100), interval = Interval.DAILY),
                    ], 'conditions': []}, 'expected': False},
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            got = rule.reaching_closedup_short(sticks = data['val']['sticks'], conditions = data['val']['conditions'])
            self.assertEqual(data['expected'], got) 

    def test_closedup_short(self):
        """
        closedup_short
        """
        input_data = [
                {
                    'val': {  # Normal case.
                        'cash':  Decimal('104000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 17), losscut_price = Decimal('36.3'))
                            ], 
                        'sticks' : [
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {'return': (True, [ 
                        History(open_date = date(2019, 10, 17), close_date = date(2019, 10, 20), open_price = Decimal('33'), close_price = Decimal('28'), volume = 303, position_type = PositionType.SELL),
                        ], Decimal('95516')), 'conditions': []}
                    },
                {
                    'val': {  # Multiple position.
                        'cash':  Decimal('104000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 16), losscut_price = Decimal('36.3')),
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3')),
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('34'), volume = 303, date = date(2019, 10, 18), losscut_price = Decimal('36.3'))
                            ], 
                        'sticks' : [
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [
                        History(open_date = date(2019, 10, 16), close_date = date(2019, 10, 20), open_price = Decimal('33'), close_price = Decimal('28'), volume = 303, position_type = PositionType.SELL),
                        History(open_date = date(2019, 10, 18), close_date = date(2019, 10, 20), open_price = Decimal('34'), close_price = Decimal('28'), volume = 303, position_type = PositionType.SELL),
                            ], Decimal('87032')), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))
                            ]
                        }
                    },
                {
                    'val': {  # No SHORT position.
                        'cash':  Decimal('104000'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))
                            ], 
                        'sticks' : [
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('28'), high_price = Decimal('29'), low_price = Decimal('23'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (False, [], Decimal('104000')), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))
                            ]
                        }
                    },
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.closedup_short(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

    def test_losscut_short(self):
        """
        losscut_short
        """
        input_data = [
                {
                    'val': {  # Normal case.
                        'cash':  Decimal('109999'), 
                        'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 15), losscut_price = Decimal('36.3'))], 
                        'sticks' : [ 
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('30'), close_price = Decimal('30'), high_price = Decimal('37'), low_price = Decimal('29'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [ 
                            History(open_date = date(2019, 10, 15), close_date = date(2019, 10, 20), open_price = Decimal('33'), close_price = Decimal('36.3'), volume = 303, position_type = PositionType.SELL),
                            ], Decimal('99000.1')),
                        'conditions': []
                        }
                    },
                {
                    'val': {  # Multiple position.
                        'cash':  Decimal('109999'), 
                        'conditions': [
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 14), losscut_price = Decimal('36.3')),
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3')),
                            InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 16), losscut_price = Decimal('36.3')),
                            ], 
                        'sticks' : [ 
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('30'), close_price = Decimal('30'), high_price = Decimal('37'), low_price = Decimal('29'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (True, [
                            History(open_date = date(2019, 10, 14), close_date = date(2019, 10, 20), open_price = Decimal('33'), close_price = Decimal('36.3'), volume = 303, position_type = PositionType.SELL),
                            History(open_date = date(2019, 10, 16), close_date = date(2019, 10, 20), open_price = Decimal('33'), close_price = Decimal('36.3'), volume = 303, position_type = PositionType.SELL),
                            ], Decimal('88001.2')),
                        'conditions': [
                            InvestCondition(position_type = PositionType.BUY, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3')),
                            ]
                        }
                    },
                {
                    'val': {  # Hold case. 
                        'cash':  Decimal('109999'), 
                        'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))],
                        'sticks' : [
                            Candlestick(code = 'AAAA', market = 'NASDAQ', date = date(2019, 10, 20), open_price = Decimal('20'), close_price = Decimal('20'), high_price = Decimal('23'), low_price = Decimal('20'), volume = int(100), interval = Interval.DAILY), 
                            ]
                        }, 
                    'expected': {
                        'return': (False, [], Decimal('109999')),
                        'conditions': [InvestCondition(position_type = PositionType.SELL, price = Decimal('33'), volume = 303, date = date(2019, 10, 20), losscut_price = Decimal('36.3'))]
                        }
                    },
                ]

        rule = TurtleInvestRule(unit_number = 10, losscut_rate = Decimal('0.1'))
        for data in input_data: 
            conditions = data['val']['conditions']
            got = rule.losscut_short(sticks = data['val']['sticks'], conditions = conditions, cash = data['val']['cash'])
            self.assertEqual(data['expected']['return'], got) 
            self.assertEqual(data['expected']['conditions'], conditions) 

