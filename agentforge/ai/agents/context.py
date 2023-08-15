import json, uuid
from typing import Dict
from agentforge.utils import Parser

class Context:
    def __init__(self, init: Dict = {}) -> None:
        self.parser = Parser()
        self.context_data = {}
        self._id = uuid.uuid4()
        for k,v in init.items():
            self.set(k, v)

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

    def pretty_print(self):
        return json.dumps(self.context_data, indent=4)

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
        name = self.get('model.avatar_config.name')
        biography = self.get('model.avatar_config.biography')
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
