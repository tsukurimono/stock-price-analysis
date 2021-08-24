from abc import ABCMeta, abstractmethod

from app.repository.transaction      import TxContext
from app.repository.inputdata.stock  import *
from app.repository.outputdata.stock import *

class StockRepository(metaclass=ABCMeta):
    @abstractmethod
    def find(self, ctx: TxContext, input_data:FindInput) -> FindOutput:
        raise NotImplementedError

    @abstractmethod
    def find_tag(self, ctx: TxContext, input_data:FindTagInput) -> FindTagOutput:
        raise NotImplementedError

    @abstractmethod
    def save(self, ctx: TxContext, input_data:SaveInput) -> SaveOutput:
        raise NotImplementedError

    @abstractmethod
    def save_tag(self, ctx: TxContext, input_data:SaveTagInput) -> SaveTagOutput:
        raise NotImplementedError

    @abstractmethod
    def remove_ones_all(self, ctx: TxContext, input_data:RemoveOnesAllInput) -> RemoveOnesAllOutput:
        raise NotImplementedError

    @abstractmethod
    def get(self, ctx: TxContext, input_data:GetInput) -> GetOutput:
        raise NotImplementedError

    @abstractmethod
    def get_ones_all(self, ctx: TxContext, input_data:GetOnesAllInput) -> GetOnesAllOutput:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, ctx: TxContext, input_data:GetAllInput) -> GetAllOutput:
        raise NotImplementedError

    @abstractmethod
    def get_each(self, ctx: TxContext, input_data:GetEachInput) -> GetEachOutput:
        raise NotImplementedError

    @abstractmethod
    def get_range(self, ctx: TxContext, input_data:GetRangeInput) -> GetRangeOutput:
        raise NotImplementedError

    @abstractmethod
    def search_tickers(self, ctx: TxContext, input_data:SearchTickersInput) -> SearchTickersOutput:
        raise NotImplementedError

    @abstractmethod
    def get_tickers(self, ctx: TxContext, input_data:GetTickersInput) -> GetTickersOutput:
        raise NotImplementedError

    @abstractmethod
    def search_markets(self, ctx: TxContext, input_data:SearchMarketsInput) -> SearchMarketsOutput:
        raise NotImplementedError

    @abstractmethod
    def search_tags(self, ctx: TxContext, input_data:SearchTagsInput) -> SearchTagsOutput:
        raise NotImplementedError

    @abstractmethod
    def get_stockdatainfo(self, ctx: TxContext, input_data:GetStockdatainfoInput) -> GetStockdatainfoOutput:
        raise NotImplementedError

    @abstractmethod
    def save_delisting(self, ctx: TxContext, input_data:SaveDelistingInput) -> SaveDelistingOutput:
        raise NotImplementedError

    @abstractmethod
    def find_delisting(self, ctx: TxContext, input_data:FindDelistingInput) -> FindDelistingOutput:
        raise NotImplementedError

    @abstractmethod
    def get_delistings_ones_all(self, ctx: TxContext, input_data:GetDelistingsOnesAllInput) -> GetDelistingsOnesAllOutput:
        raise NotImplementedError

    @abstractmethod
    def remove_delistings_ones_all(self, ctx: TxContext, input_data:RemoveDelistingsOnesAllInput) -> RemoveDelistingsOnesAllOutput:
        raise NotImplementedError

    @abstractmethod
    def get_all_term(self, ctx: TxContext, input_data:GetAllTermInput) -> GetAllTermOutput:
        raise NotImplementedError

    @abstractmethod
    def remove_tag(self, ctx: TxContext, input_data:RemoveTagInput) -> RemoveTagOutput:
        raise NotImplementedError
