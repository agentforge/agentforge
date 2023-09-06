from typing import Any, Dict, List
from agentforge.ai.planning.planner import PlanningController
from agentforge.ai.beliefs.symbolic import SymbolicMemory
from agentforge.ai.attention.tasks import TaskManager
from agentforge.utils.stream import stream_string
from agentforge.interfaces import interface_interactor
from agentforge.utils import logger
from agentforge.ai.planning.pddl import PDDLGraph, PDDL
from agentforge.ai.reasoning.query import Query
from agentforge.ai.reasoning.relation import Relation
from agentforge.ai.agents.context import Context

### PLANNING SUBROUTINE: Executes PDDL plans with help from LLM resource
class Plan:
    ### Executes PDDL plans with help from LLM resource
    def __init__(self, domain: str, goals: List[str]):
        self.llm = interface_interactor.get_interface("llm")
        self.planner = PlanningController(domain)
        self.task_management = TaskManager()
        self.domain = domain
        self.goals = goals
        domain_file = self.planner.config.domain_pddl_file_path
        problem_file = self.planner.config.domain_pddl_problem_path
        self.pddl_graph = PDDLGraph(domain_file, problem_file)
        self.pddl = PDDL()

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
        done = task.done()

        print(f"PLAN PLAN PLAN{task != None} and {not done} and {len(task.all())}")
        print(task != None and not done and len(task.all()))
        print(task)

        # if task in progress but no queries, generate them and create the PDDL Plan callback
        if task != None and not done and len(task.all()) == 0:
            # Get the current goal
            goal = self.goals[task.stage]
            print("GOAL", goal)
            queries = self.gather(goal)

            print(f"{queries=}")
            list(map(task.push, queries)) # efficiently push queries to the task
            logger.info(f"{task=}")

        if task != None and not done:
            ### Get activated query if any
            query = task.activate_query()

            query = Query().get(context, query)

            ## Capture Relational Information
            # query = Relation().extract(context, query)

            logger.info(f"{query=}")
            # raise ValueError("STOP")
            context.set("response", query['text'])

            self.task_management.save(task)

        elif task != None and done:
            finalize_reponse = "I have all the info I need, let me finalize the plan."

            goal = self.goals[task.stage]
            problem_data = self.pddl.create_pddl_problem_state(task.actions["complete"], goal, self.pddl_graph)
            logger.info(problem_data)
            logger.info("Creating PDDL Plan")

            # TODO: Make channel user specific, make text plan specific
            stream_string('channel', finalize_reponse, end_token=" ")

            context.set("response", finalize_reponse)
            response = self.planner.execute(context.get_model_input(), task, problem_data)

            task.active = True
            # setup plan as next action in task sequence
            task.push({"plan_nl": response, "plan": self.planner.best_plan, "cost": self.planner.best_cost, "metatype": "plan"})
            self.task_management.save(task)
            context.set("response", response)
            return context

        return context
