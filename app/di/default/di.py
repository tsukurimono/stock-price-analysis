from __future__                            import annotations

from configparser                          import ConfigParser
from os                                    import path, getenv

from app.di.di                             import DIContainer

from app.repository.stock                  import StockRepository
from app.repository.transaction            import Transaction

from app.repository.sqlalchemy.transaction import SqlalchemyTransaction
from app.repository.sqlalchemy.stock       import SqlalchemyStockRepository

from app.usecase.stock                     import StockUsecase
from app.usecase.default.stock             import DefaultStockInteractor

from app.controller.stock                  import StockController
from app.controller.cli.stock              import CliStockController

from app.driver.cache                      import CacheDriver
from app.driver.redis.cache                import RedisCacheDriver

class DefaultDIContainer(DIContainer):
    config:             ConfigParser
    stock_repository:   StockRepository
    stock_usecase:      StockUsecase
    transaction:        Transaction
    stock_controller:   StockController
    cache_driver:       CacheDriver

    def __init__(self):
        self.stock_usecase      = None
        self.stock_repository   = None
        self.transaction        = None
        self.stock_controller   = None
        self.cache_driver       = None

        self.config = ConfigParser()
        self.config.read(path.dirname(__file__)+'/config.ini', encoding='utf-8')

    def inject_stock_repository(self) -> StockRepository:
        if self.stock_repository == None:
            self.stock_repository = SqlalchemyStockRepository()
        return self.stock_repository

    def inject_transaction(self) -> Transaction:
        if self.transaction == None:
            self.transaction = SqlalchemyTransaction(
                    target_url   = getenv('TransactionTargetUrl',       self.config['Transaction']['target_url']),
                    pool_recycle = int(getenv('TransactionPoolRecycle', self.config['Transaction']['pool_recycle']))
                    ) 
        return self.transaction

    def inject_stock_usecase(self) -> StockUsecase:
        if self.stock_usecase == None:
            self.stock_usecase = DefaultStockInteractor(
                    stock_repository = self.inject_stock_repository(),
                    transaction      = self.inject_transaction(),
                    cache_driver     = self.inject_cache_driver()
                    )
        return self.stock_usecase

    def inject_stock_controller(self) -> StockController:
        if self.stock_controller == None:
            self.stock_controller = CliStockController(
                    stock_usecase = self.inject_stock_usecase()
                    )
        return self.stock_controller

    def inject_cache_driver(self) -> CacheDriver:
        if self.cache_driver == None:
            self.cache_driver = RedisCacheDriver(
                    server = getenv('CacheDriverServer', self.config['CacheDriver']['server']),
                    port   = getenv('CacheDriverPort', self.config['CacheDriver']['port'])
                    )
        return self.cache_driver
