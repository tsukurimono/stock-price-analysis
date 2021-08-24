import sys
import code
import readline
import atexit
import os

from app.di.default.di import DefaultDIContainer
from decimal import Decimal
from datetime import date
import datetime
from typing import List
import re

from app.domain.stock import Interval, Candlestick
from app.usecase.inputdata.stock import CreateCandlestickInput
from app.controller.stock import StockController

from dataclasses import dataclass

class StockPriceAnalysisConsole(code.InteractiveConsole):
    @dataclass
    class CommonParameter:
        ticker:    str
        market:    str
        tags:      []
        today:     str

    @dataclass
    class ChartParameter:
        from_date: str
        to_date:   str

    @dataclass
    class SimulationParameter:
        principal:       str
        commission_min:  str
        commission_max:  str
        commission_rate: str

    controller: StockController
    common_parameter: CommonParameter
    chart_parameter: ChartParameter
    simulation_parameter: SimulationParameter

    def __init__(self, local=None, filename="<console>", histfile=os.path.expanduser("~/.console-history")):
        self.controller = DefaultDIContainer().inject_stock_controller()
        self.common_parameter = self.CommonParameter(ticker = '', market = '', tags = [], today = date.today().strftime('%Y-%m-%d')) 
        self.chart_parameter = self.ChartParameter(from_date = (date.today() - datetime.timedelta(days=300)).strftime('%Y-%m-%d'), to_date = date.today().strftime('%Y-%m-%d'))
        self.simulation_parameter = self.SimulationParameter(principal = '10000', commission_min = '0', commission_max = '22.2', commission_rate = '0.0495')

        code.InteractiveConsole.__init__(self, local, filename)
        self.init_history(histfile)

    def print_parameter(self):
        message  = "---------------------------------------------------------------------------------------------------------------------------------------------------\n"
        message += f"Market: {self.common_parameter.market:<20}| Ticker: {self.common_parameter.ticker:<20}| Tags: {','.join(self.common_parameter.tags):<80}|\n"
        message += f"From:   {self.chart_parameter.from_date:>20}| To:     {self.chart_parameter.to_date:>20}| Today:  {self.common_parameter.today:>20}|\n"
        message += f"Principal: {self.simulation_parameter.principal:>17}| Commission: (Min: {self.simulation_parameter.commission_min:>4}, Max: {self.simulation_parameter.commission_max:>4}, Rate: {self.simulation_parameter.commission_rate:>8})|"
        print(message)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(' \t\n=')
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

    def push(self, line):
        parsedline = list(filter(lambda a: a != '', line.split(' ')))
        command    = "" if len(parsedline) < 1 else parsedline[0]
        argv       = parsedline[1:]

        if command == 'quit':
            self.command_quit(argv)
        elif command == 'today':
            self.command_today(argv)
        elif command == 'listings':
            self.command_listings(argv)
        elif command == 'cachetag':
            self.command_cachetag(argv)
        elif command == 'delistings':
            self.command_delistings(argv)
        elif command == 'simulate':
            self.command_simulate(argv)
        elif command == 'ticker':
            self.command_ticker(argv)
        elif command == 'principal':
            self.command_principal(argv)
        elif command == 'predict':
            self.command_predict(argv)
        elif command == 'market':
            self.command_market(argv)
        elif command == 'tags':
            self.command_tags(argv)
        elif command == 'cacheclear':
            self.command_cacheclear(argv)
        elif command == 'cachemultiple':
            self.command_cachemultiple(argv)
        elif command == 'cacheshow':
            self.command_cacheshow(argv)
        elif command == 'syntax':
            self.command_syntax(argv)
        elif command == 'from':
            self.command_from(argv)
        elif command == 'to':
            self.command_to(argv)
        elif command == 'search':
            self.command_search(argv)
        elif command == 'marketsearch':
            self.command_marketsearch(argv)
        elif command == 'tagsearch':
            self.command_tagsearch(argv)
        elif command == 'chart':
            self.command_chart(argv)
        elif command == 'sma':
            self.command_sma(argv)
        elif command == 'wma':
            self.command_wma(argv)
        elif command == 'ema':
            self.command_ema(argv)
        elif command == 'load':
            self.command_load(argv)
        elif command == 'forceload':
            self.command_forceload(argv)
        elif command == 'help':
            self.command_help(argv)
        elif command == 'rank':
            self.command_rank(argv)
        elif command == 'trend':
            self.command_trend(argv)
        elif command == 'tagload':
            self.command_tagload(argv)
        elif command == 'stocksplit':
            self.command_stocksplit(argv)
        elif command == 'ath':
            self.command_ath(argv)
        elif command == 'atl':
            self.command_atl(argv)
        elif command == 'atr':
            self.command_atr(argv)
        elif command == 'lastdate':
            self.command_lastdate(argv)
        elif command == 'firstdate':
            self.command_firstdate(argv)

        self.print_parameter()

    def command_quit(self, argv:List[str]):
        sys.exit()

    def command_listings(self, argv:List[str]):
        if len(argv) > 0: 
            parsed = argv[0].split(':')
            _ = self.controller.listings_sticks(
                    code   = parsed[1],
                    market = parsed[0],
                    )

    def command_delistings(self, argv:List[str]):
        if len(argv) > 0: 
            parsed = argv[0].split(':')
            _ = self.controller.delistings_sticks(
                    code   = parsed[1],
                    market = parsed[0],
                    )

    def command_simulate(self, argv:List[str]):
        isdecimal_lambda = lambda x: len(x.split('.')) < 3 and all([a.isdigit() for a in x.split('.')])

        if len(argv) > 3 and (argv[0] in ['turtle', 'random', 'randlong', 'randtrail', 'goldentrail', 'serialstepuptrail', 'triplestepuptrail', 'buyhold']) and argv[1].isdigit() and isdecimal_lambda(argv[2]) and argv[3].isdigit(): 
            message = self.controller.simulate_trade_rule(
                    rule_type       = argv[0],
                    code            = self.common_parameter.ticker, 
                    market          = self.common_parameter.market, 
                    tags            = self.common_parameter.tags, 
                    unit            = int(argv[1]),
                    losscut_rate    = argv[2],
                    today           = self.common_parameter.today,
                    term            = int(argv[3]),
                    principal       = Decimal(self.simulation_parameter.principal),
                    commission_min  = Decimal(self.simulation_parameter.commission_min),
                    commission_max  = Decimal(self.simulation_parameter.commission_max),
                    commission_rate = Decimal(self.simulation_parameter.commission_rate),
                    is_summary      = True if len(argv) > 4 and argv[4] == 'True' else False,
                    loop_num        = 1 if len(argv) < 6 or not argv[5].isdigit() else int(argv[5])
                    )
            print(message)

    def command_stocksplit(self, argv:List[str]):
        isdecimal_lambda = lambda x: len(x.split('.')) < 3 and all([a.isdigit() for a in x.split('.')])

        if len(argv) > 2 and isdecimal_lambda(argv[0]) and isdecimal_lambda(argv[1]): 
            self.controller.reflect_stocksplit(code = self.common_parameter.ticker, market = self.common_parameter.market, present_price = argv[0], newer_price = argv[1], target_date = argv[2])

    def command_ticker(self, argv:List[str]):
        self.common_parameter.ticker = "" if len(argv) < 1 else argv[0]

    def command_market(self, argv:List[str]):
        self.common_parameter.market = "" if len(argv) < 1 else argv[0]

    def command_tags(self, argv:List[str]):
        self.common_parameter.tags = [] if len(argv) < 1 else argv[0].split(',')

    def command_principal(self, argv:List[str]):
        isdecimal_lambda = lambda x: len(x.split('.')) < 3 and all([a.isdigit() for a in x.split('.')])
        self.simulation_parameter.principal = "" if len(argv) < 1 or not isdecimal_lambda(argv[0]) else argv[0]

    def command_cachetag(self, argv:List[str]):
        if len(argv) > 0 and argv[1].isdigit():
            message = self.controller.make_cachetag(
                    cachekey = argv[0],
                    limit    = int(argv[1])
                    )
            print(message)

    def command_predict(self, argv:List[str]):
        if len(argv) > 0 and (argv[0] in ['turtle', 'random', 'randlong', 'randtrail', 'goldentrail', 'serialstepuptrail', 'triplestepuptrail', 'buyhold']):
            message = self.controller.predict_setupsignal(
                    code      = self.common_parameter.ticker, 
                    market    = self.common_parameter.market, 
                    tags      = self.common_parameter.tags, 
                    rule_type = argv[0],
                    base_date = self.common_parameter.today if len(argv)==1 else argv[1]
                    )
            print(message)

    def command_cacheclear(self, argv:List[str]):
        if len(argv) == 0:
            return

        self.controller.clear_cachedata(cachekey = argv[0])

    def command_cachemultiple(self, argv:List[str]):
        if len(argv) < 2:
            return

        self.controller.multiple_cachedata(cachekey = argv[0], coefficient = argv[1])

    def command_tagload(self, argv:List[str]):
        if len(argv) < 1:
            return

        message = self.controller.load_tags(filename = argv[0])
        print(message)

    def command_cacheshow(self, argv:List[str]):
        if len(argv) < 3 or (not argv[1].isdigit()) or (not argv[2].isdigit()):
            return

        message = self.controller.show_cachedata(cachekey = argv[0], limit = int(argv[1]), offset = int(argv[2]))
        print(message)

    def command_syntax(self, argv:List[str]):
        if len(argv) == 0:
            return

        parsed = argv[0].split(':')
        if len(parsed) == 2:
            self.common_parameter.ticker = parsed[1]
            self.common_parameter.market = parsed[0]

    def command_today(self, argv:List[str]):
        self.common_parameter.today = date.today().strftime('%Y-%m-%d') if len(argv)<1 else argv[0]

    def command_from(self, argv:List[str]):
        self.chart_parameter.from_date = "" if len(argv) < 1 else argv[0]

    def command_to(self, argv:List[str]):
        self.chart_parameter.to_date = "" if len(argv) < 1 else argv[0]

    def command_search(self, argv:List[str]):
        print(self.controller.search_tickersymbols(keyword = "" if len(argv) == 0 else argv[0]))

    def command_marketsearch(self, argv:List[str]):
        print(self.controller.search_marketsymbols(keyword = "" if len(argv) == 0 else argv[0]))

    def command_tagsearch(self, argv:List[str]):
        print(self.controller.search_tags(keyword = "" if len(argv) == 0 else argv[0]))

    def command_chart(self, argv:List[str]):
        price_message = self.controller.get_stock_prices(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, chart=True)
        print("=================== Price Chart")
        print(price_message)

        volume_message, scale = self.controller.get_stock_volumes(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, chart=True)
        print(f"=================== Volume Chart ({scale})")
        print(volume_message)

    def command_sma(self, argv:List[str]):
        if len(argv) > 0 and argv[0].isdigit(): 
            price_message = self.controller.get_stock_price_smas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True) 
            print("=================== Price Chart with SMA")
            print(price_message)

            volume_message, scale = self.controller.get_stock_volume_smas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True)
            print(f"=================== Volume Chart ({scale})")
            print(volume_message)

    def command_wma(self, argv:List[str]):
        if len(argv) > 0 and argv[0].isdigit(): 
            price_message = self.controller.get_stock_price_wmas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True) 
            print("=================== Price Chart with WMA")
            print(price_message)

            volume_message, scale = self.controller.get_stock_volume_wmas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True)
            print(f"=================== Volume Chart ({scale})")
            print(volume_message)

    def command_ema(self, argv:List[str]):
        if len(argv) > 0 and argv[0].isdigit(): 
            price_message = self.controller.get_stock_price_emas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True) 
            print("=================== Price Chart with EMA")
            print(price_message)

            volume_message, scale = self.controller.get_stock_volume_emas(code = self.common_parameter.ticker, market = self.common_parameter.market, from_date = self.chart_parameter.from_date, to_date = self.chart_parameter.to_date, term = int(argv[0]),  chart=True)
            print(f"=================== Volume Chart ({scale})")
            print(volume_message)

    def command_load(self, argv:List[str]):
        if len(argv) > 0:
            message = self.controller.load_candlesticks(filename = argv[0], safe = True)
            print(message)

    def command_ath(self, argv:List[str]):
        if len(argv) > 0:
            message = self.controller.get_ath(
                    market    = self.common_parameter.market, 
                    tags      = self.common_parameter.tags, 
                    term      = int(argv[0]),
                    base_date = self.common_parameter.today if len(argv)==1 else argv[1]
                    )
            print(message)

    def command_atl(self, argv:List[str]):
        if len(argv) > 0:
            message = self.controller.get_atl(
                    market    = self.common_parameter.market, 
                    tags      = self.common_parameter.tags, 
                    term      = int(argv[0]),
                    base_date = self.common_parameter.today if len(argv)==1 else argv[1]
                    )
            print(message)
    def command_atr(self, argv:List[str]):
        if len(argv) > 0:
            message = self.controller.get_average_atr(
                    code   = self.common_parameter.ticker,
                    market = self.common_parameter.market, 
                    term   = int(argv[0]),
                    today  = self.common_parameter.today if len(argv)==1 else argv[1]
                    )
            print(message)

    def command_forceload(self, argv:List[str]):
        if len(argv) > 0:
            message = self.controller.load_candlesticks(filename = argv[0], safe = False)
            print(message)

    def command_rank(self, argv:List[str]):
        table = ''
        if (len(argv) >= 5) and (argv[0] in ['price', 'volume']) and (argv[1] in ['asc', 'desc']) and (argv[2].isdigit()) and (argv[3].isdigit()) and (argv[4].isdigit()):
            if argv[0] == 'price': 
                table = self.controller.ranking_price( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        term     = int(argv[2]),
                        order    = argv[1],
                        limit    = int(argv[3]),
                        offset   = int(argv[4]),
                        cache    = False if len(argv) < 6 or argv[5] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 7 else argv[6]
                        )
            elif argv[0] == 'volume': 
                table = self.controller.ranking_volume( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        term     = int(argv[2]),
                        order    = argv[1],
                        limit    = int(argv[3]),
                        offset   = int(argv[4]),
                        cache    = False if len(argv) < 6 or argv[5] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 7 else argv[6]
                        )
        elif (len(argv) >= 4) and (argv[0] in ['rs']) and (argv[1] in ['asc', 'desc']) and (argv[2].isdigit()) and (argv[3].isdigit()):
            if argv[0] == 'rs': 
                table = self.controller.ranking_relative_strength( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        order    = argv[1],
                        limit    = int(argv[2]),
                        offset   = int(argv[3]),
                        cache    = False if len(argv) < 5 or argv[4] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 6 else argv[5]
                        )
        elif (len(argv) >= 6) and (argv[0] in ['deviation']) and (argv[1] in ['asc', 'desc']) and (argv[2].isdigit()) and (argv[3].isdigit()) and (argv[4].isdigit()) and (argv[5].isdigit()):
            if argv[0] == 'deviation': 
                table = self.controller.ranking_deviation( 
                        market    = self.common_parameter.market,
                        tags      = self.common_parameter.tags,
                        today     = self.common_parameter.today,
                        longterm  = int(argv[2]),
                        shortterm = int(argv[3]),
                        order     = argv[1],
                        limit     = int(argv[4]),
                        offset    = int(argv[5]),
                        cache     = False if len(argv) < 7 or argv[6] != 'True' else True,
                        cachekey  = self.common_parameter.market if len(argv) < 8 else argv[7]
                        )
        print(table)

    def command_firstdate(self, argv:List[str]):
        table = ''
        if (len(argv) >= 3) and (argv[0] in ['desc', 'asc']) and (argv[1].isdigit()) and (argv[2].isdigit()):
            table = self.controller.stock_firstdate( 
                    order  = argv[0],
                    limit  = int(argv[1]),
                    offset = int(argv[2]),
                    )
            print(table)

    def command_lastdate(self, argv:List[str]):
        table = ''
        if (len(argv) >= 3) and (argv[0] in ['desc', 'asc']) and (argv[1].isdigit()) and (argv[2].isdigit()):
            table = self.controller.stock_lastdate( 
                    order  = argv[0],
                    limit  = int(argv[1]),
                    offset = int(argv[2]),
                    )
            print(table)

    def command_trend(self, argv:List[str]):
        table = ''
        if (len(argv) >= 7) and (argv[0] in ['price', 'volume', 'momentum']) and (argv[1] in ['up', 'down']) and (argv[2].isdigit()) and (argv[3].isdigit()) and (argv[4].isdigit()) and (argv[5].isdigit()) and (argv[6].isdigit()):
            if argv[0] == 'price': 
                table = self.controller.trend_price( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        sorttype = argv[1],
                        margin   = int(argv[4]),
                        term     = int(argv[2]),
                        smaterm  = int(argv[3]),
                        limit    = int(argv[5]),
                        offset   = int(argv[6]),
                        cache    = False if len(argv) < 8 or argv[7] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 9 else argv[8]
                        )
            elif argv[0] == 'volume': 
                table = self.controller.trend_volume( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        sorttype = argv[1],
                        margin   = int(argv[4]),
                        term     = int(argv[2]),
                        smaterm  = int(argv[3]),
                        limit    = int(argv[5]),
                        offset   = int(argv[6]),
                        cache    = False if len(argv) < 8 or argv[7] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 9 else argv[8]
                        )
            elif argv[0] == 'momentum': 
                table = self.controller.trend_momentum( 
                        market   = self.common_parameter.market,
                        tags     = self.common_parameter.tags,
                        today    = self.common_parameter.today,
                        sorttype = argv[1],
                        margin   = int(argv[4]),
                        term     = int(argv[2]),
                        smaterm  = int(argv[3]),
                        limit    = int(argv[5]),
                        offset   = int(argv[6]),
                        cache    = False if len(argv) < 8 or argv[7] != 'True' else True,
                        cachekey = self.common_parameter.market if len(argv) < 9 else argv[8]
                        )
            print(table)

    def command_help(self, argv:List[str]):
        print("---------------------------------------------------------------------------------------------------------------")
        print("StockPriceAnalysis")
        print("---------------------------------------------------------------------------------------------------------------")
        print("You can use commands listed below.")
        print("")
        print("[load]")
        print("  Description:")
        print("    Load the csvfile. If inconsistency data error occurs, it will rollback and displays the data missmatched.")
        print("  Usage:")
        print("    load </path/to/the/csvfile>")
        print("")
        print("[forceload]")
        print("  Description:")
        print("    Force load the csvfile. Update all data with no check.")
        print("  Usage:")
        print("    forceload </path/to/the/csvfile>")
        print("")
        print("[search]")
        print("  Description:")
        print("    Search the ticker symbol which includes the keyword given by arg.")
        print("  Usage:")
        print("    search <keyword>")
        print("")
        print("[marketsearch]")
        print("  Description:")
        print("    Search the market symbol which includes the keyword given by arg.")
        print("  Usage:")
        print("    marketsearch <keyword>")
        print("")
        print("[tagsearch]")
        print("  Description:")
        print("    Search the tags which includes the keyword given by arg.")
        print("  Usage:")
        print("    tagsearch <keyword>")
        print("")
        print("[chart]")
        print("  Description:")
        print("    Draw the chart specified by the parameter. Set the parameter before useing this command.")
        print("  Usage:")
        print("    chart")
        print("")
        print("[sma]")
        print("  Description:")
        print("    Draw the chart with Simple Moving Average specified by the parameter. Set the parameter before useing this command.")
        print("  Usage:")
        print("    sma <term(integer)>")
        print("")
        print("[wma]")
        print("  Description:")
        print("    Draw the chart with Weighted Moving Average specified by the parameter. Set the parameter before useing this command.")
        print("  Usage:")
        print("    wma <term(integer)>")
        print("")
        print("[ema]")
        print("  Description:")
        print("    Draw the chart with Exponential Moving Average specified by the parameter. Set the parameter before useing this command.")
        print("  Usage:")
        print("    ema <term(integer)>")
        print("")
        print("[ticker]")
        print("  Description:")
        print("    Set the ticker (like ZM) to parameter.")
        print("  Usage:")
        print("    ticker <ticker symbol>")
        print("")
        print("[market]")
        print("  Description:")
        print("    Set the market (like NASDAQ or NYSE) to parameter.")
        print("  Usage:")
        print("    market <market>")
        print("")
        print("[syntax]")
        print("  Description:")
        print("    Set the ticker and market at the same time.")
        print("  Usage:")
        print("    syntax <market>:<ticker>")
        print("")
        print("[rank]")
        print("  Description:")
        print("    Show the ranking table. If you set <save cache> True, it will be affected to cache data. Default cache key is market name.")
        print("  Usage:")
        print("    rank price <order [desc|asc]> <term(integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("    rank volume <order [desc|asc]> <term(integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("    rank rs <order [desc|asc]> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("    rank deviation <order [desc|asc]> <longterm(integer)> <shortterm(integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("")
        print("[trend]")
        print("  Description:")
        print("    Show the trend table. Count the number of above(below) sma plus margin in the term.")
        print("    Momentum indicates the number of price rise/fall under big volume (which means above the sma + margin).")
        print("  Usage:")
        print("    trend price <sortkey [up|down]> <term(inteer)> <smaterm(integer)> <margin(%) (integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("    trend volume <sortkey [up|down]> <term(inteer)> <smaterm(integer)> <margin(%) (integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("    trend momentum <sortkey [up|down]> <term(inteer)> <smaterm(integer)> <margin(%) (integer)> <limit(int)> <offset(int)> <save cache(True/False) *optional> <cachekey (str) *optional>")
        print("")
        print("[stocksplit]")
        print("  Description:")
        print("    Adjusts past stock prices at the specified stock price ratio. (includes the specified day)")
        print("  Usage:")
        print("    stocksplit <specified day's close price (decimal)> <specified day's new close price(decimal)> <specified date(date)>")
        print("")
        print("[cacheclear]")
        print("  Description:")
        print("    Clear the target key's cache data.")
        print("  Usage:")
        print("    cacheclear <cachekey (str)>")
        print("")
        print("[cachemultiple]")
        print("  Description:")
        print("    Multiple the target market's cache data by coefficient.")
        print("  Usage:")
        print("    cachemultiple <cachekey (str)> <coefficient(decimal)>")
        print("")
        print("[cacheshow]")
        print("  Description:")
        print("    Show the target market's cache data")
        print("  Usage:")
        print("    cacheshow <cachekey (str)> <limit(int)> <offset(int)>")
        print("")
        print("[tagload]")
        print("  Description:")
        print("    Read the tag csv")
        print("  Usage:")
        print("    tagload <csv path>")
        print("")
        print("[cachetag]")
        print("  Description:")
        print("    Make tag from cache data. Use top <limit> number.")
        print("  Usage:")
        print("    cachetag <cache key(str)> <limit(int)>")
        print("")
        print("[tagdelete]")
        print("  Description:")
        print("    Delete tag.")
        print("  Usage:")
        print("    tagdelete <tagname (str)>")
        print("")
        print("[ath]")
        print("  Description:")
        print("    Pickup the stock which price is in the ATH on the base date.")
        print("  Usage:")
        print("    ath <term(integer)> <base date(YYYY-MM-DD) *optional>")
        print("")
        print("[atl]")
        print("  Description:")
        print("    Pickup the stock which price is in the ATL on the base date.")
        print("  Usage:")
        print("    atl <term(integer)> <base date(YYYY-MM-DD) *optional>")
        print("")
        print("[atr]")
        print("  Description:")
        print("    Calculate the stock ATR between the term.")
        print("  Usage:")
        print("    atr <term(integer)>")
        print("")
        print("[simulate]")
        print("  Description:")
        print("    Simulate the trade rule and evaluate.")
        print("  Usage:")
        print("    simulate <rule [turtle|random|randlong|randtrail|goldentrail|serialstepuptrail|triplestepuptrail|buyhold]> <unit (int)> <losscut rate(decimal)> <term(integer)> <summary (bool) *optional> <loop num (int) *optional>")
        print("")
        print("[principal]")
        print("  Description:")
        print("    Set the principal for simulation.")
        print("  Usage:")
        print("    principal <amount (decimal)>")
        print("")
        print("[predict]")
        print("  Description:")
        print("    Predict the setup signal.")
        print("  Usage:")
        print("    predict <rule [turtle|random|randlong|randtrail|goldentrail|serialstepuptrail|triplestepuptrail|buyhold]> <base date(YYYY-MM-DD) *optional>")
        print("")
        print("[listings]")
        print("  Description:")
        print("    Listings the target candlesticks data.")
        print("  Usage:")
        print("    Listings <syntax (market:ticker)>")
        print("")
        print("[delistings]")
        print("  Description:")
        print("    Delistings the target candlesticks data.")
        print("  Usage:")
        print("    delistings <syntax (market:ticker)>")
        print("")
        print("[lastdate]")
        print("  Description:")
        print("    List the last day of each stock data and sort by date.")
        print("  Usage:")
        print("    lastdate <order [desc|asc]> <limit(int)> <offset(int)>")
        print("")
        print("[firstdate]")
        print("  Description:")
        print("    List the first day of each stock data and sort by date.")
        print("  Usage:")
        print("    firstdate <order [desc|asc]> <limit(int)> <offset(int)>")
        print("")
        print("[today]")
        print("  Description:")
        print("    Set the basis date. Default value is today.")
        print("  Usage:")
        print("    today <base date (YYYY-MM-DD) *optional>")
        print("")
        print("[quit]")
        print("  Description:")
        print("    Quit this program.")
        print("  Usage:")
        print("    quit")
        print("")


if __name__ == '__main__':
    console = StockPriceAnalysisConsole()
    sys.ps1 = "(command)>> "
    sys.ps2 = "------>> "
    console.interact("### Welcome to Stock Price Analysis!!! ###")

