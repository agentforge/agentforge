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

    def get_query(self, **kwargs) -> Optional[Dict]:
        try:
            # Get the queue object from the database
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}")

            # If queue_obj exists and is not empty, return the first query
            if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
                return queue_obj['queue'][0]
            else:
                return None
        except Exception as e:
            logging.error(f"Error fetching query: {e}")
            return None

    def get_queries(self, **kwargs) -> Optional[Dict]:
        try:
            # Get the queue object from the database
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}")

            # If queue_obj exists and is not empty, return the first query
            if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
                return queue_obj['queue']
            else:
                return []
        except Exception as e:
            logging.error(f"Error fetching query: {e}")
            return []
    
    def update_query(self, **kwargs):
        try:
            # Get the existing queue object
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}")

            # If queue_obj exists and is not empty, update the top-most query
            if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
                # Update the top-most query with kwargs
                queue_obj['queue'][0].update(kwargs)

                # Save the updated queue object back to the database
                self.db.set("queries", f"{self.user_id}-{self.session_id}", queue_obj)
            else:
                logging.error(f"No query to update for user_id {self.user_id} and session_id {self.session_id}")
        except Exception as e:
            logging.error(f"Error updating query: {e}")


    def push_query(self, **kwargs):
        try:
            # Get the existing queue object or create a new one if it doesn't exist
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}") or {'queue': []}

            # Push the new query to the queue
            queue_obj['queue'].append({"user_id": self.user_id, "session_id": self.session_id, **kwargs})

            # Save the updated queue object back to the database
            self.db.set("queries", f"{self.user_id}-{self.session_id}", queue_obj)
        except Exception as e:
            logging.error(f"Error saving query: {e}")

    def pop_query(self) -> Optional[Dict]:
        try:
            # Get the queue object from the database
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}")

            # If queue_obj exists and is not empty, pop the first query
            if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
                query = queue_obj['queue'].pop(0)

                # Save the updated queue object back to the database
                self.db.set("queries", f"{self.user_id}-{self.session_id}", queue_obj)

                return query
            else:
                return None
        except Exception as e:
            logging.error(f"Error popping query: {e}")
            return None

    def parse_response(self, response_text):
        try:
            # Get the queue object from the database
            queue_obj = self.db.get("queries", f"{self.user_id}-{self.session_id}")

            # If queue_obj exists and is not empty, update the first query
            if queue_obj and 'queue' in queue_obj and queue_obj['queue']:
                queue_obj['queue'][0]['response'] = response_text

                # Save the updated queue object back to the database
                self.db.set("queries", f"{self.user_id}-{self.session_id}", queue_obj)
        except Exception as e:
            logging.error(f"Error parsing response: {e}")

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

