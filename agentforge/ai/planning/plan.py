from typing import Any, Dict
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.reasoning.query_engine import QueryEngine
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManagement
from agentforge.utils.stream import stream_string

### PLANNING: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self):
        self.planner = PlanningController()
        self.symbolic_memory = SymbolicMemory()
        self.task_management = TaskManagement()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        input_ = {
            "user_id": context["input"]["user_id"],
            "session_id": context["input"]["id"],
            "prompt": context['input'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }

        query_engine = QueryEngine(context["input"]['user_id'], context["input"]['model_id'])
        user_id = context['input']['user_id']
        session_id = context['input']['model_id']
        key = f"{user_id}-{session_id}-plan-{self.planner.config.domain}"

        ## TODO: CHECK BELIEFS
        ## Check if a plan already exists and there is no other queries in progress
        ## If this is the case we enquire if the user wants to browse other plans or
        ## create a new plan
        ## This step is the confirmation step preferably achieved by CoT Reasoning Engine


        ### UPDATE_BELIEFS
        # # if query exists and is a response, pop
        print("[INPUT] ", context["input"])
        sent = query_engine.get_sent_queries()
        if len(sent) > 0:
            query = sent[0]
            # feed in to the OQAL
            # raise Exception(context["input"]["prompt"])
            query["response"] = context["input"]["prompt"] # The user response comes in as a prompt
            print("[PLAN] Learning new information...")
            stream_string('channel', "One moment while I make a note.", end_token=" ") # TODO: Make channel user specific, make text plan specific
            learned, results = self.symbolic_memory.learn(query, context) # TODO: I doubt the user formats the response correctly, we should rely on the LLM here
            print(learned, results)
            if learned:
                stream_string('channel', "Okay I've jotted that down.", end_token=" ") # TODO: Make channel user specific, make text plan specific
                self.symbolic_memory.satisfy_attention(key, query, results)
                query_engine.pop_query()

        ### PLANNING
        # If the predicate memory attention is satisfied kick off the plan
        if self.symbolic_memory.attention_satisfied(key):
            print("attention satisfied...")
            finalize_reponse = "I have all the info I need, let me finalize the plan."
            stream_string('channel', finalize_reponse, end_token=" ") # TODO: Make channel user specific, make text plan specific
            
            context["response"] = finalize_reponse
            response = self.planner.execute(input_, self.symbolic_memory.get_attention(key))
            
            self.task_management.update_task(user_id, context["input"]["model_id"], "plan", is_active=False)
            print("[PLAN][update_task]", user_id, context["input"]["model_id"], "plan", False)
            context["response"] = response
            return context

        ### UPDATE BELIEFS
        # If the predicate memory attention does not exist, feed plan queries into the current attention
        if not self.symbolic_memory.attention_exists(key):
            print("[PLAN] Creating new Attention to Plan")

            response = "Okay let's formulate a plan."
            stream_string('channel', response, end_token=" ") # TODO: Make channel user specific, make text plan specific
            context["response"] = response

            queries = self.planner.domain.get_queries()
            query_engine.create_queries(queries)
            self.symbolic_memory.create_attention(queries, key)
        else:
            queries = query_engine.get_queries()

        ### COMMUNICATION
        # Iterate through unsent queries and send the latest
        for query in queries:
            if query is not None:
                print("[PLAN] asking a query", query['query'])
                query_engine.update_query(sent=True)
                stream_string('channel', query['query']) # TODO: Make channel user specific
                context["response"] = query['query']
                # Return new context to the user w/ response
                return context

        return context