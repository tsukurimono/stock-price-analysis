from abc import ABCMeta, abstractmethod
from typing import Dict

class CacheDriver(metaclass=ABCMeta):
    @abstractmethod
    def clear_dictionary(self, key:str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_dictionary(self, key:str, value:Dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_dictionary(self, key:str) -> Dict:
        raise NotImplementedError
