
### Executive Cognition
### Handles Model Ensemble Coordination
### Higher level memory and reasoning loops

import threading
# from agentforge.ai import Avatar
from agentforge.interfaces import APIService
from agentforge.ai import Agent
from flask_sse import sse
from agentforge.utils import logger

### TODO: Convert this to a helper for cognitive tasks
class ExecutiveCognition:
    def __init__(self) -> None:
        self.avatar = {} # Avatar() # personality
        self.agent = Agent() # agency, reason, memory, prompt engineering
        self.thoughts = {} # thoughts hack #TODO: replace with memory
        self.service = APIService()
        self.lock = threading.Lock() # for async calls

    # Either return a wav file or a mp4 file based on flag
    def speak(self, prompt, form_data):
        # Get wav/tts file
        avatar = self.avatar.get_avatar(form_data["avatar"])
        form_data["avatar"] = avatar

        prompt = self.agent.parser.parse_prompt(prompt)
        wav_response = self.service.call_tts(form_data)

        # if we want to generate lipsync
        if "lipsync" in form_data and form_data["lipsync"] != 'false':
            form_data["wav_file"] = wav_response["filename"]
            lipsync_response = self.service.call_lipsync(form_data)
            return {"filename": lipsync_response["filename"], "type": "video/mp4"}

        # else just return the wav file
        return {"filename": wav_response["filename"], "type": "audio/wav"}

    # Takes a sound file and returns a text string
    def interpret(self, form_data):
        # Get wav/tts file
        json_response = self.service.call_interpret(form_data)

        # else just return the wav file
        return json_response

    # Responds to a user prompt -- queries LLM and returns a response
    # Reflects on the prompt and returns a reflection
    def respond(self, prompt, form_data, app):
        # Validate form data
        for v in ["prompt", "avatar"]:
            if v not in form_data:
                return {"error": f"User must stipulate {v} for response"} # return error

        # Configure agent with new config
        form_data["avatar"] = self.avatar.get_avatar(form_data["avatar"])
        self.agent.configure(form_data)

        # Get recent memories about this prompt
        self.agent.memory.recall(prompt)

        # Record raw prompt in memory
        self.agent.save_speech(prompt)

        # Format prompt with our Prompt engineering
        formatted_prompt = self.agent.process_prompt(instruction=prompt, config=form_data)
        form_data["prompt"] = formatted_prompt
        if "reflection" in self.thoughts and self.thoughts["reflection"] is not None:
            form_data["avatar"]["prompt_context"]["reflection"] = self.thoughts["reflection"]

        # Get response from LLM
        response = self.service.call_llm(form_data)
        logger.info(response)
        if "choices" not in response:
            return {"error": response} # return error

        text = response["choices"][0]["text"]

        # Parse response
        response["choices"][0]["text"] = self.agent.process_completion(text, form_data) # backwards compatibility

        # Record response in memory
        self.agent.save_response(response["choices"][0]["text"])
        self.agent.memory.remember(prompt, response["choices"][0]["text"], app)

        form_data["prompt"] = prompt
        logger.info(f"PROMPT: {prompt}")

        # Asyncronous reaction/reflection on this conversation -- how the agent feels, should it act, etc.
        # self.react(prompt, text, form_data, app)

        return response

    # Use ReAct Agent (from langchain?) to take action in response to this observation
    def action(self, prompt, response, form_data, thought):
        pass # TODO

    # Asyncronous reflection on this conversation -- how the agent feels, should it act, etc.
    def react(self, prompt, text, form_data, app):
        observation_thread_args=(prompt, text, form_data, {"type": "observation", "callback": self.action}, app)
        observation_thread = threading.Thread(target=self.thought_with_app_context, args=observation_thread_args )
        observation_thread.start()

        reflection_thread_args=(prompt, text, form_data, {"type": "reflection", "callback": None}, app)
        reflection_thread = threading.Thread(target=self.thought_with_app_context, args=reflection_thread_args )
        reflection_thread.start()

    # Locking and thread ontext for async thought processing
    def thought_with_app_context(self, prompt, response, form_data, thought, app):
        with app.app_context():
            with self.lock:
                self.think(prompt, thought, form_data)

    # queries the local visual environmemt for contextual information
    def query_vision(self, prompt):
        pass # TODO

    # Runs an observation loop to determine if we need to adjust our on-going prompt context
    def adapt_communication(self, prompt, form_data):
        pass # TODO

    # Thought function provides necessary components to prompt the LLM for information either within an agent loop or externally
    # optionally publish to SSE
    def think(self, prompt, thought, form_data, publish=True):
        # Get prompt
        prompt = self.agent.prompt_manager.get_prompt(thought["type"], instruction=prompt)
        # Format prompt
        # prompt = self.agent.process_prompt(instruction=prompt, config=form_data)
        # Informational prompts are restricted to 128 tokens
        form_data["prompt"] = prompt
        form_data["streaming"] = False
        form_data["max_new_tokens"] = 128

        response = self.service.call_llm(form_data)
        text = response["choices"][0]["text"]

        # Parse response
        response["choices"][0]["text"] = self.agent.process_completion(text, form_data, skip_tokens=["\n"]) # backwards compatibility

        self.thoughts[thought["type"]] = response["choices"][0]["text"]
        if publish:
            sse.publish({f"{thought['type']}": response}, type=thought["type"])
        
        # Run callback -- action in response to this thought
        if "callback" in thought and thought["callback"] is not None:
            thought["callback"](prompt, response, form_data, thought)
    
    # Implement proactive social interaction here
    # Game loops, prompts, agentforgel avatars to talk to, etc.
    def social_interaction_features(elderly_person):
        pass
