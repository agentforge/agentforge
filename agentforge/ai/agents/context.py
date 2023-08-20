import json, uuid, os
from typing import Dict
from agentforge.utils import Parser
from agentforge.utils import AbortController

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
        self.parser = Parser()
        self.task_routines = {}
        self.context_data = {}
        self.prompts = self.read_prompts()
        self.abort_controller = AbortController()
        self._id = uuid.uuid4()
        for k,v in init.items():
            self.set(k, v)

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
    def get(self, key: str):
        keys = key.split('.')
        value = self.context_data
        for k in keys:
            value = value.get(k, None)
            if value is None:
                return None
        return value

    # In the set method, we split the key using the dot
    # as a delimiter and then recursively set the value
    # in the nested dictionary structure.
    def set(self, key: str, value):
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
            return json.dumps(self.context_data, indent=4)
        if key in self.context_data:
            return json.dumps(self.context_data[key], indent=4)
        else:
            raise ValueError(f"Key {key} not found in context")

    def has_key(self, key: str) -> bool:
        keys = key.split('.')
        value = self.context_data
        for k in keys:
            value = value.get(k, None)
            if value is None:
                return False
        return False

    ### Helper function to get entire formatted prompt
    def get_formatted(self):
        prompt_template = self.get('model.prompt_config.prompt_template')
        name = self.get('model.persona.name')
        biography = self.get('model.persona.biography')
        memory = self.get('recall')
        instruction = self.get('prompt')
        
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

        return self.parser.format_template(
            prompt_template,
            name=name,
            instruction=instruction,
            biography=biography,
            memory=memory,
            human="Human"
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