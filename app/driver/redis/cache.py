from app.driver.cache import CacheDriver
import redis
from typing import Dict

class RedisCacheDriver(CacheDriver): 

    def __init__(self, server:str, port:str):
        self.conn = redis.StrictRedis(host=server, port=port, db=0, decode_responses=True)

    # ---------------------------------------------------------------------------------
    # Save dictionary.
    # ---------------------------------------------------------------------------------
    def save_dictionary(self, key:str, value:Dict) -> bool:
        self.conn.hmset(key, value)

    # ---------------------------------------------------------------------------------
    # Get dictionary.
    # ---------------------------------------------------------------------------------
    def get_dictionary(self, key:str) -> Dict:
        return self.conn.hgetall(key)

    # ---------------------------------------------------------------------------------
    # Clear dictionary.
    # ---------------------------------------------------------------------------------
    def clear_dictionary(self, key:str) -> bool:
        self.conn.delete(key)

