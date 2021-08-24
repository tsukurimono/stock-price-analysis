from typing   import ClassVar, List
import csv
import asciichartpy

from app.util.exception import DataNotfoundAppException, UnauthorizedAppException, InconsistencyDataException

from app.usecase.stock           import StockUsecase
from app.usecase.inputdata.stock import *

from app.controller.stock  import  StockController

from app.domain.stock import Candlestick
from app.domain.analyze import TrendType
from app.domain.invest import PositionType, InvestRuleType

import re

class CliStockController(StockController):

    stock_usecase:       StockUsecase

    def __init__(self, stock_usecase: StockUsecase):
        self.stock_usecase = stock_usecase

    # ---------------------------------------------------------------------------------
    # Simulate the trade rule.
    # ---------------------------------------------------------------------------------
    def simulate_trade_rule(self, rule_type:str, code:str, market:str, tags:List[str], unit:int, losscut_rate:str, today:str, term:int, principal:str, commission_max:str, commission_min:str, commission_rate:str, is_summary:bool, loop_num:int):
        (today_year, today_month, today_day) = today.split('-')

        invest_rule_type = None
        if rule_type == 'random':
            invest_rule_type = InvestRuleType.RANDOM
        elif rule_type == 'randlong':
            invest_rule_type = InvestRuleType.RANDOM_LONG
        elif rule_type == 'randtrail':
            invest_rule_type = InvestRuleType.RANDOM_TRAIL
        elif rule_type == 'goldentrail':
            invest_rule_type = InvestRuleType.GOLDEN_TRAIL
        elif rule_type == 'serialstepuptrail':
            invest_rule_type = InvestRuleType.SERIAL_STEPUP_TRAIL
        elif rule_type == 'triplestepuptrail':
            invest_rule_type = InvestRuleType.TRIPLE_STEPUP_TRAIL
        elif rule_type == 'buyhold':
            invest_rule_type = InvestRuleType.BUYHOLD
        else:
            invest_rule_type = InvestRuleType.TURTLE
                        
        outputdata = []
        try:
            for i in range(loop_num):
                outputdata.append(self.stock_usecase.simulate_trade_rule( 
                        input_data = SimulateTradeRuleInput(
                            rule_type    = invest_rule_type,
                            code         = code,
                            market       = market, 
                            tags         = tags,
                            unit         = unit,
                            losscut_rate = Decimal(losscut_rate),
                            today        = date(int(today_year), int(today_month), int(today_day)),
                            term         = term,
                            principal    = Decimal(principal),
                            commission   = StandardCommission(minimum = Decimal(commission_min), maximum = Decimal(commission_max), rate = Decimal(commission_rate))
                            )
                        ))
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        if outputdata == []:
            return ''

        result = ''
        
        if not is_summary:
            for (index, item) in enumerate(outputdata):
                r = item.report
                result += "----------------------------------------------------------------------------------------------------------------------------------------------\n"
                result += f"[Summery {index+1}/{loop_num}]\n\n"
                result += f"|{'Principal':>20}|{'Current Valuation':>20}|{'Commission':>20}\n" 
                result += f"|{'':->20}|{'':->20}|{'':->20}|\n" 
                result += f"|{r.principal:>20,.7f}|{r.current_valuation:>20,.7f}|{r.commission:>20,.7f}|\n" 
                result += f"|{'':->20}|{'':->20}|{'':->20}|\n" 
                result += "\n"
                result += f"|{'Mean Profit':>20}|{'Mean Loss':>20}|{'Win Rate':>20}|{'Lose Rate':>20}|{'Payoff Ratio':>20}|\n" 
                result += f"|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|\n" 
                result += f"|{r.mean_profit:>20.7f}|{r.mean_loss:>20.7f}|{r.win_rate:>20.7f}|{r.lose_rate:>20.7f}|{r.payoff_ratio:>20.7f}|\n" 
                result += "\n"
                result += "[Transaction Details]\n\n"
                result += f"{'':>21}|{'Open':>41}|{'Close':>41}|\n" 
                result += f"|{'':>20}|{'':->41}|{'':->41}|\n" 
                result += f"|{'Ticker':>20}|{'Date':>20}|{'Price':>20}|{'Date':>20}|{'Price':>20}|{'Type':>10}|{'Volume':>20}|{'Profit':>20}|\n" 
                result += f"|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->10}|{'':->20}|{'':->20}|\n" 

                for (key, histories) in r.histories.items(): 
                    for h in histories: 
                        result += f"|{key:>20}|{h.open_date.strftime('%Y-%m-%d'):>20}"
                        result += f"|{h.open_price:>20.7f}|{h.close_date.strftime('%Y-%m-%d'):>20}|{h.close_price:>20.7f}"
                        result += f"|{'Buy' if h.position_type == PositionType.BUY else 'Sell':>10}"
                        result += f"|{h.volume:>20}|{h.profit():>20.7f}|\n"

                result += "\n"
                result += "[Position]\n\n"
                result += f"|{'Ticker':>20}|{'Date':>20}|{'Price':>20}|{'Type':>10}|{'Volume':>20}|\n" 
                result += f"|{'':->20}|{'':->20}|{'':->20}|{'':->10}|{'':->20}|\n" 

                for (key, positions) in r.positions.items(): 
                    for p in positions: 
                        result += f"|{key:>20}|{p.date.strftime('%Y-%m-%d'):>20}" 
                        result += f"|{p.price:>20.7f}" 
                        result += f"|{'Buy' if p.position_type == PositionType.BUY else 'Sell':>10}" 
                        result += f"|{p.volume:>20}|\n"
        else:
            result += "----------------------------------------------------------------------------------------------------------------------------------------------\n"
            result += f"|{'Current Valuation':>20}|{'Commission':>20}|{'Mean Profit':>20}|{'Mean Loss':>20}|{'Win Rate':>20}|\n" 
            for (index, item) in enumerate(outputdata): 
                r = item.report
                result += f"|{r.current_valuation:>20,.7f}|{r.commission:>20,.7f}|{r.mean_profit:>20.7f}|{r.mean_loss:>20.7f}|{r.win_rate:>20.7f}|\n" 


        return result
        

    # ---------------------------------------------------------------------------------
    # Load candlesticks.
    # ---------------------------------------------------------------------------------
    def load_candlesticks(self, filename:str, safe:bool):
        csv_file = open(filename, "r", errors="", newline="" )
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        header = next(f) # Discard header part.

        sticks = []
        for row in f: 
            date_split = re.split(r"\s+|\/|:", row[2]) 
            sticks.append(
                    Candlestick( 
                        code        = row[0], 
                        market      = row[1], 
                        date        = date(int(date_split[0]), int(date_split[1]), int(date_split[2])), 
                        open_price  = Decimal(row[3]), 
                        close_price = Decimal(row[6]), 
                        high_price  = Decimal(row[4]), 
                        low_price   = Decimal(row[5]), 
                        volume      = int(row[7]), 
                        interval    = Interval.DAILY
                        )
                    )
        result = ''
        try:
            outputdata = self.stock_usecase.create_candlestick( 
                    input_data = CreateCandlestickInput(
                        candlesticks = sticks,
                        safe         = safe
                        )
                    )
        except InconsistencyDataException as e:
            result += f"|{'':>10}|{'Symbol':>20}|{'Date':>12}|{'Open Price':>20}|{'Close Price':>20}|{'High Price':>20}|{'Low Price':>20}|{'Volume':>20}|{'Interval':>10}|{'Patched':>10}|\n" 
            for (present, newer) in list(zip(e.present, e.newer)):
                result += f"|{'':->10}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->10}|{'':->10}|\n" 
                result += f"|{'Present':>10}|{present.code:>20}|{present.date.strftime('%Y-%m-%d'):>12}|{present.open_price:>20}|{present.close_price:>20}|{present.high_price:>20}|{present.low_price:>20}|{present.volume:>20}|{present.interval:>10}|{present.patched:>10}|\n"
                result += f"|{'Newer':>10}|{newer.code:>20}|{newer.date.strftime('%Y-%m-%d'):>12}|{newer.open_price:>20}|{newer.close_price:>20}|{newer.high_price:>20}|{newer.low_price:>20}|{newer.volume:>20}|{newer.interval:>10}|{newer.patched:>10}|\n"

        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return result

    # ---------------------------------------------------------------------------------
    # Load tags.
    # ---------------------------------------------------------------------------------
    def load_tags(self, filename:str):
        csv_file = open(filename, "r", errors="", newline="" )
        f = csv.reader(csv_file, delimiter="\t", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        stocks = []
        for row in f: 
            syntax_split = re.split(r"\s+|:", row[0]) 
            tag_split = re.split(r"\s+|,", row[1]) 
            stocks.append(Stock(
                code   = syntax_split[1], 
                market = syntax_split[0], 
                tags   = tag_split
                ))

        result = ''
        try:
            outputdata = self.stock_usecase.create_tag( 
                    input_data = CreateTagInput(
                        stocks = stocks
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return result

    # ---------------------------------------------------------------------------------
    # Get stock prices.
    # ---------------------------------------------------------------------------------
    def get_stock_prices(self, code:str, market:str, from_date:str, to_date:str, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_candlesticks( 
                    input_data = GetCandlesticksInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day))
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        if chart:
            result = asciichartpy.plot([stick.close_price for stick in outputdata.candlesticks], {'height': 30})
        else: 
            for stick in outputdata.candlesticks:
                result += f"{stick.date.strftime('%Y-%m-%d')},{stick.close_price}\n"

        return result

    # ---------------------------------------------------------------------------------
    # Get stock volumes.
    # ---------------------------------------------------------------------------------
    def get_stock_volumes(self, code:str, market:str, from_date:str, to_date:str, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_candlesticks( 
                    input_data = GetCandlesticksInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day))
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        scale  = ''
        if chart:
            maxPrice = max([stick.close_price for stick in outputdata.candlesticks])
            priceScale = len(str(int(str(maxPrice).split('.')[0])))
            maxVolume = max([stick.volume for stick in outputdata.candlesticks])
            volumeScale = len(str(int(str(maxVolume).split('.')[0])))
            scale = f"x{10**(volumeScale - priceScale):,}"

            result = asciichartpy.plot([stick.volume/10**(volumeScale - priceScale)  for stick in outputdata.candlesticks], {'height': 20})
        else: 
            for stick in outputdata.candlesticks:
                result += f"{stick.date.strftime('%Y-%m-%d')},{stick.volume}\n"

        return result, scale

    # ---------------------------------------------------------------------------------
    # Search ticker symbols .
    # ---------------------------------------------------------------------------------
    def search_tickersymbols(self, keyword:str):
        outputdata = None
        try:
            outputdata = self.stock_usecase.search_tickers(
                    input_data = SearchTickersInput(keyword = keyword)
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        for ticker in outputdata.tickers:
            result += f"{ticker.market}:{ticker.code}\n"

        return result

    # ---------------------------------------------------------------------------------
    # Search market symbols .
    # ---------------------------------------------------------------------------------
    def search_marketsymbols(self, keyword:str):
        outputdata = None
        try:
            outputdata = self.stock_usecase.search_markets(
                    input_data = SearchMarketsInput(keyword = keyword)
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result  = f"|{'':->20}|\n"
        result += f"|{'Markets':>20}|\n"
        result += f"|{'':->20}|\n"
        for market in outputdata.markets:
            result += f"|{market:>20}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Search tags.
    # ---------------------------------------------------------------------------------
    def search_tags(self, keyword:str):
        outputdata = None
        try:
            outputdata = self.stock_usecase.search_tags(
                    input_data = SearchTagsInput(keyword = keyword)
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result  = f"|{'':->20}|\n"
        result += f"|{'Tags':>20}|\n"
        result += f"|{'':->20}|\n"
        for tag in outputdata.tags:
            result += f"|{tag:>20}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Get stock price SMA.
    # ---------------------------------------------------------------------------------
    def get_stock_price_smas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_sma( 
                    input_data = CalcurateSmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result = ''
        if chart:
            prices = [unit.price for unit in outputdata.data]
            smas   = [unit.price_sma for unit in outputdata.data]

            result = asciichartpy.plot([prices, smas], {'colors': [asciichartpy.black,asciichartpy.green],'height': 30})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.price},{unit.price_sma}\n"

        return result


    # ---------------------------------------------------------------------------------
    # Get stock volume SMA.
    # ---------------------------------------------------------------------------------
    def get_stock_volume_smas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_sma( 
                    input_data = CalcurateSmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        scale  = ''
        if chart:
            maxPrice = max([stick.price for stick in outputdata.data])
            priceScale = len(str(int(str(maxPrice).split('.')[0])))
            maxVolume = max([stick.volume for stick in outputdata.data])
            volumeScale = len(str(int(str(maxVolume).split('.')[0])))
            scale = f"x{10**(volumeScale - priceScale)}"

            volumes = [unit.volume/10**(volumeScale - priceScale)  for unit in outputdata.data]
            smas    = [unit.volume_sma/10**(volumeScale - priceScale)  for unit in outputdata.data]

            result = asciichartpy.plot([volumes, smas], {'colors': [asciichartpy.black,asciichartpy.green], 'height': 20})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.volume},{unit.volume_sma}\n"

        return result, scale

    # ---------------------------------------------------------------------------------
    # Get stock price WMA.
    # ---------------------------------------------------------------------------------
    def get_stock_price_wmas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_wma( 
                    input_data = CalcurateWmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        if chart:
            prices = [unit.price for unit in outputdata.data]
            wmas   = [unit.price_wma for unit in outputdata.data]
            result = asciichartpy.plot([prices, wmas], {'colors': [asciichartpy.black,asciichartpy.green],'height': 30})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.price},{unit.price_wma}\n"

        return result


    # ---------------------------------------------------------------------------------
    # Get stock volume WMA.
    # ---------------------------------------------------------------------------------
    def get_stock_volume_wmas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_wma( 
                    input_data = CalcurateWmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            pass

        result = ''
        scale  = ''
        if chart:
            maxPrice = max([stick.price for stick in outputdata.data])
            priceScale = len(str(int(str(maxPrice).split('.')[0])))
            maxVolume = max([stick.volume for stick in outputdata.data])
            volumeScale = len(str(int(str(maxVolume).split('.')[0])))
            scale = f"x{10**(volumeScale - priceScale):,}"

            volumes = [unit.volume/10**(volumeScale - priceScale)  for unit in outputdata.data]
            wmas    = [unit.volume_wma/10**(volumeScale - priceScale)  for unit in outputdata.data]

            result = asciichartpy.plot([volumes, wmas], {'colors': [asciichartpy.black,asciichartpy.green], 'height': 20})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.volume},{unit.volume_wma}\n"

        return result, scale

    # ---------------------------------------------------------------------------------
    # Get stock price EMA.
    # ---------------------------------------------------------------------------------
    def get_stock_price_emas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_ema( 
                    input_data = CalcurateWmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result = ''
        if chart:
            prices = [unit.price for unit in outputdata.data]
            emas   = [unit.price_ema for unit in outputdata.data]
            result = asciichartpy.plot([prices, emas], {'colors': [asciichartpy.black,asciichartpy.green],'height': 30})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.price},{unit.price_ema}\n"

        return result


    # ---------------------------------------------------------------------------------
    # Get stock volume EMA.
    # ---------------------------------------------------------------------------------
    def get_stock_volume_emas(self, code:str, market:str, from_date:str, to_date:str, term:int, chart:bool):
        (from_year, from_month, from_day) = from_date.split('-')
        (to_year, to_month, to_day)       = to_date.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.calcurate_ema( 
                    input_data = CalcurateWmaInput(
                        code      = code,
                        market    = market,
                        from_date = date(int(from_year), int(from_month), int(from_day)),
                        to_date   = date(int(to_year), int(to_month), int(to_day)),
                        term      = term
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result = ''
        scale  = ''
        if chart:
            maxPrice = max([stick.price for stick in outputdata.data])
            priceScale = len(str(int(str(maxPrice).split('.')[0])))
            maxVolume = max([stick.volume for stick in outputdata.data])
            volumeScale = len(str(int(str(maxVolume).split('.')[0])))
            scale = f"x{10**(volumeScale - priceScale)}"

            volumes = [unit.volume/10**(volumeScale - priceScale)  for unit in outputdata.data]
            emas    = [unit.volume_ema/10**(volumeScale - priceScale)  for unit in outputdata.data]

            result = asciichartpy.plot([volumes, emas], {'colors': [asciichartpy.black,asciichartpy.green], 'height': 20})
        else: 
            for unit in outputdata.data:
                result += f"{unit.date.strftime('%Y-%m-%d')},{unit.volume},{unit.volume_ema}\n"

        return result, scale

    # ---------------------------------------------------------------------------------
    # Ranking price.
    # ---------------------------------------------------------------------------------
    def ranking_price(self, market:str, tags:List[str], today:str, term:int, order:str, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_ranking_price( 
                    input_data   = GetRankingPriceInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        term     = term,
                        order    = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result = f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->10}|\n"
        result += f"|{'Symbol':>20}|{'Base date':>12}|{'Base value':>20}|{'Present date':>12}|{'Present value':>20}|{'Rate':>10}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->10}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.base_date.strftime('%Y-%m-%d'):>12}|{row.base_value:20.7f}|{row.present_date.strftime('%Y-%m-%d'):>12}|{row.present_value:20.7f}|{row.change_rate():+10.3f}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Ranking volume.
    # ---------------------------------------------------------------------------------
    def ranking_volume(self, market:str, tags:List[str], today:str, term:int, order:str, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_ranking_volume( 
                    input_data   = GetRankingVolumeInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        term     = term,
                        order    = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result = f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->10}|\n"
        result += f"|{'Symbol':>20}|{'Base date':>12}|{'Base value':>20}|{'Present date':>12}|{'Present value':>20}|{'Rate':>10}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->10}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.base_date.strftime('%Y-%m-%d'):>12}|{row.base_value:20.7f}|{row.present_date.strftime('%Y-%m-%d'):>12}|{row.present_value:20.7f}|{row.change_rate():+10.3f}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Ranking relative strength.
    # ---------------------------------------------------------------------------------
    def ranking_relative_strength(self, market:str, tags:List[str], today:str, order:str, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_ranking_rs( 
                    input_data   = GetRankingRsInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        order    = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result =  f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'Date':>12}|{'Price':>20}|{'Date63':>12}|{'Price63':>20}|{'Date126':>12}|{'Price126':>20}|{'Date189':>12}|{'Price189':>20}|{'Date252':>12}|{'Price252':>20}|{'Score':>20}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.stick.date.strftime('%Y-%m-%d'):>12}|{row.stick.close_price:20.7f}|{row.stick63.date.strftime('%Y-%m-%d'):>12}|{row.stick63.close_price:20.7f}|{row.stick126.date.strftime('%Y-%m-%d'):>12}|{row.stick126.close_price:20.7f}|{row.stick189.date.strftime('%Y-%m-%d'):>12}|{row.stick189.close_price:20.7f}|{row.stick252.date.strftime('%Y-%m-%d'):>12}|{row.stick252.close_price:20.7f}|{row.point:>20}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Ranking standard deviation.
    # ---------------------------------------------------------------------------------
    def ranking_deviation(self, market:str, tags:List[str], today:str, longterm:int, shortterm:int, order:str, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_ranking_deviation( 
                    input_data    = GetRankingDeviationInput(
                        market    = market,
                        tags      = tags,
                        today     = date(int(today_year), int(today_month), int(today_day)),
                        longterm  = longterm,
                        shortterm = shortterm,
                        order     = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit     = limit,
                        offset    = offset,
                        cache     = cache,
                        cachekey  = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result =  f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'From(Long)':>12}|{'Deviation(L)':>20}|{'From(Short)':>12}|{'Deviation(S)':>20}|{'Rate':>20}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.base_date.strftime('%Y-%m-%d'):>12}|{row.base_value:20.7f}|{row.present_date.strftime('%Y-%m-%d'):>12}|{row.present_value:20.7f}|{row.rate():20.7f}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Trned price.
    # ---------------------------------------------------------------------------------
    def trend_price(self, market:str, tags:List[str], today:str, sorttype:str, margin:int, term:int, smaterm:int, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_trend_price( 
                    input_data   = GetTrendPriceInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        sorttype = TrendType.UP if sorttype == 'up' else TrendType.DOWN,
                        margin   = margin,
                        term     = term,
                        smaterm  = smaterm,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result =  f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'From Date':>12}|{'To Date':>12}|{'UP':>20}|{'Down':>20}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.from_date.strftime('%Y-%m-%d'):>12}|{row.to_date.strftime('%Y-%m-%d'):>12}|{row.up:>20}|{row.down:>20}|\n"
        return result

    # ---------------------------------------------------------------------------------
    # Trned volume.
    # ---------------------------------------------------------------------------------
    def trend_volume(self, market:str, tags:List[str], today:str, sorttype:str, margin:int, term:int, smaterm:int, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_trend_volume( 
                    input_data   = GetTrendVolumeInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        sorttype = TrendType.UP if sorttype == 'up' else TrendType.DOWN,
                        margin   = margin,
                        term     = term,
                        smaterm  = smaterm,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result =  f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'From Date':>12}|{'To Date':>12}|{'UP':>20}|{'Down':>20}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.from_date.strftime('%Y-%m-%d'):>12}|{row.to_date.strftime('%Y-%m-%d'):>12}|{row.up:>20}|{row.down:>20}|\n"
        return result

    # ---------------------------------------------------------------------------------
    # Trned momentum.
    # ---------------------------------------------------------------------------------
    def trend_momentum(self, market:str, tags:List[str], today:str, sorttype:str, margin:int, term:int, smaterm:int, limit:int, offset:int, cache:bool, cachekey:str):
        (today_year, today_month, today_day) = today.split('-')

        outputdata = None
        try:
            outputdata = self.stock_usecase.get_trend_momentum( 
                    input_data   = GetTrendMomentumInput(
                        market   = market,
                        tags     = tags,
                        today    = date(int(today_year), int(today_month), int(today_day)),
                        sorttype = TrendType.UP if sorttype == 'up' else TrendType.DOWN,
                        margin   = margin,
                        term     = term,
                        smaterm  = smaterm,
                        limit    = limit,
                        offset   = offset,
                        cache    = cache,
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            # TODO: Handle exception.
            print(e)
            pass

        result =  f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'From Date':>12}|{'To Date':>12}|{'UP':>20}|{'Down':>20}|\n"
        result += f"|{'':->20}|{'':->12}|{'':->12}|{'':->20}|{'':->20}|\n"
        for row in outputdata.data:
            result += f"|{row.code:>20}|{row.from_date.strftime('%Y-%m-%d'):>12}|{row.to_date.strftime('%Y-%m-%d'):>12}|{row.up:>20}|{row.down:>20}|\n"
        return result

    # ---------------------------------------------------------------------------------
    # Reflect Stocksplit.
    # ---------------------------------------------------------------------------------
    def reflect_stocksplit(self, code:str, market:str, present_price:str, newer_price:str, target_date:str):
        (target_year, target_month, target_day) = target_date.split('-')

        result = ''
        try:
            outputdata = self.stock_usecase.reflect_stocksplit( 
                    input_data = ReflectStocksplitInput(
                        code          = code,
                        market        = market,
                        present_price = Decimal(present_price),
                        newer_price   = Decimal(newer_price),
                        target_date   = date(int(target_year), int(target_month), int(target_day))
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return result

    # ---------------------------------------------------------------------------------
    # Clear cache data of the target market.
    # ---------------------------------------------------------------------------------
    def clear_cachedata(self, cachekey:str):
        result = ''
        try:
            outputdata = self.stock_usecase.clear_cachedata(
                    input_data = ClearCachedataInput(
                        cachekey = cachekey
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return result

    # ---------------------------------------------------------------------------------
    # Multiple cache data of the target market.
    # ---------------------------------------------------------------------------------
    def multiple_cachedata(self, cachekey:str, coefficient:str):
        result = ''
        try:
            outputdata = self.stock_usecase.multiple_cachedata(
                    input_data = MultipleCachedataInput(
                        cachekey           = cachekey,
                        coefficient        = Decimal(coefficient),
                        additional_ranking = []
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return result

    # ---------------------------------------------------------------------------------
    # Show cache data of the target market.
    # ---------------------------------------------------------------------------------
    def show_cachedata(self, cachekey:str, limit:int, offset:int):
        result = ''
        try:
            outputdata = self.stock_usecase.get_cachedata(
                    input_data = GetCachedataInput(
                        cachekey = cachekey,
                        limit    = limit,
                        offset   = offset
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result =  f"|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'Score':>20}|\n"
        result += f"|{'':->20}|{'':->20}|\n"
        for score in outputdata.scores:
            result += f"|{score.code:>20}|{score.score:>20.7f}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Get stocks in the ATH.
    # ---------------------------------------------------------------------------------
    def get_ath(self, market:str, tags:List[str], term:int, base_date:str):
        (base_year, base_month, base_day) = base_date.split('-')

        result = ''
        try:
            outputdata = self.stock_usecase.get_ath(
                    input_data = GetAthInput(
                        market    = market,
                        tags      = tags,
                        term      = term,
                        base_date = date(int(base_year), int(base_month), int(base_day))
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result =  f"|{'':->20}|{'':->12}|\n"
        result += f"|{'Symbol':>20}|{'Date':>12}|\n"
        result += f"|{'':->20}|{'':->12}|\n"
        for candlestick in outputdata.candlesticks:
            result += f"|{candlestick.code:>20}|{candlestick.date.strftime('%Y-%m-%d'):>12}|\n"

        result += f"Total: {len(outputdata.candlesticks)}"

        return result

    # ---------------------------------------------------------------------------------
    # Get stocks in the ATL.
    # ---------------------------------------------------------------------------------
    def get_atl(self, market:str, tags:List[str], term:int, base_date:str):
        (base_year, base_month, base_day) = base_date.split('-')

        result = ''
        try:
            outputdata = self.stock_usecase.get_atl(
                    input_data = GetAtlInput(
                        market    = market,
                        tags      = tags,
                        term      = term,
                        base_date = date(int(base_year), int(base_month), int(base_day))
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result =  f"|{'':->20}|{'':->12}|\n"
        result += f"|{'Symbol':>20}|{'Date':>12}|\n"
        result += f"|{'':->20}|{'':->12}|\n"
        for candlestick in outputdata.candlesticks:
            result += f"|{candlestick.code:>20}|{candlestick.date.strftime('%Y-%m-%d'):>12}|\n"

        result += f"Total: {len(outputdata.candlesticks)}"

        return result

    # ---------------------------------------------------------------------------------
    # Get average ATR.
    # ---------------------------------------------------------------------------------
    def get_average_atr(self, code:str, market:str, term:int, today:str):
        (today_year, today_month, today_day) = today.split('-')

        result = ''
        try:
            outputdata = self.stock_usecase.get_average_atr(
                    input_data = GetAverageAtrInput(
                        code   = code,
                        market = market,
                        term   = term,
                        today  = date(int(today_year), int(today_month), int(today_day))
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result =  f"|{'':->20}|{'':->20}|\n"
        result += f"|{'Symbol':>20}|{'ATR':>20}|\n"
        result += f"|{'':->20}|{'':->20}|\n"
        result += f"|{code:>20}|{outputdata.average_atr:>20.7f}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Predict setup signal.
    # ---------------------------------------------------------------------------------
    def predict_setupsignal(self, code:str, market:str, tags:List[str], rule_type:str, base_date:str):
        (today_year, today_month, today_day) = base_date.split('-')

        invest_rule_type = None
        if rule_type == 'random':
            invest_rule_type = InvestRuleType.RANDOM
        elif rule_type == 'randlong':
            invest_rule_type = InvestRuleType.RANDOM_LONG
        elif rule_type == 'randtrail':
            invest_rule_type = InvestRuleType.RANDOM_TRAIL
        elif rule_type == 'goldentrail':
            invest_rule_type = InvestRuleType.GOLDEN_TRAIL
        elif rule_type == 'serialstepuptrail':
            invest_rule_type = InvestRuleType.SERIAL_STEPUP_TRAIL
        elif rule_type == 'buyhold':
            invest_rule_type = InvestRuleType.BUYHOLD
        else:
            invest_rule_type = InvestRuleType.TURTLE

        result = ''
        try:
            outputdata = self.stock_usecase.predict_setup_signal(
                    input_data = PredictSetupSignalInput(
                        rule_type = invest_rule_type,
                        code      = code,
                        market    = market,
                        tags      = tags,
                        today     = date(int(today_year), int(today_month), int(today_day))
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result =  f"|{'':->20}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|\n"
        result += f"|{'Market':>20}|{'Ticker':>20}|{'Date':>12}|{'Open':>20}|{'Close':>20}|{'High':>20}|{'Low':>20}|{'Volume':>20}|\n"
        result += f"|{'':->20}|{'':->20}|{'':->12}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|{'':->20}|\n"

        for stick in outputdata.candlesticks: 
            result += f"|{stick.market:>20}|{stick.code:>20}|{stick.date.strftime('%Y-%m-%d'):>12}|{stick.open_price:>20}|{stick.close_price:>20}|{stick.high_price:>20}|{stick.low_price:>20}|{stick.volume:>20}|\n"

        result += f"Total: {len(outputdata.candlesticks)}"

        return result

    # ---------------------------------------------------------------------------------
    # Delistings the sticks data.
    # ---------------------------------------------------------------------------------
    def delistings_sticks(self, code:str, market:str):
        result = ''
        try:
            outputdata = self.stock_usecase.delisting_stock(
                    input_data = DelistingStockInput(
                        code      = code,
                        market    = market,
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return True

    # ---------------------------------------------------------------------------------
    # Listings the sticks data.
    # ---------------------------------------------------------------------------------
    def listings_sticks(self, code:str, market:str):
        result = ''
        try:
            outputdata = self.stock_usecase.listing_stock(
                    input_data = ListingStockInput(
                        code      = code,
                        market    = market,
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return True

    # ---------------------------------------------------------------------------------
    # Get first date of the all stocks.
    # ---------------------------------------------------------------------------------
    def stock_firstdate(self, order:str, limit:int, offset:int):
        try:
            outputdata = self.stock_usecase.get_each_firststick(
                    input_data = GetEachFirststickInput(
                        order  = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit  = limit,
                        offset = offset,
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result  = f"|{'':->40}|{'':->12}|\n"
        result += f"|{'Market:Ticker':>40}|{'First date':>12}|\n"
        result += f"|{'':->40}|{'':->12}|\n"

        for term in outputdata.terms: 
            result += f"|{term.market + ':' + term.code:>40}|{term.first_date.strftime('%Y-%m-%d'):>12}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Get last date of the all stocks.
    # ---------------------------------------------------------------------------------
    def stock_lastdate(self, order:str, limit:int, offset:int):
        try:
            outputdata = self.stock_usecase.get_each_laststick(
                    input_data = GetEachLaststickInput(
                        order  = RankingOrder.ASC if order == 'asc' else RankingOrder.DESC,
                        limit  = limit,
                        offset = offset,
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        result  = f"|{'':->40}|{'':->12}|\n"
        result += f"|{'Market:Ticker':>40}|{'First date':>12}|\n"
        result += f"|{'':->40}|{'':->12}|\n"

        for term in outputdata.terms: 
            result += f"|{term.market + ':' + term.code:>40}|{term.last_date.strftime('%Y-%m-%d'):>12}|\n"

        return result

    # ---------------------------------------------------------------------------------
    # Make cachetag from cache data.
    # ---------------------------------------------------------------------------------
    def make_cachetag(self, cachekey:str, limit:int):
        try:
            outputdata = self.stock_usecase.make_cachetag(
                    input_data = MakeCachetagInput(
                        cachekey = cachekey,
                        limit    = limit,
                        )
                    )
        except Exception as e:
            print(e)
            # TODO: Handle exception.
            pass

        return True
