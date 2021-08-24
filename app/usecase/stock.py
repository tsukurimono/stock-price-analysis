from abc import ABCMeta, abstractmethod

from app.usecase.inputdata.stock import *
from app.usecase.outputdata.stock import *

class StockUsecase(metaclass=ABCMeta):
    @abstractmethod
    def simulate_trade_rule(self, input_data: SimulateTradeRuleInput) -> SimulateTradeRuleOutput:
        raise NotImplementedError

    @abstractmethod
    def create_candlestick(self, input_data: CreateCandlestickInput) -> CreateCandlestickOutput:
        raise NotImplementedError

    @abstractmethod
    def create_tag(self, input_data: CreateTagInput) -> CreateTagOutput:
        raise NotImplementedError

    @abstractmethod
    def get_candlesticks(self, input_data: GetCandlesticksInput) -> GetCandlesticksOutput:
        raise NotImplementedError

    @abstractmethod
    def search_tickers(self, input_data: SearchTickersInput) -> SearchTickersOutput:
        raise NotImplementedError

    @abstractmethod
    def search_markets(self, input_data: SearchMarketsInput) -> SearchMarketsOutput:
        raise NotImplementedError

    @abstractmethod
    def search_tags(self, input_data: SearchTagsInput) -> SearchTagsOutput:
        raise NotImplementedError

    @abstractmethod
    def calcurate_sma(self, input_data: CalcurateSmaInput) -> CalcurateSmaOutput:
        raise NotImplementedError

    @abstractmethod
    def calcurate_wma(self, input_data: CalcurateWmaInput) -> CalcurateWmaOutput:
        raise NotImplementedError

    @abstractmethod
    def calcurate_ema(self, input_data: CalcurateEmaInput) -> CalcurateEmaOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ranking_price(self, input_data: GetRankingPriceInput) -> GetRankingPriceOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ranking_volume(self, input_data: GetRankingVolumeInput) -> GetRankingVolumeOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ranking_rs(self, input_data: GetRankingRsInput) -> GetRankingRsOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ranking_deviation(self, input_data: GetRankingDeviationInput) -> GetRankingDeviationOutput:
        raise NotImplementedError

    @abstractmethod
    def get_trend_price(self, input_data: GetTrendPriceInput) -> GetTrendPriceOutput:
        raise NotImplementedError

    @abstractmethod
    def get_trend_volume(self, input_data: GetTrendVolumeInput) -> GetTrendVolumeOutput:
        raise NotImplementedError

    @abstractmethod
    def get_trend_momentum(self, input_data: GetTrendMomentumInput) -> GetTrendMomentumOutput:
        raise NotImplementedError

    @abstractmethod
    def reflect_stocksplit(self, input_data: ReflectStocksplitInput) -> ReflectStocksplitOutput:
        raise NotImplementedError

    @abstractmethod
    def clear_cachedata(self, input_data: ClearCachedataInput) -> ClearCachedataOutput:
        raise NotImplementedError

    @abstractmethod
    def multiple_cachedata(self, input_data: MultipleCachedataInput) -> MultipleCachedataOutput:
        raise NotImplementedError

    @abstractmethod
    def get_cachedata(self, input_data: GetCachedataInput) -> GetCachedataOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ath(self, input_data: GetAthInput) -> GetAthOutput:
        raise NotImplementedError

    @abstractmethod
    def get_atl(self, input_data: GetAtlInput) -> GetAtlOutput:
        raise NotImplementedError

    @abstractmethod
    def get_average_atr(self, input_data: GetAverageAtrInput) -> GetAverageAtrOutput:
        raise NotImplementedError

    @abstractmethod
    def predict_setup_signal(self, input_data: PredictSetupSignalInput) -> PredictSetupSignalOutput:
        raise NotImplementedError

    @abstractmethod
    def delisting_stock(self, input_data: DelistingStockInput) -> DelistingStockOutput:
        raise NotImplementedError

    @abstractmethod
    def listing_stock(self, input_data: ListingStockInput) -> ListingStockOutput:
        raise NotImplementedError

    @abstractmethod
    def get_each_firststick(self, input_data: GetEachFirststickInput) -> GetEachFirststickOutput:
        raise NotImplementedError

    @abstractmethod
    def get_each_laststick(self, input_data: GetEachLaststickInput) -> GetEachLaststickOutput:
        raise NotImplementedError

    @abstractmethod
    def make_cachetag(self, input_data: MakeCachetagInput) -> MakeCachetagOutput:
        raise NotImplementedError
