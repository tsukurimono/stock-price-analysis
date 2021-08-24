from __future__ import annotations
from abc import ABCMeta, abstractmethod

from app.repository.stock import StockRepository
from app.repository.transaction import Transaction

from app.driver.cache import CacheDriver

from app.usecase.stock import StockUsecase

from app.controller.stock import StockController

class DIContainer(metaclass=ABCMeta):
    @abstractmethod
    def inject_stock_repository(self) -> StockRepository:
        raise NotImplementedError

    @abstractmethod
    def inject_transaction(self) -> Transaction:
        raise NotImplementedError

    @abstractmethod
    def inject_stock_usecase(self) -> StockUsecase:
        raise NotImplementedError

    @abstractmethod
    def inject_stock_controller(self) -> StockController:
        raise NotImplementedError

    @abstractmethod
    def inject_cache_driver(self) -> CacheDriver:
        raise NotImplementedError
