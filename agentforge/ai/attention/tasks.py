import uuid, json
from datetime import datetime
from typing import Any, Dict, Optional, List
from agentforge.interfaces import interface_interactor
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from pydantic import BaseModel, Field
from datetime import datetime
from agentforge.ai.agents.context import Context
from collections import deque

"""
### Basic Task Model
Allows us to return a Task model from this module
Task manages its own queries and attention
"""
class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    session_id: str
    name: str
    stage: int = 0
    created_at: datetime
    updated_at: datetime
    active: bool
    queries: Optional[Dict[str, List[Any]]] = {'queue': deque([]),'complete': deque([]),'active': deque([]),'failed': deque([])}

    @classmethod
    def from_dict(cls, task_data: dict):
        t = cls(**task_data)
        t.queries = {'queue': deque(t['queries']['queue']),
                        'complete': deque(t['queries']['complete']),
                        'failed': deque(t['queries']['failed']),
                        'active': deque(t['queries']['active'])}
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
        return len(self.queries['queue']) == 0 and len(self.queries['active']) == 0 and len(self.queries['complete']) > 0
    
    """
    Creates new queries for the task using the planner
    """

    def peek(self) -> Optional[Dict]:
        return self.queries['queue'][0] if self.queries['queue'] else None

    def all(self) -> Optional[Dict]:
        return self.queries['queue'] if self.queries['queue'] else []

    def push(self, query: Dict=None):
        self.queries['queue'].append(query)

    # Update the first query in the queue, i.e. the head
    def update_query(self, **kwargs):
        if self.queries['queue']:
            self.queries['queue'][0].update(kwargs)

    # Pop the first query in the queue, i.e. the head
    def pop(self) -> Optional[Dict]:
        if self.queries['queue']:
            return self.queries['queue'].popleft()
        return None

    # Adds a query to the completed lists - this is a successful query
    def push_complete(self, query):
        self.queries['complete'].append(query)

    # Adds a query to the completed lists - for retrying
    def push_failed(self, query):
        self.queries['failed'].append(query)

    """
    Input - context: Context object
            llm: LLM object

    Output - str:  Adds a query to the active list from the queue by calling the LLM
    """
    def activate(self, context, llm) -> str:
        if len(self.queries['active']) > 0:
            return self.queries['active'][0]['text']
        query = self.queries['queue'].popleft()

        # # We need to create a query via the LLM using the context and query
        input = context.get_model_input()
        # prompt = context.prompts[f"{query['type']}.query.prompt"]
        # data = {
        #     "goal": query['goal'],
        #     "type": query['type'],
        #     "detail": query['object'].replace("?",""),
        #     "action": query['goal'],
        # }
        # print(query)
        # print(input)
        # query = {}
        input['prompt'] = query['text']
        # input['prompt'] = context.process_prompt(prompt, data)
        query['text'] = llm.call(input)["choices"][0]["text"]
        print(query['text'])
        # We've got our query now activate it
        self.queries['active'].append(query)
        return query['text']

    # Only gets active query, will not activate a new one
    def get_active_query(self) -> Optional[Dict]:
        print(self.queries) 
        if len(self.queries['active']) == 0:
            return None
        return self.queries['active'].popleft()

"""
TaskManager class is responsible for managing tasks for the agent through the DB
Tasks are stored in the database and are associated with a user_id and session_id
Tasks also manage their attention and queries to the user.
"""
class TaskManager:
    def __init__(self) -> None:
        self.db = interface_interactor.get_interface("db")
        self.collection = 'tasks'

    """
    Input: user_id, session_id, name
    Output: Task object
    """
    def add_task(self, user_id: str, session_id: str, name: str, active: bool = True) -> Optional[Any]:
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
        return Task.from_dict(self.db.create(self.collection, id, task_data))

    """
    Input: user_id, session_id, name

    Output: Returns a list of Task objects to the user
    """
    def get_tasks(self, user_id: str, session_id: str, name: str) -> Optional[Any]:
        task_ctr = self.db.get_many(self.collection, {"user_id": user_id, "session_id": session_id, "name": name})
        return [Task(t) for t in task_ctr]

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
