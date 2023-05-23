from typing import Any, Optional, Protocol
from pymongo import MongoClient, errors

from agentforge.config import DbConfig
import logging
from agentforge.adapters import AbstractKVStore
class MongoDBKVStore(AbstractKVStore):
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def _check_connection(self):
        if not self.client or not self.db or not self.collection:
            raise ConnectionError("No active connection available.")

    def connection(self, config: DbConfig) -> None:
        try:
            self.client = MongoClient(config.host, config.port)
            self.db = self.client[config.db_name]
            self.collection = self.db[config.collection_name]
            logging.info('Connection established.')
        except errors.ConnectionFailure as e:
            logging.error(f'Connection failed: {str(e)}')
            raise

    def get(self, key: str) -> Optional[Any]:
        self._check_connection()
        try:
            result = self.collection.find_one({"_id": key})
            return result['value'] if result else None
        except Exception as e:
            logging.error(f'Get operation failed for key {key}: {str(e)}')
            raise

    def set(self, key: str, value: Any) -> None:
        self._check_connection()
        try:
            self.collection.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
            logging.info(f'Successfully set value for key {key}.')
        except Exception as e:
            logging.error(f'Set operation failed for key {key}: {str(e)}')
            raise

    def delete(self, key: str) -> None:
        self._check_connection()
        try:
            self.collection.delete_one({"_id": key})
            logging.info(f'Successfully deleted value for key {key}.')
        except Exception as e:
            logging.error(f'Delete operation failed for key {key}: {str(e)}')
            raise