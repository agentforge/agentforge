import json
import logging
from typing import Any, List, Optional
from agentforge.interfaces import interface_interactor

import logging
from typing import Optional, Dict
from agentforge.interfaces import interface_interactor

class QueryEngine:
    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id
        self.db = interface_interactor.get_interface("db")

    def create_queries(self, queries: List[Dict]):
        key = f"{self.user_id}-{self.session_id}"
        # Check if the document already exists
        existing_doc = self.db.get("queries", key)
        if existing_doc:
            raise ValueError(f"A document with key {key} already exists")
        else:
            # Create a new document with user_id and session_id at the root level
            queue_obj = {'user_id': self.user_id, 'session_id': self.session_id, 'queue': queries}
            self.db.create("queries", key, queue_obj)

    def get_query(self) -> Optional[Dict]:
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        return queue_obj['queue'][0] if queue_obj and 'queue' in queue_obj and queue_obj['queue'] else None

    def get_queries(self) -> Optional[Dict]:
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        return queue_obj['queue'] if queue_obj and 'queue' in queue_obj else []

    def get_sent_queries(self) -> Optional[List[Dict]]:
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        return [query for query in queue_obj['queue'] if 'sent' in query and query['sent']] if queue_obj and 'queue' in queue_obj else []

    def push_query(self, **kwargs):
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key) or {'user_id': self.user_id, 'session_id': self.session_id, 'queue': []}
        # Push the new query to the queue without user_id and session_id
        queue_obj['queue'].append(kwargs)
        self.db.set("queries", key, queue_obj)

    def update_query(self, **kwargs):
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
            queue_obj['queue'][0].update(kwargs)
            self.db.set("queries", key, queue_obj)

    def pop_query(self) -> Optional[Dict]:
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
            query = queue_obj['queue'].pop(0)
            self.db.set("queries", key, queue_obj)
            return query
        return None
    
    def parse_response(self, response_text):
        key = f"{self.user_id}-{self.session_id}"
        queue_obj = self.db.get("queries", key)
        if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
            queue_obj['queue'][0]['response'] = response_text
            self.db.set("queries", key, queue_obj)

# Example Usage

# # Assume DB has been properly configured and connected.
# qe = QueryEngine()
# user_id = "user1"
# session_id = "session1"

# # Add a query
# qe.push_query(user_id, session_id, question="What's your name?")

# # Get the top query without removing it
# top_query = qe.get_query(user_id, session_id)
# print(f"Top Query: {top_query}")

# # Parse a response for the top query
# qe.parse_response(user_id, session_id, "My name is ChatGPT.")

# # Pop the top query
# popped_query = qe.pop_query(user_id, session_id)
# print(f"Popped Query: {popped_query}")

