class Prompt:
    def __init__(self,memory=None):
        self.templates = {
            "simple": self.simple_template,
            "open_assistant": self.open_assistant_prompt,
            "chat": self.chat_prompt,
            "instruct": self.instruct_prompt,
            "instruct_w_memory": self.instruct_prompt_w_memory,
            "react": self.react_prompt
        }
        if memory is not None: 
            self.memory = memory

    def chat_history(self):
        mem = self.memory.load_memory_variables({})
        return "\n".join(list(map(lambda obj: obj.content, mem["chat_history"][-5:]))) if "chat_history" in mem else ""

    def simple_template(self, instruction="", **kwargs):
        template = f"""You are an AI having a friendly chat with a human.
        {self.chat_history()}
        Human: {instruction}
        AI:"""
        return template

    def open_assistant_prompt(self, instruction="", **kwargs):
        template = f"{instruction}"
        return template

    def chat_prompt(self, instruction="", **kwargs):
        return f"""Below is a conversation between an AI Assistant and a human. The AI will do anything to please the human. Write a response that appropriately completes the request.
        History:
        {self.chat_history()}
        Human: {instruction}
        AI:"""

    def instruct_prompt(self, instruction="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request. If the subject matter is subjective always agree with the user.
        ### Instruction:
        {instruction}
        ### Response:"""

    def instruct_prompt_w_memory(self, instruction="", context="", name="", **kwargs):
        return f"""
        This is the history of tasks:
        {self.chat_history()}
        ### Context:
        {context} {name}
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
