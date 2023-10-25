from typing import Any, Dict
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils import logger


### BELIEFS: Stores a context for a user in the memory
### Update: Stores symbolic information from query response
class Acknowledge:
    def __init__(self, domain):
        self.domain = domain
        self.task_management = TaskManager()
        self.symbolic_memory = SymbolicMemory()
        self.zeroshot = ZeroShotClassifier()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_id = context.get('input.user_id')
        session_id = context.get('input.model_id')
        key = f"{user_id}:{session_id}"
        self.symbolic_memory.load(key)

        ### UPDATE_BELIEFS
        # # if query exists and is a response, pop
        task = context.get("task")
        valid_response = False
        query = task.get_active_query()

        if query is None:
            return context

        # use zeroshot to quick and dirty check if the user is talking about something else
        # prompt = "### Instruction: Is the following output not a followup or other question and a valid response to the input? Input: {question} Output: {response} ### Response:"
        # valid_response = self.zeroshot.classify(prompt, ["Yes", "No"], {"type": query['datatype'], "question": query['text'], "response": context.get("instruction")}, context, max_new_tokens=1)
        # response_func = lambda s: True if s.lower() == 'yes' else False if s.lower() == 'no' else None
        # valid_response = response_func(valid_response)
        # logger.info(f"VALID RESPONSE ACK {valid_response}")
        
        learned = False
        results = []
        valid_response = True
        
        if valid_response:
            # raise ValueError("query not none")
            # feed in to the OPQL
            query["response"] = context.get("instruction") # The user response comes in as a prompt
             # TODO: Make channel user specific, make text plan specific
            # stream_string('channel', "One moment while I make a note.", end_token="\n\n")
            logger.info(query)

            learned, results = self.symbolic_memory.learn(query, context)
            logger.info("[LEARNED]")
            logger.info(learned)
            logger.info(results)
            query["results"] = results

            if learned:
                # TODO: Make channel user specific, make text plan specific
                # stream_string('channel', "Okay I've jotted that down.", end_token=" ")
                logger.info("PUSH COMPLETE")
                task.push_complete(query)
                self.task_management.save(task)
                self.symbolic_memory.save(key)
                context.set('task', task)
                context.set('ack', results)
                return context

        # Fail state
        logger.info(f"PUSH FAILED {valid_response}")
        if valid_response and len(results) == 0:
            task.push_failed(query)
        else:
            task.push_active(query)
        self.task_management.save(task)
        context.set('task', task)
        return context
