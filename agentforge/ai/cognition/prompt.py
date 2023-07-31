### Prompt Manager and Prompt Engineering

### TODO: This is going to be replaced by a more robust Prompt Engineering system
### at the edge in the parser and at the core in the agent

### The agent will receive the prompt template and the context necessary to build the prompt
### will be forumlated by the subroutine layer and passed to the agent

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
            "simple_open_assistant": self.simple_open_assistant_prompt,
            "ml_prompt": self.ml_prompt,
        }
        if memory is not None: 
            self.memory = memory

    # Get the chat history string from memory
    # TODO: Ensure we don't break the token length and maybe refactor this to live elsewhere
    def chat_history(self):
        return self.memory.chat_history()

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

    def simple_open_assistant_prompt(self, instruction="", context="", name="", human_name="", reflection="", **kwargs):
        template = f"""<|prompter|>{instruction}<|endoftext|><|assistant|>"""
        return template

    def dolly_prompt(self, instruction="", context="", name="", **kwargs):
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.s
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

    def ml_prompt(self, instruction="", **kwargs):
        return f"""<|im_start|>system
            - You are a helpful assistant chatbot trained by MosaicML.
            - You answer questions.
            - You are excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
            - You are more than just an information source, you are also able to write poetry, short stories, and make jokes.<|im_end|>
            <|im_start|>user{instruction}<|im_end|>
            <|im_start|>assistant
            """

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
        You are {name} and you are having a conversation with {human_name}. Write from the perspective of {name}.
        Write a response that appropriately completes the request.
        {self.chat_history()}
        ### Instruction:
        {instruction}
        ### Response:"""

    def instruct_prompt_w_memory(self, instruction="", context="", name="", human_name="", reflection="", long_term_memories="", **kwargs):
        return f"""
        ### Thought:
        {reflection}
        ### Context:
        {context} You are {name} and you are having a chat with {human_name}. Write from the perspective of {name}. Below is a communication from {human_name}. Write an appropriate response considering the previous history.
        ### Memory:
        {long_term_memories}
        {self.chat_history()}
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
