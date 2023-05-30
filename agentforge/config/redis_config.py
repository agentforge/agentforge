from typing import Optional
import os

class RedisConfig():
    def __init__(self,
                 host: Optional[str] = "localhost",
                 port: Optional[int] = 6379,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 db: Optional[int] = 0
                 ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db

    @staticmethod
    def from_env() -> 'RedisConfig':
        return RedisConfig(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            username=os.getenv('REDIS_USER'),
            password=os.getenv('REDIS_PASS'),
            db=int(os.getenv('REDIS_DB', 0)),
        )
