from typing import Any, Optional, Protocol, Dict, List
from pymongo import MongoClient, errors
from pymongo.cursor import Cursor
from urllib.parse import quote_plus
import uuid
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from agentforge.config import DbConfig
import logging
from agentforge.adapters import DB
from agentforge.utils import logger
class MongoDBKVStore(DB):
    def __init__(self, config: DbConfig) -> None:
        self.connection(config)
        self.id = "id"

    def _check_connection(self):
        if not self.client or self.db is None:
            raise ConnectionError("No active connection available.")

    def connection(self, config: DbConfig) -> None:
        try:
            if config.mongo_uri is not None:
                self.client = MongoClient(f"{config.mongo_uri}")
            else:
                username = quote_plus(config.username)
                password = quote_plus(config.password)
                host = config.host
                port = config.port
                self.client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}")
            self.db = self.client[config.db_name]
            logging.info('Connection established.')
        except errors.ConnectionFailure as e:
            logging.error(f'Connection failed: {str(e)}')
            raise

    def batch_upload(self, collection: str, documents: List[Dict[str, Any]]) -> None:
        # Perform batch upload of documents to the specified collection
        if not documents:
            return  # Exit if there are no documents to upload

        operations = []
        for doc in documents:
            # Use the _id field for upsert operations
            operation = UpdateOne({'_id': doc['uuid']}, {'$set': doc}, upsert=True)
            operations.append(operation)

        try:
            collection_ref = self.db[collection]
            result = collection_ref.bulk_write(operations)
            return True
            # print(f"Batch upload complete: {result.bulk_api_result}")
        except BulkWriteError as e:
            logger.info(f"Error during batch upload: {e.details}")
            return False
            # Handle specific errors or perform additional error logging here

    # Explicitly create document with key
    def create(self, collection:str, key: str ="", data: Dict[str, Any] = {}) -> Dict[str, Any]:
        self._check_connection()
        collection = self.db[collection]
        try:
            if key == "":
                 key = str(uuid.uuid4())
            if collection.find_one({"id": key}):
                logging.error(f'Create operation failed for key {key}: record already exists.')
                raise ValueError(f'A record with key {key} already exists.')
            data["id"] = key  # add the key to the data dict
            collection.insert_one(data)
            logging.info(f'Successfully created record with key {key}.')
            return data
        except Exception as e:
            logging.error(f'Create operation failed for key {key}: {str(e)}')
            raise

    def get(self, collection:str, key: str) -> Optional[Dict[str, Any]]:
        self._check_connection()
        collection = self.db[collection]
        try:
            result = collection.find_one({"id": key})
            if result:
                del result["id"]  # remove the _id field from the result
            return result
        except Exception as e:
            logging.error(f'Get operation failed for key {key}: {str(e)}')
            raise

    # Create or update document
    def set(self, collection:str, key: str, data: Dict[str, Any]) -> None:
        self._check_connection()
        collection = self.db[collection]
        try:
            data["id"] = key  # add the key to the data dict
            ret = collection.update_one({"id": key}, {"$set": data}, upsert=True)
            # logging.info(f'Successfully set value for key {key}.')
        except Exception as e:
            logging.error(f'Set operation failed for keyChange the following  {key}: {str(e)}')
            raise
        return ret

    def copy(self, src_collection: str, dest_collection: str, key: str, new_key: Optional[str] = None) -> None:
        self._check_connection()
        src_collection = self.db[src_collection]
        dest_collection = self.db[dest_collection]
        
        try:
            document = src_collection.find_one({"id": key})
            if document is not None:
                if new_key is None:
                    new_key = str(uuid.uuid4())
                    
                document["id"] = new_key
                dest_collection.update_one({"id": new_key}, {"$set": document}, upsert=True)
                
                logging.info(f'Successfully copied document for key {key}. New key: {new_key}')
                return True
            else:
                logging.warning(f'No document found for key {key}. Nothing to copy.')
        except Exception as e:
            logging.error(f'Copy operation failed for key {key}: {str(e)}')
            return False


    def delete(self, collection:str, key: str) -> None:
        self._check_connection()
        collection = self.db[collection]
        try:
            collection.delete_one(key)
            logging.info(f'Successfully deleted value for key {key}.')
        except Exception as e:
            logging.error(f'Delete operation failed for key {key}: {str(e)}')
            raise


    def count(self, collection:str, filter: Dict[str, Any]) -> Cursor:
        self._check_connection()
        collection = self.db[collection]
        try:
            result = collection.count_documents(filter)
            return result
        except Exception as e:
            logging.error(f'Get operation failed for filter {filter}: {str(e)}')
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

    def aggregate(self, collection: str, pipeline: List[Dict[str, Any]]) -> Optional[Any]:
        col = self.db[collection]
        return list(col.aggregate(pipeline))
