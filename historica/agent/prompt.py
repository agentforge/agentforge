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
            "no_prompt": self.no_prompt,
            "reflection": self.reflection,
            "observation": self.observation,
            "open_assistant_prompt": self.open_assistant_prompt,
        }
        if memory is not None: 
            self.memory = memory

    # Get the chat history string from memory
    # TODO: Ensure we don't break the token length and maybe refactor this to live elsewhere
    def chat_history(self):
        print("ACCESSING CHAT MEMORY")
        mem = self.memory.load_memory_variables({})
        def get_content(obj):
            prefix = "### Instruction: " if obj.__class__.__name__ == "HumanMessage" else "### Response: "
            return prefix + obj.content
        # TODO: Need a more robust way to ensure we don't hit token limit for prompt
        return "\n".join(list(map(lambda obj: get_content(obj), mem["history"][-5:]))) if "history" in mem else ""

    # no prompt is useful for experiments
    def no_prompt(self, instruction="", **kwargs):
        template = f"""{instruction}"""
        return template

    def simple_template(self, instruction="", **kwargs):
        template = f"""You are an AI having a friendly chat with a human.
        {self.chat_history()}
        Human: {instruction}
        AI:"""
        return template

    def open_assistant_prompt(self, instruction="", context="", name="", human_name="", reflection="", **kwargs):
        template = f"""<|prompter|>
        {context} Your latest thought is the following. {reflection}
        You are {name} and you are having a conversation with {human_name}. Write from the perspective of {name}. Write a response that appropriately completes the request: {instruction} <|endoftext|><|assistant|>"""
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

    def reflection(self, instruction="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        Reflect on how the following statement statement makes you feel: You are a bad person.
        ### Response: This makes me feel bad.
        ### Instruction:
        Reflect on how the following statement statement makes you feel: I love you.
        ### Response: This makes me feel a profound sense of love.
        ### Instruction:
        Reflect on how the following statement statement makes you feel: {instruction}
        ### Response:
        """

    def observation(self, instruction="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        Does the following prompt require you to take action? Reply Yes or No: I need help
        ### Response: Yes
        ### Instruction:
        Does the following prompt require you to take action? Reply Yes or No: I am bored
        ### Response: No
        ### Instruction:
        Does the following prompt require you to take action? Reply Yes or No: Call my caretaker
        ### Response: Yes
        ### Instruction:
        Does the following prompt require you to take action? Reply Yes or No: {instruction}
        ### Response:
        """

    def instruct_prompt_w_context(self, instruction="", context="", name="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        ### Instruction:
        {context} You are {name} conversing with a Human. Write from the perspective of {name}.
        {instruction}
        ### Response:"""

    def _informal_instruct_prompt_w_memory(self, instruction="", context="", name="", human_name="", reflection="", **kwargs):
        return f"""
        {context} Your latest thought is the following. {reflection} Below is an instruction that describes a task.
        Write a response that appropriately completes the request. Write a response that appropriately completes the request.
        You are {name} and you are having a conversation with {human_name}. Write from the perspective of {name}. Write only a single response.
        {self.chat_history()}
        ### Instruction:
        {instruction}
        ### Response:"""

    def instruct_prompt_w_memory(self, instruction="", context="", name="", human_name="", reflection="", **kwargs):
        return f"""
        ### History:
        {self.chat_history()}
        ### Thought:
        {reflection}
        ### Context:
        {context} You are {name} and you are having a conversation with {human_name}. Write from the perspective of {name}. Write only a single response.
        ### Instruction:
        {instruction}
        ### Response:"""

    def react_prompt(self, instruction=""):
        return f"""Context: You are an AI Assistant designed to use tools and answer questions or chat with the human.
        Question: {instruction}
        Observation: I have the following tools: [Search, Calculator]
        Thought:"""

    def synthesis_prompt(self, instruction=""):
        return f"""You are [Name of famous expert 1], together with [Name of famous expert 2] you are reviewing this document:
        {instruction}
        You take turns discussing and suggesting improvement points, until you at the end, rewrite only the document and implement all the suggestions."""

    def get_prompt(self, prompt_type, *args, **kwargs):
        if prompt_type in self.templates:
            return self.templates[prompt_type](*args, **kwargs)
        else:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
