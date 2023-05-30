from typing import Any, Optional, Protocol, Dict
from pymongo import MongoClient, errors
from pymongo.cursor import Cursor

from agentforge.config import DbConfig
import logging
from agentforge.adapters import DB

class MongoDBKVStore(DB):
    def __init__(self, config: DbConfig) -> None:
        self.connection(config)

    def _check_connection(self):
        if not self.client or self.db is None:
            raise ConnectionError("No active connection available.")

    def connection(self, config: DbConfig) -> None:
        try:
            self.client = MongoClient(f"mongodb://{config.username}:{config.password}@{config.host}:{config.port}")
            self.db = self.client[config.db_name]
            logging.info('Connection established.')
        except errors.ConnectionFailure as e:
            logging.error(f'Connection failed: {str(e)}')
            raise

    # Explicitly create document with key
    def create(self, collection:str, key: str, data: Dict[str, Any]) -> None:
        self._check_connection()
        collection = self.db[collection]
        try:
            if collection.find_one({"_id": key}):
                logging.error(f'Create operation failed for key {key}: record already exists.')
                raise ValueError(f'A record with key {key} already exists.')
            data["_id"] = key  # add the key to the data dict
            collection.insert_one(data)
            logging.info(f'Successfully created record with key {key}.')
        except Exception as e:
            logging.error(f'Create operation failed for key {key}: {str(e)}')
            raise

    def get(self, collection:str, key: str) -> Optional[Dict[str, Any]]:
        self._check_connection()
        collection = self.db[collection]
        try:
            result = collection.find_one({"_id": key})
            if result:
                del result["_id"]  # remove the _id field from the result
            return result
        except Exception as e:
            logging.error(f'Get operation failed for key {key}: {str(e)}')
            raise

    # Create or update document
    def set(self, collection:str, key: str, data: Dict[str, Any]) -> None:
        self._check_connection()
        collection = self.db[collection]
        try:
            data["_id"] = key  # add the key to the data dict
            collection.update_one({"_id": key}, {"$set": data}, upsert=True)
            logging.info(f'Successfully set value for key {key}.')
        except Exception as e:
            logging.error(f'Set operation failed for keyChange the following  {key}: {str(e)}')
            raise

    def delete(self, collection:str, key: str) -> None:
        self._check_connection()
        collection = self.db[collection]
        try:
            collection.delete_one({"_id": key})
            logging.info(f'Successfully deleted value for key {key}.')
        except Exception as e:
            logging.error(f'Delete operation failed for key {key}: {str(e)}')
            raise

    def get_many(self, collection:str, filter: Dict[str, Any]) -> Cursor:
        self._check_connection()
        collection = self.db[collection]
        try:
            result = collection.find(filter)
            return result
        except Exception as e:
            logging.error(f'Get operation failed for filter {filter}: {str(e)}')
            raise
