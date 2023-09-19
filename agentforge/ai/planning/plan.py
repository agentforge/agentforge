from typing import Any, Dict, List
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManager
from agentforge.ai.beliefs.state import StateManager
from agentforge.utils.stream import stream_string
from agentforge.interfaces import interface_interactor
from agentforge.utils import logger
from agentforge.ai.planning.pddl import PDDLGraph, PDDL
from agentforge.ai.reasoning.query import Query
from agentforge.ai.reasoning.relation import Relation
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.zeroshot import ZeroShotClassifier

### PLANNING SUBROUTINE: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self, domain: str, goals: List[str]):
        self.llm = interface_interactor.get_interface("llm")
        self.planner = PlanningController(domain)
        self.task_management = TaskManager()
        self.state_management = StateManager()
        self.domain = domain
        self.goals = goals
        domain_file = self.planner.config.domain_pddl_file_path
        problem_file = self.planner.config.domain_pddl_problem_path
        self.pddl_graph = PDDLGraph(domain_file, problem_file, domain)
        self.pddl = PDDL(self.pddl_graph)

    """
        Gether information phase of the planning task
        -- gather from user, environment, and memory
    """
    def gather(self, goal: str) -> List[Dict[str, Any]]:
        # Creates queries for the planning task
        seeds = self.pddl_graph.get_seed_queries(goal)
        goal_data = goal.split(" ")
        goal = goal_data[0] # split the goal into the goal and the object, 1st is always predicate

        logger.info(f"{seeds=}")
        queries = []
        for action_name, seed_list in seeds.items():
            for seed in seed_list:
                seed['goal']  = goal
                seed['metatype']  = "query"
                seed['action'] = action_name
                queries.append(seed)
        return queries

    # Helper function to explore knowledge graph/PDDL and create queries for our plan
    # if we need them
    def init_queries(self, task, context):
        # Get the current goal
        goal = self.goals[task.stage]
        logger.info("GOAL", goal)
        queries = self.gather(goal)
        logger.info(f"{queries=}")
        list(map(task.push, queries)) # efficiently push queries to the task
        logger.info(f"{task=}")
        self.task_management.save(task)
        return self.init_query(task, context)

    # Helper function to activate a query
    def init_query(self, task, context):
        query = task.activate_query()
        logger.info(f"INIT QUERY {query}")
        if query is not None:
            if 'text' in query:
                response = query['text']
            else:
                # only stream the new query if we are on the happy path
                query = Query().get(context, query, streaming=False)
                ## Capture Relational Information
                # query = Relation().extract(context, query)
                logger.info(f"{query=}")
                # raise ValueError("STOP")
                response = query['text']

            context.set("query", response)
            self.task_management.save(task)
        return context

    def execute(self, context: Context) -> Dict[str, Any]:
        user_id = context.get('input.user_id')
        session_id = context.get('input.model_id')
        key = f"{user_id}:{session_id}:{self.domain}"

        ## TODO: CHECK BELIEFS
        ## Check if a plan already exists and there is no other queries in progress
        ## If this is the case we enquire if the user wants to browse other plans or
        ## create a new plan
        ## This step is the confirmation step preferably a`chieved by CoT Reasoning Engine

        ### PLANNING
        # If there are no remaining queries for the planning task, we can execute the plan
        task = context.get("task")

        ### If there is no task we should not engage in planning at this time...
        if task is None:
            return context

        user_done = False
        agent_done = True #TODO: When we add agent actions we need to make this smarter

        ### Check additional user intent on plan
        plan = task.get_active_plan()
        user_input = context.get("instruction")

        ## TEST: Determine if the user has completed a plan
        if plan is not None:
            z = ZeroShotClassifier()
            z_val = z.classify("### Instruction: Does this imply the user has completed the current plan? Respond with Yes or No. ### Input: {{user_input}} ### Response: ", ["Yes", "No"], {"user_input": user_input}, context)
            if z_val == "Yes":
                task.push_complete(plan)
                task.iterate_stage_and_flush()
                self.pddl.execute_plan(plan)
                user_done = True
                ## Move the plan to the next stage and trace graph to create new queries.
                if task.stage >= len(self.goals):
                    ## If the next stage does not exist, congragulate the user! Job well done
                    stream_string('channel', f"You've done it! You've completed the {task.name} plan.", end_token=" ")
                    # TODO: save and return here
                else:
                    # create new quer
                    context = self.init_queries(task, context)
                self.task_management.save(task)
                return context
            else:
                # stream_string('channel', "<PLAN-ACTIVE>", end_token=" ")
                context.set("plan", plan['plan_nl'])

        # Sample these after plan management
        empty_queue = task.is_empty_queue()
        empty_active = task.is_empty_active()
        empty_complete = task.is_empty_complete()
        logger.info(f"empty_queue: {empty_queue}, empty_active: {empty_active}, plan: {plan}, empty_complete: {empty_complete}")

        # GATHER NEW QUERIES FOR THIS STATE
        # if task in progress but no queries, generate them and create the PDDL Plan callback
        # Triggers when we have no actions queued/active and we are either at an end-stage
        # point initiated by the user/agent or 
        if empty_queue and empty_active and ((user_done and agent_done) or empty_complete):
            logger.info("GATHERING NEW QUERIES")
            context = self.init_queries(task, context)

        # QUERY USER: Activate a query if we have none active
        elif not empty_queue and empty_active:
            logger.info("ACTIVATING QUERY")
            context = self.init_query(task, context)

        # PLAN: Not a new instance/stage and no queries, we're at planning time
        elif empty_queue and empty_active and not plan:
            logger.info("PLANNING")
            ## Queries complete, let's execute the plan
            finalize_reponse = "I have all the info I need, let me finalize the current plan."

            goal = self.goals[task.stage]
            problem_data = self.pddl.create_pddl_problem_state(task.actions["complete"], goal)
            logger.info(problem_data)
            logger.info("Creating PDDL Plan")

            # TODO: Make channel user specific
            stream_string('channel', finalize_reponse, end_token=" ")

            response = self.planner.execute(context.get_model_input(), task, problem_data)

            task.active = True
            # setup plan as next action in task sequence
            plan_task = {
                "plan_nl": response,
                "plan": self.planner.best_plan,
                "cost": self.planner.best_cost,
                "metatype": "plan",
                "state": problem_data,
            }
            task.push(plan_task)
            task.activate_plan()
            self.task_management.save(task)
            context.set("plan_response", response)
            return context

        return context