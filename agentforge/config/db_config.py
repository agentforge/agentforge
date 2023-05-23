from typing import Optional
from dotenv import load_dotenv
import os

class DbConfig():
    def __init__(self,
                 db_name: str,
                 host: Optional[str] = "localhost",
                 port: Optional[int] = 27017,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 auth_source: Optional[str] = "admin",
                 ) -> None:
        self.db_name = db_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source


    @staticmethod
    def from_env() -> 'DbConfig':
        load_dotenv()
        return DbConfig(
            db_name=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 27017)),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            auth_source=os.getenv('DB_AUTH_SOURCE', 'admin'),
        )
