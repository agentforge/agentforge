import json, uuid, os
from typing import Dict, Any
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser
from agentforge.utils import AbortController, logger
from bson.objectid import ObjectId
from copy import deepcopy
from jinja2 import Template
from datetime import datetime
import threading
from datetime import datetime

"""
    Context Class - Shared State for Agent Subroutines

    The context class is a shared state for agent subroutines.
    It is a dictionary-like object that allows us to store and
    retrieve values using dot notation. It also provides helper
    functions to format prompts and get model input and abort.

    Input:
        init: Dict - Initial values to set in the context
"""
class Context:
    def __init__(self, init: Dict = {}) -> None:
        self.db = interface_interactor.get_interface("db")
        self.parser = Parser()
        self.task_routines = {}
        self.context_data = {}
        self.prompts = self.read_prompts()
        self.abort_controller = AbortController()
        self._id = uuid.uuid4()
        self.created_dt = datetime.utcnow()
        self.lock = threading.Lock()  # Add a threading lock
        for k,v in init.items():
            self.set(k, v)

    def update(self, new_data: Dict) -> None:
        with self.lock:  # Acquire lock before updating
            self.context_data.update(new_data)

    def save(self):
        collection = "context"
        ctx = deepcopy(self.context_data)
        if "task" in ctx:
            del ctx["task"]
        # Prepare the data to be inserted; only serialize what's necessary
        data = {
            "context_data": ctx,
            "prompts": self.prompts,
            "created_dt": self.created_dt,
        }

        # Insert to the DB
        self.db.create(collection, str(self._id), data)

    def load(self, context_id: str):
        collection = "context"
        
        # Retrieve data from DB
        stored_data = self.db.get(collection, context_id)
        
        if stored_data is not None:
            # Update the object with the loaded data
            self.__dict__.update(stored_data)
            
            # Initialize parser and abort_controller since they were skipped during serialization
            self.parser = Parser()
            self.abort_controller = AbortController()

    """
    abort - Send a signal to the agent to abort a task
    """
    def abort(self):
        user_id = self.get("input.user_id")
        self.abort_controller.send_signal(user_id, True)

    """
    is_aborted - Check if the agent has sent a signal to abort a task
    """
    def is_aborted(self):
        user_id = self.get("input.user_id")
        return self.abort_controller.get_signal(user_id)

    # In the get method, we split the key using the dot
    # as a delimiter and then recursively fetch the value
    # from the nested dictionary structure.
    def get(self, key: str, default: str = None):
        with self.lock:  # Acquire lock before accessing
            keys = key.split('.')
            value = self.context_data
            for k in keys:
                value = value.get(k, None)
                if value is None:
                    if default is not None:
                        return default
                    return None
            return value

    # In the set method, we split the key using the dot
    # as a delimiter and then recursively set the value
    # in the nested dictionary structure.
    def set(self, key: str, value):
        if key == "response":
            logger.info(f"Setting response: {value}")
        keys = key.split('.')
        target = self.context_data
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        target[keys[-1]] = value

    def delete(self, key: str):
        keys = key.split('.')
        target = self.context_data
        for k in keys[:-1]:
            target = target.get(k, None)
            if target is None:
                return
        target.pop(keys[-1], None)

    def pretty_print(self, key=None):
        if key is None:
            return json.dumps(self.context_data, default=self._json_serializable, indent=4)
        if key in self.context_data:
            return json.dumps(self.context_data[key], default=self._json_serializable, indent=4)
        else:
            raise ValueError(f"Key {key} not found in context")

    def _json_serializable(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, "name"):
            return {"name": obj.name}
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def has_key(self, key: str) -> bool:
        value = self.context_data.get(key, None)
        if value is None:
            return False
        else:
            return True
    
    def get_messages(self, prefix="", postfix=""):
        messages = []
        for message in self.get('input.messages')[:-1]:
            if message['role'] == 'user':
                messages.append(f"{prefix}{message['content']}{postfix}")
            elif message['role'] == 'assistant':
                messages.append(message['content'])
        return " ".join(messages)

    def format_template(self, prompt_template, **kwargs):
        logger.info("FORMAT_TEMPLATE")
        logger.info(kwargs)
        # Find all placeholders in the prompt_template
        template = Template(prompt_template)
        rendered_str = template.render(kwargs)
        logger.info("INPUT")
        logger.info(rendered_str)
        return rendered_str

    ### Helper function to get entire formatted prompt
    def get_formatted(self):
        prompt_template = self.prompts[self.get('model.prompt_config.prompt_template')]
        biography = self.get('model.persona.biography')
        memory = self.get('recall')
        if memory is not None and memory.strip() == "":
            memory = None
        plan = self.get('plan', None)
        new_plan = self.get('new_plan', None)
        instruction = self.get('prompt')
        username = self.get('input.user_name', "Human")
        agentname = self.get('model.persona.display_name', "Agent")
        query = self.get('query', None)
        message_history = self.get_messages(prefix=f"\n{username}: ", postfix=f"\n{agentname}:")
        ack = self.get('ack', None) # if response was an acknowledgement, we want to drop it
        image_response = self.get('image_response', None)
        knowledge = self.get('knowledge', None)
        voice = self.get('model.model_config.speech', False)

        ### VALIDATE FORMATTED TEMPLATE
        # formatted_template cannot be greater than the context window size of the model (and is preferably less)
        # we need to tokenize the formatted template and check the length
        # if the length is greater than the context window size, we need to truncate the formatted template
        # To do so we will summarize our most recent memories and truncate the formatted template to fit
        
        # TODO: Implement this, pull this logic out into it's own function so we can reformat the template
        # i.e. session history back-off, summarization of memories, etc.

        # print(prompt_template,
        #     name,
        #     instruction,
        #     f"biography: {biography}"
        #     f"mem: {memory}"
        # )


        return self.format_template(
            prompt_template,
            name=agentname,
            instruction=instruction,
            biography=biography,
            memory=memory,
            human=username,
            plan=plan,
            new_plan=new_plan,
            image_response=image_response,
            knowledge=knowledge,
            query=query,
            message_history=message_history,
            voice=voice,
            ack=ack,
            # current_date=datetime.now().strftime("%Y-%m-%d"),
        )
    
    def get_model_input(self):
        return {
            "user_id": self.get("input.user_id"),
            "session_id": self.get("input.id"),
            "prompt": self.get('prompt'),
            "generation_config": self.get('model.generation_config'),
            "model_config": self.get('model.model_config'),
        }

    def read_prompts(self):
        directory = os.path.join(os.path.dirname(__file__), './prompts')
        prompts_dict = {}
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    prompts_dict[filename] = content
        return prompts_dict

    def process_prompt(self, prompt: str, values: Dict) -> str:
        for k,v in values.items():
            prompt = prompt.replace(f"<|{k}|>", str(v))
        return prompt