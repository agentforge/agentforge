import uuid, json
from datetime import datetime
from typing import Any, Dict, Optional, List, Callable
from agentforge.interfaces import interface_interactor
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from agentforge.ai.agents.context import Context
from collections import deque
from agentforge.utils import logger

# TODO: Move this to env
MAX_QUERY_RETRIES = 3

"""
### Basic Task Model
Allows us to return a Task model from this module
Task manages its own queries and attention
A task is something like -- help user plan their garden, help user plan their vacation, etc.
"""
class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="id")
    user_id: str
    session_id: str
    name: str
    stage: int = 0
    created_at: datetime
    updated_at: datetime
    active: bool
    actions: Optional[Dict[str, List[Any]]] = {'queue': deque([]),'complete': deque([]),'active': deque([]),'failed': deque([])}

    @classmethod
    def from_dict(cls, task_data: dict):
        t = cls(**task_data)
        t.actions = {'queue': deque(t['actions']['queue']),
                        'complete': deque(t['actions']['complete']),
                        'failed': deque(t['actions']['failed']),
                        'active': deque(t['actions']['active'])}
        return t

    def to_dict(self):
        task_model = Task(**self.__dict__)
        return task_model.dict(by_alias=True)

    def pretty_print(self):
        def datetime_serializer(o):
            if isinstance(o, datetime):
                return o.isoformat()
            raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

        task_dict = self.to_dict()
        pretty_string = json.dumps(task_dict, indent=4, default=datetime_serializer)
        print(pretty_string)

    # helpers for dict like access
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    """
    Input - context: Context object
    Output - None

    Runs the task routine specified by the task name
    """
    def run(self, context: Context) -> None:
        context.task_routines[self.name].run(context)

    def done(self) -> bool:
        return len(self.actions['queue']) == 0 and len(self.actions['active']) == 0 and len(self.actions['complete']) > 0
    
    """
    Creates new queries for the task using the planner
    """

    def peek(self) -> Optional[Dict]:
        return self.actions['queue'][0] if self.actions['queue'] else None

    def all(self) -> Optional[Dict]:
        return self.actions['queue'] if self.actions['queue'] else []

    def push(self, query: Dict=None):
        self.actions['queue'].append(query)

    # Update the first query in the queue, i.e. the head
    def update_query(self, **kwargs):
        if self.actions['queue']:
            self.actions['queue'][0].update(kwargs)

    # Pop the first query in the queue, i.e. the head
    def pop(self) -> Optional[Dict]:
        if self.actions['queue']:
            return self.actions['queue'].popleft()
        return None

    # Adds a query to the completed lists - this is a successful query
    def push_complete(self, query):
        self.actions['complete'].append(query)

    # Adds a query to the completed lists - for retrying
    def push_failed(self, query):
        if 'retries' in query and query['retries'] > MAX_QUERY_RETRIES:
            self.actions['failed'].append(query)
        elif 'retries' in query:
            query['retries'] = query['retries'] + 1
            self.actions['queue'].append(query)
        else:
            query['retries'] = 1
            self.actions['queue'].append(query)

    """
    Input - context: Context object
            llm: LLM object

    Output - str:  Adds a query to the active list from the queue by calling the LLM
    """
    def activate_query(self) -> str:
        return self.activate_n("query")

    def activate_plan(self) -> str:
        return self.activate_n("plan")

    def activate_n(self, metatype: str) -> str:
        if len(self.actions['active']) > 0:
            return self.actions['active'][0]
        query = None
        # Iterate through the queue
        for i, action in enumerate(self.actions['queue']):
            # Check if metatype exists and if it contains "query"
            if 'metatype' in action and action['metatype'] == metatype:
                query = self.actions['queue'][i]
                # Remove the item at index i
                self.actions['queue'] = deque(list(self.actions['queue'])[:i] + list(self.actions['queue'])[i+1:])
                break  # Exit loop once a query is found                
        if query is not None:
            self.actions['active'].append(query)
            return query
        else:
            return None  # Return None if no query is found

    def get_active_query(self) -> Optional[Dict]:
        self.get_active_n("query")

    def get_active_plan(self) -> Optional[Dict]:
        self.get_active_n("plan")

    # Only gets active query, will not activate a new one
    def get_active_n(self, metatype: str) -> Optional[Dict]:
        if len(self.actions['active']) == 0:
            return None
        query = None
        # Iterate through the queue
        for i, action in enumerate(self.actions['active']):
            # Check if metatype exists and if it contains "query"
            if 'metatype' in action and action['metatype'] == metatype:
                query = self.actions['active'][i]
                # Remove the item at index i
                self.actions['active'] = deque(list(self.actions['active'])[:i] + list(self.actions['active'])[i+1:])
                break  # Exit loop once a query is found                
        if query is not None:
            return query
        else:
            return None  # Return None if no query is found
        

"""
TaskManager class is responsible for managing tasks for the agent through the DB
Tasks are stored in the database and are associated with a user_id and session_id
Tasks also manage their attention and actions/queries/plans to the user.
"""
class TaskManager:
    def __init__(self) -> None:
        self.db = interface_interactor.get_interface("db")
        self.collection = 'tasks'

    """
        Inits a Task from a context, task id, and active state.
        Input - context: Context object
                name: str
                active: bool
    """
    def init_task(self, context: Context, name: str, active: bool = True) -> Task:
        user_id = context.get('input.user_id')
        session_id = context.get('input.model_id')

        creation_time = datetime.utcnow().isoformat()
        latest_update_time = creation_time
        id = str(uuid.uuid4())
        task_data = {
            'user_id': user_id,
            'session_id': session_id,
            'name': name,
            'created_at': creation_time,
            'updated_at': latest_update_time,
            'active': active
        }
        return Task.from_dict(task_data)

    """
    Input: user_id, session_id, name

    Output: Returns a list of Task objects to the user
    """
    def get_tasks(self, user_id: str, session_id: str, name: str) -> Optional[Any]:
        task_ctr = self.db.get_many(self.collection, {"user_id": user_id, "session_id": session_id, "name": name})
        return [Task.from_dict(t) for t in task_ctr]

    """
    Input: user_id, session_id, name

    Output: Returns a count of all tasks that match the input criteria
    """
    def count(self, user_id: str, session_id: str, name: str) -> Optional[Any]:
        return self.db.count(self.collection, {"user_id": user_id, "session_id": session_id, "name": name})

    def save(self, task: Task) -> None:
        if task:
            task.updated_at = datetime.utcnow().isoformat()
            print("task_] updaing task_:", task.id)
            self.db.set(self.collection, task.id, task.to_dict())
        else:
            raise ValueError(f"Attempted to save task with {task}")

    def delete_task(self, user_id: str, session_id: str, name: str) -> None:
        self.db.delete(self.collection, {"user_id": user_id, "session_id": session_id, "name": name})

    def active_task(self, user_id: str, session_id: str) -> bool:
        filter_criteria = {
            'user_id': user_id,
            'session_id': session_id,
            'active': True
        }
        active_tasks = self.db.get_many(self.collection, filter_criteria)
        for task in active_tasks:
            return Task.from_dict(task)
        return None
