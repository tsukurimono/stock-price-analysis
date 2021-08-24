from abc import ABCMeta, abstractmethod

class StockController:
    @abstractmethod
    def simulate_trade_rule(self):
        raise NotImplementedError

    @abstractmethod
    def load_candlesticks(self):
        raise NotImplementedError

    @abstractmethod
    def load_tags(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_prices(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_volumes(self):
        raise NotImplementedError

    @abstractmethod
    def search_tickersymbols(self):
        raise NotImplementedError

    @abstractmethod
    def search_marketsymbols(self):
        raise NotImplementedError

    @abstractmethod
    def search_tags(self):
        raise NotImplementedError

    @abstractmethod
    def clear_cachedata(self):
        raise NotImplementedError

    @abstractmethod
    def multiple_cachedata(self):
        raise NotImplementedError

    @abstractmethod
    def show_cachedata(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_price_smas(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_volume_smas(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_price_wmas(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_volume_wmas(self):
        raise NotImplementedError


    @abstractmethod
    def get_stock_price_emas(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_volume_emas(self):
        raise NotImplementedError

    @abstractmethod
    def ranking_price(self):
        raise NotImplementedError

    @abstractmethod
    def ranking_volume(self):
        raise NotImplementedError

    @abstractmethod
    def ranking_relative_strength(self):
        raise NotImplementedError

    @abstractmethod
    def ranking_deviation(self):
        raise NotImplementedError

    @abstractmethod
    def trend_price(self):
        raise NotImplementedError

    @abstractmethod
    def trend_volume(self):
        raise NotImplementedError

    @abstractmethod
    def trend_momentum(self):
        raise NotImplementedError

    @abstractmethod
    def reflect_stocksplit(self):
        raise NotImplementedError

    @abstractmethod
    def get_ath(self):
        raise NotImplementedError

    @abstractmethod
    def get_atl(self):
        raise NotImplementedError

    @abstractmethod
    def get_average_atr(self):
        raise NotImplementedError

    @abstractmethod
    def predict_setupsignal(self):
        raise NotImplementedError

    @abstractmethod
    def delistings_sticks(self):
        raise NotImplementedError

    @abstractmethod
    def listings_sticks(self):
        raise NotImplementedError

    @abstractmethod
    def stock_firstdate(self):
        raise NotImplementedError

    @abstractmethod
    def stock_lastdate(self):
        raise NotImplementedError

    @abstractmethod
    def make_cachetag(self):
        raise NotImplementedError
