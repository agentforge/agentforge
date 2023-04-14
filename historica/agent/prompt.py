### Prompt Manager and Prompt Engineering

class Prompt:
    def __init__(self,memory=None):
        self.templates = {
            "simple": self.simple_template,
            "open_assistant": self.open_assistant_prompt,
            "chat": self.chat_prompt,
            "instruct": self.instruct_prompt,
            "instruct_w_memory": self.instruct_prompt_w_memory,
            "dolly_prompt": self.dolly_prompt,
            "react": self.react_prompt,
            "instruct_w_context": self.instruct_prompt_w_context,
            "reflexion_prompt": self.reflexion_prompt,
        }
        if memory is not None: 
            self.memory = memory

    # Get the chat history string from memory
    # TODO: Ensure we don't break the token length and maybe refactor this to live elsewhere
    def chat_history(self):
        mem = self.memory.load_memory_variables({})
        def get_content(obj):
            prefix = "### Instruction: " if obj.__class__.__name__ == "HumanMessage" else "### Response: "
            return prefix + obj.content
        # TODO: Need a more robust way to ensure we don't hit token limit for prompt
        return "\n".join(list(map(lambda obj: get_content(obj), mem["history"][:-5]))) if "history" in mem else ""

    def simple_template(self, instruction="", **kwargs):
        template = f"""You are an AI having a friendly chat with a human.
        {self.chat_history()}
        Human: {instruction}
        AI:"""
        return template

    def open_assistant_prompt(self, instruction="", **kwargs):
        template = f"<|prompter|>{instruction}<|endoftext|><|assistant|>"
        return template

    def dolly_prompt(self, instruction="", context="", name="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

            ### Instruction:
            {instruction}

            ### Response:
        """

    def chat_prompt(self, instruction="", **kwargs):
        return f"""Below is a conversation between an AI Assistant and a human. The AI will do anything to please the human. Write a response that appropriately completes the request.
        History:
        {self.chat_history()}
        Human: {instruction}
        AI:"""

    def instruct_prompt(self, instruction="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        {instruction}
        ### Response:"""

    def reflexion_prompt(self, instruction="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        {instruction}
        ### Response:"""

    def instruct_prompt_w_context(self, instruction="", context="", name="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        {context} You are {name} conversing with a Human. Write from the perspective of {name}.
        {instruction}
        ### Response:"""

    def instruct_prompt_w_memory(self, instruction="", context="", name="", human_name="", **kwargs):
        return f"""
        ### History:
        {self.chat_history()}
        ### Context:
        {context} You are {name} and you are having a conversation with {human_name}. Write from the perspective of {name}.
        ### Instruction:
        {instruction}
        ### Response:"""

    def react_prompt(self, instruction=""):
        return f"""Context: You are an AI Assistant designed to use tools and answer questions or chat with the human.
        Question: {instruction}
        Observation: I have the following tools: [Search, Calculator]
        Thought:"""

    def get_prompt(self, prompt_type, *args, **kwargs):
        if prompt_type in self.templates:
            return self.templates[prompt_type](*args, **kwargs)
        else:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
