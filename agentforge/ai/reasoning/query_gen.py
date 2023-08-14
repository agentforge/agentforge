from typing import Any, Dict
from agentforge.ai.agents.context import Context
from agentforge.ai.planning.pddl_to_graph import get_seed_queries

### REASONING: We need to identify the gaps in our knowledge that we need to fill
### This can either come from a Task or come from the agent's inner-reflections
class QueryGenerator:
  def __init__():
    pass

  def execute(self, context: Context) -> Dict[str, Any]:
    ### Consider the following: 
    # 
    #   Current Task (if any)
    #   Attentional State
    #   Current Goal
    #   Current Belief State
    #   Current Knowledge State
    #   Current Memory State
    #   Current Context
    #   Current Environment
    ###
    goal = context.get("goal")

    ### If the Task exists, is active, and has a query, we should ask it
    if self.task_manager.task_exists():
      task = self.task_manager.get_active_task()
      if task.has_query():
        return task.get_query()
    
    ### If there is an attention formed but no active task, we should identify what task to activate
    if self.attention.has_attention():
      task = self.task_manager.get_active_task()
      if task == None:
        return self.attention.get_attention()
      
    ### If there are gaps in our knowledge, we should try to close those gaps
    queries = get_seed_queries(goal)
    for query_obj, details in queries.items():
      # Create a prompt and query for each query_obj
      pass
    if self.knowledge.has_gaps():
        for gap in self.knowledge.get_gaps():
          return self.query_engine.generate_query(gap)
    
    pass
    