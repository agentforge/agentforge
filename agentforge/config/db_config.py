from typing import Optional
import os

class DbConfig():
    def __init__(self,
                 db_name: str,
                 host: Optional[str] = "localhost",
                 port: Optional[int] = 27017,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 auth_source: Optional[str] = "admin",
                 mongo_uri: Optional[str] = None,
                 ) -> None:
        self.db_name = db_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.mongo_uri = mongo_uri


    @staticmethod
    def from_env() -> 'DbConfig':
        return DbConfig(
            db_name=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 27017)),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            auth_source=os.getenv('DB_AUTH_SOURCE', 'admin'),
            mongo_uri=os.getenv('MONGODB_URI', None),
        )
