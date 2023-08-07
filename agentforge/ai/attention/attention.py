from datetime import datetime, timedelta
from typing import List
from functools import wraps
from agentforge.interfaces import interface_interactor
''
def check_ttl(func):
    @wraps(func)
    def wrapper(self, key, *args, **kwargs):
        # Fetching the attention document
        attention_doc = self.db.get("attention", key)
        if attention_doc:
            # Checking the TTL
            timestamp = datetime.fromisoformat(attention_doc["timestamp"])
            if datetime.utcnow() - timestamp > timedelta(days=self.ATTENTION_TTL_DAYS):
                # Deleting expired attention document
                self.db.delete("attention", key)
                return None
            return func(self, attention_doc, key, *args, **kwargs)
        return None
    return wrapper


class Attention:
    def __init__(self):
        self.db = interface_interactor.get_interface("db")

    ### When you need to acquire some information, let's apply some attention to the situation
    ### so we can remember what we have learned and what we still need to learn
    def create_attention(self, task, queries: List[str], key: str) -> None:
        # Creating an attention document with queries and timestamp
        if queries is not None and len(queries) > 0:
            attention_doc = {
                "task": task,
                "queries": queries,
                "satisfied": [False] * len(queries),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.db.create("attention", key, attention_doc)
        else:
            raise ValueError(f"Attempted to create attention with queries {queries}")

    @check_ttl
    def satisfy_attention(self, attention_doc, key: str, query: str, results: List[str]) -> None:
        # Fetching the attention document
        attention_doc = self.db.get("attention", key)
        # Marking the query as satisfied
        for idx, q in enumerate(attention_doc["queries"]):
            if q["query"] == query["query"]:
                print("That's satisfaction baby")
                attention_doc["satisfied"][idx] = True
                attention_doc["queries"][idx]["results"] = results
                break
        # Updating the attention document
        self.db.set("attention", key, attention_doc)

    @check_ttl
    def attention_satisfied(self, attention_doc, key: str) -> bool:
        # Checking if all queries are satisfied
        return all(attention_doc["satisfied"])

    @check_ttl  
    def get_attention(self, attention_doc, key: str) -> bool:
        # Fetching the attention document
        return attention_doc

    @check_ttl
    def attention_exists(self, _, key: str) -> bool:
        # Fetching the attention document
        return True