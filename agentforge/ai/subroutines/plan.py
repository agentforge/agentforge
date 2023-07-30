from typing import Any, Dict
from agentforge.ai.cognition.planner import PlanningController
from agentforge.ai.cognition.query_engine import QueryEngine
from agentforge.ai.cognition.symbolic import PredicateMemory
from agentforge.ai.cognition.flow import FlowManagement
from agentforge.utils.stream import stream_string

class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self):
        self.planner = PlanningController()
        self.predicate_memory = PredicateMemory()
        self.flow_management = FlowManagement()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        input_ = {
            "user_id": context["input"]["user_id"],
            "session_id": context["input"]["id"],
            "prompt": context['input'],
            "generation_config": context['model_profile']['generation_config'],
            "model_config": context['model_profile']['model_config'],
        }

        query_engine = QueryEngine(context["input"]['user_id'], context["input"]['id'])
        user_id = context['input']['user_id']
        session_id = context['input']['id']
        key = f"{user_id}-{session_id}-plan-{self.planner.config.domain}"

        # # if query exists and is a response, pop
        sent = query_engine.get_sent_queries()
        if len(sent) > 0:
            query = sent[0]
            # feed in to the OQAL
            # raise Exception(context["input"]["prompt"])
            query["response"] = context["input"]["prompt"]
            print("I'm learning...")
            stream_string('channel', "One moment while I make a note.", end_token=" ") # TODO: Make channel user specific, make text plan specific
            learned, results = self.predicate_memory.learn(query, context) # TODO: I doubt the user formats the response correctly, we should rely on the LLM here
            print(learned, results)
            if learned:
                stream_string('channel', "Okay I've jotted that down.", end_token=" ") # TODO: Make channel user specific, make text plan specific
                self.predicate_memory.satisfy_attention(key, query, results)
                query_engine.pop_query()

        # If the predicate memory attention is satisfied kick off the plan
        if self.predicate_memory.attention_satisfied(key):
            print("attention satisfied...")
            stream_string('channel', "I have all the info I need, let me finalize the plan.", end_token=" ") # TODO: Make channel user specific, make text plan specific
            response = self.planner.execute(input_, self.predicate_memory.get_attention(key))
            self.flow_management.update_flow(user_id, session_id, "plan", False)
            print("[PLAN][update_flow]", user_id, session_id, "plan", False)
            context["response"] = response
            return context

        # If the predicate memory attention does not exist, feed plan queries into the current attention
        if not self.predicate_memory.attention_exists(key):
            print("attention not exists...")
            stream_string('channel', "Okay let's formulate a plan.", end_token=" ") # TODO: Make channel user specific, make text plan specific
            queries = self.planner.domain.get_queries()
            query_engine.create_queries(queries)
            self.predicate_memory.create_attention(queries, key)
        else:
            queries = query_engine.get_queries()

        print("checking queries")
        # Iterate through unsent queries and send the latest
        for query in queries:
            if query is not None:
                print("asking a query", query['query'])
                query_engine.update_query(sent=True)
                stream_string('channel', query['query']) # TODO: Make channel user specific
                print("sending ", query['query'])
                context["response"] = query['query']
                # Return new context to the user w/ response
                return context

        return context