from app.util.exception import InvalidDataAppException, FatalAppException, DataNotfoundAppException, InconsistencyDataException
import datetime

from app.usecase.inputdata.stock  import *
from app.usecase.outputdata.stock import *

from app.repository.inputdata.stock   import *
from app.repository.outputdata.stock  import *

import app.repository.inputdata.stock  as stock_repository_inputdata

from app.usecase.stock           import StockUsecase
from app.repository.stock        import StockRepository
from app.repository.transaction  import TxContext, Transaction

from app.driver.cache            import CacheDriver

from app.domain.stock            import Candlestick, Atr
from app.domain.statistics       import Statistics
from app.domain.analyze          import RankingOrder
from app.domain.simulator        import InvestSimulator

class DefaultStockInteractor(StockUsecase):
    stock_repository:  StockRepository
    transaction:       Transaction
    cache_driver:      CacheDriver

    def __init__(self, stock_repository: StockRepository, transaction: Transaction, cache_driver: CacheDriver):
        self.stock_repository = stock_repository
        self.transaction      = transaction
        self.cache_driver     = cache_driver

    # ---------------------------------------------------------------------------------
    # Create candlestick.
    # ---------------------------------------------------------------------------------
    def create_candlestick(self, input_data: CreateCandlestickInput) -> CreateCandlestickOutput:
        candlesticks = input_data.candlesticks
        safe         = input_data.safe

        # Application Logic.
        def task(ctx: TxContext):
            can_continue = True
            errordata = {'present': [], 'newer': []}
            for stick in candlesticks:
                if safe:
                    present = self.stock_repository.find(ctx, stock_repository_inputdata.FindInput(code = stick.code, market = stick.market, date = stick.date)).candlestick
                    if present != None and present != stick:
                        errordata['present'].append(present)
                        errordata['newer'].append(stick)
                        can_continue = False

                if can_continue: 
                    self.stock_repository.save(ctx, stock_repository_inputdata.SaveInput(candlestick = stick))
            if not can_continue:
                raise InconsistencyDataException(present = errordata['present'], newer = errordata['newer'])

            return True

        try:
            self.transaction.do_in_tx(task)
        except InconsistencyDataException:
            raise
        except:
            raise FatalAppException()

        output_data = CreateCandlestickOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Create tag.
    # ---------------------------------------------------------------------------------
    def create_tag(self, input_data: CreateTagInput) -> CreateTagOutput:
        stocks = input_data.stocks

        # Application Logic.
        def task(ctx: TxContext):
            for stock in stocks:
                self.stock_repository.save_tag(ctx, stock_repository_inputdata.SaveTagInput(stock = stock))

            return True

        try:
            self.transaction.do_in_tx(task)
        except:
            raise FatalAppException()

        output_data = CreateTagOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Get candlesticks.
    # ---------------------------------------------------------------------------------
    def get_candlesticks(self, input_data: GetCandlesticksInput) -> GetCandlesticksOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get(ctx, stock_repository_inputdata.GetInput(
                code      = code,
                market    = market,
                from_date = from_date,
                to_date   = to_date
                ))

        try:
            result = self.transaction.do_in_tx(task)
        except:
            raise FatalAppException()

        output_data = GetCandlesticksOutput(
                candlesticks = result.candlesticks
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Search tickers.
    # ---------------------------------------------------------------------------------
    def search_tickers(self, input_data: SearchTickersInput) -> SearchTickersOutput:
        keyword = input_data.keyword

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.search_tickers(ctx, stock_repository_inputdata.SearchTickersInput(
                keyword = keyword,
                ))

        try:
            result = self.transaction.do_in_tx(task)
        except:
            raise FatalAppException()

        output_data = SearchTickersOutput(
                tickers = [SearchTickersOutput.Ticker(
                    code   = dto.code,
                    market = dto.market
                    ) for dto in result.tickers]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Search markets.
    # ---------------------------------------------------------------------------------
    def search_markets(self, input_data: SearchMarketsInput) -> SearchMarketsOutput:
        keyword = input_data.keyword

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.search_markets(ctx, stock_repository_inputdata.SearchMarketsInput(
                keyword = keyword,
                ))

        try:
            result = self.transaction.do_in_tx(task)
        except:
            raise FatalAppException()

        output_data = SearchMarketsOutput(
                markets = [dto for dto in result.markets]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Search tags.
    # ---------------------------------------------------------------------------------
    def search_tags(self, input_data: SearchTagsInput) -> SearchTagsOutput:
        keyword = input_data.keyword

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.search_tags(ctx, stock_repository_inputdata.SearchTagsInput(
                keyword = keyword,
                ))

        try:
            result = self.transaction.do_in_tx(task)
        except:
            raise FatalAppException()

        output_data = SearchTagsOutput(
                tags = [dto for dto in result.tags]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Calcurate SMA.
    # ---------------------------------------------------------------------------------
    def calcurate_sma(self, input_data: CalcurateSmaInput) -> CalcurateSmaOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date
        term      = input_data.term

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get(ctx, stock_repository_inputdata.GetInput(
                code      = code,
                market    = market,
                from_date = from_date,
                to_date   = to_date
                ))

        dates        = list()
        prices       = list()
        price_smas   = list()
        volumes      = list()
        volumes_smas = list()
        try:
            result      = self.transaction.do_in_tx(task)

            dates       = [dto.date for dto in result.candlesticks]
            prices      = [dto.close_price for dto in result.candlesticks]
            price_smas  = [Statistics(values = prices).sma(term = term)[0]]*(term-1) + Statistics(values = prices).sma(term = term)
            volumes     = [Decimal(dto.volume) for dto in result.candlesticks]
            volume_smas = [Statistics(values = volumes).sma(term = term)[0]]*(term-1) + Statistics(values = volumes).sma(term = term)
        except Exception as e:
            raise FatalAppException()

        output_data = CalcurateSmaOutput(
                data = [CalcurateSmaOutput.Unit(
                    date       = date,
                    price      = price, 
                    price_sma  = price_sma,
                    volume     = volume,
                    volume_sma = volume_sma,
                    ) for (date, price, price_sma, volume, volume_sma) in list(zip(dates, prices, price_smas, volumes, volume_smas))]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Calcurate WMA.
    # ---------------------------------------------------------------------------------
    def calcurate_wma(self, input_data: CalcurateWmaInput) -> CalcurateWmaOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date
        term      = input_data.term

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get(ctx, stock_repository_inputdata.GetInput(
                code      = code,
                market    = market,
                from_date = from_date,
                to_date   = to_date
                ))

        dates        = list()
        prices       = list()
        price_wmas   = list()
        volumes      = list()
        volumes_wmas = list()
        try:
            result      = self.transaction.do_in_tx(task)

            dates       = [dto.date for dto in result.candlesticks]
            prices      = [dto.close_price for dto in result.candlesticks]
            price_wmas  = [Statistics(values = prices).wma(term = term)[0]]*(term-1) + Statistics(values = prices).wma(term = term)
            volumes     = [Decimal(dto.volume) for dto in result.candlesticks]
            volume_wmas = [Statistics(values = volumes).wma(term = term)[0]]*(term-1) + Statistics(values = volumes).wma(term = term)
        except Exception as e:
            raise FatalAppException()

        output_data = CalcurateWmaOutput(
                data = [CalcurateWmaOutput.Unit(
                    date       = date,
                    price      = price, 
                    price_wma  = price_wma,
                    volume     = volume,
                    volume_wma = volume_wma,
                    ) for (date, price, price_wma, volume, volume_wma) in list(zip(dates, prices, price_wmas, volumes, volume_wmas))]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Calcurate EMA.
    # ---------------------------------------------------------------------------------
    def calcurate_ema(self, input_data: CalcurateEmaInput) -> CalcurateEmaOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date
        term      = input_data.term

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get(ctx, stock_repository_inputdata.GetInput(
                code      = code,
                market    = market,
                from_date = from_date,
                to_date   = to_date
                ))

        dates        = list()
        prices       = list()
        price_emas   = list()
        volumes      = list()
        volumes_emas = list()
        try:
            result      = self.transaction.do_in_tx(task)

            dates       = [dto.date for dto in result.candlesticks]
            prices      = [dto.close_price for dto in result.candlesticks]
            price_emas  = [Statistics(values = prices).ema(term = term)[0]]*(term-1) + Statistics(values = prices).ema(term = term)
            volumes     = [Decimal(dto.volume) for dto in result.candlesticks]
            volume_emas = [Statistics(values = volumes).ema(term = term)[0]]*(term-1) + Statistics(values = volumes).ema(term = term)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = CalcurateEmaOutput(
                data = [CalcurateEmaOutput.Unit(
                    date       = date,
                    price      = price, 
                    price_ema  = price_ema,
                    volume     = volume,
                    volume_ema = volume_ema,
                    ) for (date, price, price_ema, volume, volume_ema) in list(zip(dates, prices, price_emas, volumes, volume_emas))]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get ranking in price.
    # ---------------------------------------------------------------------------------
    def get_ranking_price(self, input_data: GetRankingPriceInput) -> GetRankingPriceOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        term     = input_data.term
        order    = input_data.order
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_all(ctx, stock_repository_inputdata.GetAllInput(
                market    = market,
                tags      = tags,
                from_date = today + datetime.timedelta(days=-term), 
                to_date   = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            performance_data = [PerformanceData(
                code          = sticks[0].code,
                market        = sticks[0].market,
                base_value    = sticks[-1].close_price,
                base_date     = sticks[-1].date,
                present_value = sticks[0].close_price,
                present_date  = sticks[0].date
                ) for (key, sticks) in output.candlesticks.items()]
            result = sorted(performance_data, key=lambda x: x.change_rate(), reverse=(order==RankingOrder.DESC))
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetRankingPriceOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get ranking in volume.
    # ---------------------------------------------------------------------------------
    def get_ranking_volume(self, input_data: GetRankingVolumeInput) -> GetRankingVolumeOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        term     = input_data.term
        order    = input_data.order
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_all(ctx, stock_repository_inputdata.GetAllInput(
                market    = market,
                tags      = tags,
                from_date = today + datetime.timedelta(days=-term), 
                to_date   = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            performance_data = [PerformanceData(
                code          = sticks[0].code,
                market        = sticks[0].market,
                base_value    = sticks[-1].volume,
                base_date     = sticks[-1].date,
                present_value = sticks[0].volume,
                present_date  = sticks[0].date
                ) for (key, sticks) in output.candlesticks.items()]
            result = sorted(performance_data, key=lambda x: x.change_rate(), reverse=(order==RankingOrder.DESC))
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetRankingVolumeOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get ranking in rs(relative strength).
    # ---------------------------------------------------------------------------------
    def get_ranking_rs(self, input_data: GetRankingRsInput) -> GetRankingRsOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        order    = input_data.order
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            c = self.stock_repository.get_each(ctx, stock_repository_inputdata.GetEachInput(
                market    = market,
                tags      = tags,
                offset    = 0,
                today     = today
                ))
            c63 = self.stock_repository.get_each(ctx, stock_repository_inputdata.GetEachInput(
                market    = market,
                tags      = tags,
                offset    = 63,
                today     = today
                ))
            c126 = self.stock_repository.get_each(ctx, stock_repository_inputdata.GetEachInput(
                market    = market,
                tags      = tags,
                offset    = 126,
                today     = today
                ))
            c189 = self.stock_repository.get_each(ctx, stock_repository_inputdata.GetEachInput(
                market    = market,
                tags      = tags,
                offset    = 189,
                today     = today
                ))
            c252 = self.stock_repository.get_each(ctx, stock_repository_inputdata.GetEachInput(
                market    = market,
                tags      = tags,
                offset    = 252,
                today     = today
                ))
            return c, c63, c126, c189, c252

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            scores = list()
            for code in output[0].candlesticks.keys(): 
                if code in output[1].candlesticks and code in output[2].candlesticks and code in output[3].candlesticks and code in output[4].candlesticks:
                    scores.append(
                            RelativeStrengthCalcurator.RawScore(
                                code       = code,
                                market     = output[0].candlesticks[code].market,
                                stick      = output[0].candlesticks[code],
                                stick63    = output[1].candlesticks[code],
                                stick126   = output[2].candlesticks[code],
                                stick189   = output[3].candlesticks[code],
                                stick252   = output[4].candlesticks[code]
                                ))
            rs = sorted(RelativeStrengthCalcurator(raw_scores = scores).relative_strength(), key=lambda x: x.rawscore, reverse=(order==RankingOrder.DESC))
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in rs]))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetRankingRsOutput(
                data = rs[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get ranking in standard deviation.
    # ---------------------------------------------------------------------------------
    def get_ranking_deviation(self, input_data: GetRankingDeviationInput) -> GetRankingDeviationOutput:
        market    = input_data.market
        tags      = input_data.tags
        today     = input_data.today
        longterm  = input_data.longterm
        shortterm = input_data.shortterm
        order     = input_data.order
        limit     = input_data.limit
        offset    = input_data.offset
        cache     = input_data.cache
        cachekey  = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = longterm,
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            temp_result = list()

            for (key, sticks) in output.candlesticks.items():
                deviation_long_term = Statistics(values = [item.close_price for item in sticks[0:longterm]]).standard_deviation()
                deviation_short_term = Statistics(values = [item.close_price for item in sticks[0:shortterm]]).standard_deviation()

                temp_result.append(PerformanceData(
                    code          = key,
                    market        = sticks[0].market,
                    base_value    = deviation_long_term,
                    base_date     = sticks[0:longterm][-1].date,
                    present_value = deviation_short_term,
                    present_date  = sticks[0:shortterm][-1].date
                    ))
            result = sorted(temp_result, key=lambda x: x.rate(), reverse=(order==RankingOrder.DESC))
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetRankingDeviationOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get trend in price.
    # ---------------------------------------------------------------------------------
    def get_trend_price(self, input_data: GetTrendPriceInput) -> GetTrendPriceOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        sorttype = input_data.sorttype
        margin   = input_data.margin
        term     = input_data.term
        smaterm  = input_data.smaterm
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = term + smaterm-1, 
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            temp_result = list()

            for (key, sticks) in output.candlesticks.items():
                close_prices = [item.close_price for item in sticks]
                statistics = Statistics(values = close_prices)
                smas = statistics.sma(term = smaterm)

                count = {'up': 0, 'down': 0}
                for (price, sma) in list(zip(close_prices[0:-(smaterm-1)], smas)):
                    if sma * (1 + Decimal(margin)/100) <= price:
                        count['up'] = count['up'] + 1
                    elif sma * (1 - Decimal(margin)/100) >= price:
                        count['down'] = count['down'] + 1

                temp_result.append(TrendData(
                    code      = key,
                    market    = sticks[0].market,
                    from_date = sticks[-1].date,
                    to_date   = sticks[0].date,
                    up        = count['up'],
                    down      = count['down']
                    ))

            result = sorted(temp_result, key=(lambda x: x.up) if sorttype==TrendType.UP else (lambda x: x.down), reverse=True)
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetTrendPriceOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get trend in volume.
    # ---------------------------------------------------------------------------------
    def get_trend_volume(self, input_data: GetTrendVolumeInput) -> GetTrendVolumeOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        sorttype = input_data.sorttype
        margin   = input_data.margin
        term     = input_data.term
        smaterm  = input_data.smaterm
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = term + smaterm-1, 
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            temp_result = list()

            for (key, sticks) in output.candlesticks.items():
                volumes = [Decimal(item.volume) for item in sticks]
                statistics = Statistics(values = volumes)
                smas = statistics.sma(term = smaterm)

                count = {'up': 0, 'down': 0}
                for (volume, sma) in list(zip(volumes[0:-(smaterm-1)], smas)):
                    if sma * (1 + Decimal(margin)/100) <= volume:
                        count['up'] = count['up'] + 1
                    elif sma * (1 - Decimal(margin)/100) >= volume:
                        count['down'] = count['down'] + 1

                temp_result.append(TrendData(
                    code      = key,
                    market    = sticks[0].market,
                    from_date = sticks[-1].date,
                    to_date   = sticks[0].date,
                    up        = count['up'],
                    down      = count['down']
                    ))

            result = sorted(temp_result, key=(lambda x: x.up) if sorttype==TrendType.UP else (lambda x: x.down), reverse=True)
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetTrendVolumeOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get trend in momentum.
    # ---------------------------------------------------------------------------------
    def get_trend_momentum(self, input_data: GetTrendMomentumInput) -> GetTrendMomentumOutput:
        market   = input_data.market
        tags     = input_data.tags
        today    = input_data.today
        sorttype = input_data.sorttype
        margin   = input_data.margin
        term     = input_data.term
        smaterm  = input_data.smaterm
        limit    = input_data.limit
        offset   = input_data.offset
        cache    = input_data.cache
        cachekey = input_data.cachekey

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = term + smaterm-1, 
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            temp_result = list()

            for (key, sticks) in output.candlesticks.items():
                volumes = [Decimal(item.volume) for item in sticks]
                close_prices = [Decimal(item.close_price) for item in sticks]
                changes = [Decimal(a - b) for (a, b) in list(zip(close_prices[0:-1], close_prices[1:]))]
                statistics = Statistics(values = volumes)
                smas = statistics.sma(term = smaterm)

                count = {'up': 0, 'down': 0}
                for (volume, change, sma) in list(zip(volumes[0:len(smas)], changes[0:len(smas)], smas)):
                    if sma * (1 + Decimal(margin)/100) <= volume:
                        if change > 0: 
                            count['up'] = count['up'] + 1
                        elif change < 0: 
                            count['down'] = count['down'] + 1

                temp_result.append(TrendData(
                    code      = key,
                    market    = sticks[0].market,
                    from_date = sticks[-1].date,
                    to_date   = sticks[0].date,
                    up        = count['up'],
                    down      = count['down']
                    ))

            result = sorted(temp_result, key=(lambda x: x.up) if sorttype==TrendType.UP else (lambda x: x.down), reverse=True)
            if cache:
                self.multiple_cachedata(input_data = MultipleCachedataInput(cachekey = cachekey, coefficient = 1, additional_ranking = [f"{value.market}:{value.code}" for value in result]))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetTrendMomentumOutput(
                data = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Reflect stock split.
    # ---------------------------------------------------------------------------------
    def reflect_stocksplit(self, input_data: ReflectStocksplitInput) -> ReflectStocksplitOutput:
        code          = input_data.code
        market        = input_data.market
        present_price = input_data.present_price
        newer_price   = input_data.newer_price
        target_date   = input_data.target_date

        # Application Logic.
        def task(ctx: TxContext):
            split_ratio = newer_price / present_price
            target_detail = self.stock_repository.get_stockdatainfo(ctx, stock_repository_inputdata.GetStockdatainfoInput(
                code   = code,
                market = market
                ))
            all_data = self.stock_repository.get_ones_all(ctx, stock_repository_inputdata.GetOnesAllInput(
                code      = code,
                market    = market,
                from_date = target_detail.first_date,
                to_date   = target_date
                )).candlesticks
            for data in all_data:
                stick = Candlestick(
                        code        = data.code,
                        market      = data.market,
                        date        = data.date,
                        open_price  = data.open_price  * split_ratio,
                        close_price = data.close_price * split_ratio,
                        high_price  = data.high_price  * split_ratio,
                        low_price   = data.low_price   * split_ratio,
                        volume      = int(Decimal(data.volume) / split_ratio),
                        interval    = Interval.DAILY
                        )
                self.stock_repository.save(ctx, stock_repository_inputdata.SaveInput(candlestick = stick))
            return True

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = ReflectStocksplitOutput(
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Clear cache data of the target market.
    # ---------------------------------------------------------------------------------
    def clear_cachedata(self, input_data: ClearCachedataInput) -> ClearCachedataOutput:
        cachekey = input_data.cachekey

        try:
            self.cache_driver.clear_dictionary(key = cachekey)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = ClearCachedataOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Multiple each stock's score in the target market.
    # ---------------------------------------------------------------------------------
    def multiple_cachedata(self, input_data: MultipleCachedataInput) -> MultipleCachedataOutput:
        cachekey = input_data.cachekey
        coefficient = input_data.coefficient
        additional_ranking = input_data.additional_ranking

        scores = dict()
        result = dict()
        try:
            scores = self.cache_driver.get_dictionary(key = cachekey)
            additional_scores = ScoreCalcurator().faster_better(data = additional_ranking)
            if len(scores) > 0: 
                for (key, score) in scores.items(): 
                    if len(additional_scores) == 0:
                        result[key] = str(Decimal(score) * Decimal(coefficient))
                    elif key in additional_scores: 
                        result[key] = str(Decimal(score) * Decimal(coefficient) * additional_scores[key])
            else: 
                for (key, score) in additional_scores.items(): 
                    result[key] = str(Decimal(score) * Decimal(coefficient))

            self.cache_driver.clear_dictionary(key = cachekey)
            self.cache_driver.save_dictionary(key = cachekey, value = result)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = MultipleCachedataOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Get cache data of the target market.
    # ---------------------------------------------------------------------------------
    def get_cachedata(self, input_data: GetCachedataInput) -> GetCachedataOutput:
        cachekey = input_data.cachekey
        limit    = input_data.limit
        offset   = input_data.offset

        result = dict()
        try:
            result = self.cache_driver.get_dictionary(key = cachekey)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetCachedataOutput(
                scores = sorted([GetCachedataOutput.StockScore(
                    code  = key,
                    score = Decimal(value)
                    ) for (key, value) in result.items()], key=lambda x: x.score, reverse=True)[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get stocks in the ATH.
    # ---------------------------------------------------------------------------------
    def get_ath(self, input_data: GetAthInput) -> GetAthOutput:
        market    = input_data.market
        tags      = input_data.tags
        term      = input_data.term
        base_date = input_data.base_date

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = term,
                to_date = base_date
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)

            for (key, sticks) in output.candlesticks.items():
                max_price = max([Decimal(item.close_price) for item in sticks])
                if max_price == sticks[0].close_price:
                    result.append(sticks[0])

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetAthOutput(
                candlesticks = result
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get stocks in the ATL.
    # ---------------------------------------------------------------------------------
    def get_atl(self, input_data: GetAtlInput) -> GetAtlOutput:
        market    = input_data.market
        tags      = input_data.tags
        term      = input_data.term
        base_date = input_data.base_date

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = '',
                market  = market,
                tags    = tags,
                limit   = term,
                to_date = base_date
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)

            for (key, sticks) in output.candlesticks.items():
                min_price = min([Decimal(item.close_price) for item in sticks])
                if min_price == sticks[0].close_price:
                    result.append(sticks[0])

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetAtlOutput(
                candlesticks = result
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get average ATR.
    # ---------------------------------------------------------------------------------
    def get_average_atr(self, input_data: GetAverageAtrInput) -> GetAverageAtrOutput:
        code   = input_data.code
        market = input_data.market
        term   = input_data.term
        today  = input_data.today

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = code,
                market  = market,
                tags    = [],
                limit   = term,
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetAverageAtrOutput(
                average_atr = Atr(candlesticks = output.candlesticks[code]).average(term)[0]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Simulate trade rule.
    # ---------------------------------------------------------------------------------
    def simulate_trade_rule(self, input_data: SimulateTradeRuleInput) -> SimulateTradeRuleOutput:
        rule_type    = input_data.rule_type
        code         = input_data.code
        market       = input_data.market
        tags         = input_data.tags
        unit         = input_data.unit
        losscut_rate = input_data.losscut_rate
        term         = input_data.term
        today        = input_data.today
        principal    = input_data.principal
        commission   = input_data.commission

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = code,
                market  = market,
                tags    = tags,
                limit   = term,
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)

            invest_rule = None
            if rule_type == InvestRuleType.TURTLE:
                invest_rule = TurtleInvestRule(unit_number = unit, losscut_rate = losscut_rate)
            elif rule_type == InvestRuleType.RANDOM:
                tickers = [ticker for (ticker, sticks) in output.candlesticks.items()]
                invest_rule = RandomInvestRule(unit_number = unit, losscut_rate = losscut_rate, tickers = tickers)
            elif rule_type == InvestRuleType.RANDOM_LONG:
                tickers = [ticker for (ticker, sticks) in output.candlesticks.items()]
                invest_rule = RandomLongInvestRule(unit_number = unit, losscut_rate = losscut_rate, tickers = tickers)
            elif rule_type == InvestRuleType.RANDOM_TRAIL:
                tickers = [ticker for (ticker, sticks) in output.candlesticks.items()]
                invest_rule = RandomTrailLongInvestRule(unit_number = unit, losscut_rate = losscut_rate, tickers = tickers)
            elif rule_type == InvestRuleType.GOLDEN_TRAIL:
                invest_rule = GoldenTrailLongInvestRule(unit_number = unit, losscut_rate = losscut_rate)
            elif rule_type == InvestRuleType.SERIAL_STEPUP_TRAIL:
                invest_rule = SerialStepupTrailLongInvestRule(unit_number = unit, losscut_rate = losscut_rate)
            elif rule_type == InvestRuleType.TRIPLE_STEPUP_TRAIL:
                invest_rule = TripleStepupTrailLongInvestRule(unit_number = unit, losscut_rate = losscut_rate)
            elif rule_type == InvestRuleType.BUYHOLD:
                stick_numbers = {ticker: len(sticks) for (ticker, sticks) in output.candlesticks.items()}
                invest_rule = BuyholdInvestRule(unit_number = unit, losscut_rate = losscut_rate, stick_numbers = stick_numbers)
            else:
                # TODO
                pass

            simulator = InvestSimulator(
                    rule       = invest_rule,
                    sticks     = output.candlesticks,
                    cash       = principal,
                    commission = commission
                    )
            simulator.simulate()
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = SimulateTradeRuleOutput(
                report = simulator.report(sticks = {k: v[0] for (k,v) in output.candlesticks.items()})
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Predict setup signal.
    # ---------------------------------------------------------------------------------
    def predict_setup_signal(self, input_data: PredictSetupSignalInput) -> PredictSetupSignalOutput:
        rule_type    = input_data.rule_type
        code         = input_data.code
        market       = input_data.market
        tags         = input_data.tags
        today        = input_data.today

        invest_rule = None
        if rule_type == InvestRuleType.TURTLE:
            invest_rule = TurtleInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.RANDOM:
            invest_rule = RandomInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.RANDOM_LONG:
            invest_rule = RandomLongInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.RANDOM_TRAIL:
            invest_rule = RandomTrailLongInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.GOLDEN_TRAIL:
            invest_rule = GoldenTrailLongInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.SERIAL_STEPUP_TRAIL:
            invest_rule = SerialStepupTrailLongInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.TRIPLE_STEPUP_TRAIL:
            invest_rule = TripleStepupTrailLongInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'))
        elif rule_type == InvestRuleType.BUYHOLD:
            invest_rule = BuyholdInvestRule(unit_number = int(1), losscut_rate = Decimal('1.0'), stick_numbers = {})
        else:
            # TODO
            pass

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_range(ctx, stock_repository_inputdata.GetRangeInput(
                code    = code,
                market  = market,
                tags    = tags,
                limit   = invest_rule.required_number_of_histrical_data(),
                to_date = today
                ))

        result = list()
        try:
            output = self.transaction.do_in_tx(task)

            for (ticker, sticks) in output.candlesticks.items():
                if invest_rule.reaching_have_long(sticks = sticks, conditions = []):
                    result.append(sticks[0])

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = PredictSetupSignalOutput(
                candlesticks = result
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Delisting stock.
    # ---------------------------------------------------------------------------------
    def delisting_stock(self, input_data: DelistingStockInput) -> DelistingStockOutput:
        code         = input_data.code
        market       = input_data.market

        # Application Logic.
        def task(ctx: TxContext):
            sticks = self.stock_repository.get_ones_all(ctx, stock_repository_inputdata.GetOnesAllInput(
                code      = code,
                market    = market,
                from_date = None,
                to_date   = None,
                ))

            for stick in sticks.candlesticks:
                self.stock_repository.save_delisting(ctx, stock_repository_inputdata.SaveDelistingInput(delisting = stick))
  
            self.stock_repository.remove_ones_all(ctx, stock_repository_inputdata.RemoveOnesAllInput(code = code, market = market))
            return True

        result = list()
        try:
            _ = self.transaction.do_in_tx(task)

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = DelistingStockOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Listing stock.
    # ---------------------------------------------------------------------------------
    def listing_stock(self, input_data: ListingStockInput) -> ListingStockOutput:
        code   = input_data.code
        market = input_data.market

        # Application Logic.
        def task(ctx: TxContext):
            sticks = self.stock_repository.get_delistings_ones_all(ctx, stock_repository_inputdata.GetDelistingsOnesAllInput(
                code      = code,
                market    = market,
                from_date = None,
                to_date   = None,
                ))

            for stick in sticks.delistings:
                self.stock_repository.save(ctx, stock_repository_inputdata.SaveInput(candlestick = stick))
  
            self.stock_repository.remove_delistings_ones_all(ctx, stock_repository_inputdata.RemoveDelistingsOnesAllInput(code = code, market = market))
            return True

        result = list()
        try:
            _ = self.transaction.do_in_tx(task)

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = ListingStockOutput()

        return output_data

    # ---------------------------------------------------------------------------------
    # Get each first stick data order by date.
    # ---------------------------------------------------------------------------------
    def get_each_firststick(self, input_data: GetEachFirststickInput) -> GetEachFirststickOutput:
        order  = input_data.order
        limit  = input_data.limit
        offset = input_data.offset

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_all_term(ctx, stock_repository_inputdata.GetAllTermInput())

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            result = sorted(output.terms, key=lambda x: x.first_date, reverse=(order==RankingOrder.DESC))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetEachFirststickOutput(
                terms = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Get each last stick data order by date.
    # ---------------------------------------------------------------------------------
    def get_each_laststick(self, input_data: GetEachLaststickInput) -> GetEachLaststickOutput:
        order  = input_data.order
        limit  = input_data.limit
        offset = input_data.offset

        # Application Logic.
        def task(ctx: TxContext):
            return self.stock_repository.get_all_term(ctx, stock_repository_inputdata.GetAllTermInput())

        result = list()
        try:
            output = self.transaction.do_in_tx(task)
            result = sorted(output.terms, key=lambda x: x.last_date, reverse=(order==RankingOrder.DESC))

        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = GetEachLaststickOutput(
                terms = result[offset:offset+limit]
                )

        return output_data

    # ---------------------------------------------------------------------------------
    # Make cachetag from cache data.
    # ---------------------------------------------------------------------------------
    def make_cachetag(self, input_data: MakeCachetagInput) -> MakeCachetagOutput:
        cachetagname = 'cache'
        cachekey = input_data.cachekey
        limit    = input_data.limit

        cachedata = {}
        try:
            cachedata = self.cache_driver.get_dictionary(key = cachekey)
        except Exception as e:
            print(e)
            raise FatalAppException()

        stocks = list(map(lambda x: x['stock'], sorted([{'stock': Stock(code = key.split(':')[1], market = key.split(':')[0], tags = [cachetagname]), 'value': value} for (key, value) in cachedata.items()], key=lambda x: x['value'], reverse=True)[0:0+limit]))

        # Application Logic.
        def task(ctx: TxContext):
            self.stock_repository.remove_tag(ctx, stock_repository_inputdata.RemoveTagInput(tagname = cachetagname))
            for stock in stocks:
                self.stock_repository.save_tag(ctx, stock_repository_inputdata.SaveTagInput(stock = stock))

        try:
            self.transaction.do_in_tx(task)
        except Exception as e:
            print(e)
            raise FatalAppException()

        output_data = MakeCachetagOutput()

        return output_data
