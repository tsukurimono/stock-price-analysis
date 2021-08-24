from abc import ABCMeta, abstractmethod
from typing import Any,Tuple

class TxContext(metaclass=ABCMeta):
    @abstractmethod
    def get_tx(self) -> Any:
        raise NotImplementedError


class Transaction(metaclass=ABCMeta):

    @abstractmethod
    def do_in_tx(self, func: Any) -> Any:
        raise NotImplementedError
