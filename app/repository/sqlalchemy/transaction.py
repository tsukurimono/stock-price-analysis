from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from app.repository.transaction import TxContext, Transaction
from typing import Any

class SqlclchemyTxContext(TxContext):
    tx: Any

    def __init__(self, tx: Any):
        self.tx = tx

    def get_tx(self) -> Any:
        return self.tx
    

class SqlalchemyTransaction(Transaction):
    target_url: str
    pool_recycle: int
    sql_engine: Engine
    sql_sessions: Session

    def __init__(self, target_url:str, pool_recycle:int):
        self.target_url = target_url
        self.pool_recycle = pool_recycle
        self.sql_engine = create_engine(self.target_url, pool_recycle=self.pool_recycle)
        self.sql_sessions = sessionmaker(bind=self.sql_engine, expire_on_commit=False)

    def do_in_tx(self, func: Any) -> Any:
        ctx = SqlclchemyTxContext(tx = self.sql_sessions())

        try:
            result = func(ctx)
            ctx.get_tx().commit()
        except Exception as e:
            print(e)
            ctx.get_tx().rollback()
            raise
        finally:
            ctx.get_tx().close()

        return result
