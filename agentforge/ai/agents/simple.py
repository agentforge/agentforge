from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine
from agentforge.ai.routines.planning import PlanningRoutine
from agentforge.ai.beliefs.memory import Memory
from agentforge.ai.agents.statemachine import StateMachine
from agentforge.ai.agents.context import Context
import threading, json, os
from agentforge.utils import logger

def load(root_directory):
    json_list = []

    # Walk through the root directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Check if 'plan.json' is in the list of filenames
        if 'plan.json' in filenames:
            # Construct the full path to the file
            filepath = os.path.join(dirpath, 'plan.json')
            
            # Read and parse the JSON file
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Append the JSON object to the list
            json_list.append(data)
    
    return json_list

class SimpleAgent:
    def __init__(self):
        ### Primary Reactive Routine - handles user input
        self.routine = ReactiveRoutine()
        self.task_routines = {}
        # plan_routines = load(os.getenv("PLANNER_DIRECTORY"))
        # for plan in plan_routines:
        #     key = plan["name"]
        #     prompts = plan["prompts"]
        #     goals = plan["goals"]
        #     self.task_routines[key] = PlanningRoutine(key, prompts, goals)

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        self.context = Context(input)

        # load prefix/postfix for prompt and setup memory
        prefix = self.context.get('model.model_config.prefix')
        postfix = prefix = self.context.get('model.model_config.postfix')
        self.context.memory = Memory(prefix, postfix)

        # add task routines to context
        self.context.task_routines = self.task_routines #add to context for reference in routines

        try:
            state_machine = StateMachine(self.routine.subroutines, self.task_routines)
            if not self.context.get('model.model_config.streaming'):
                return state_machine.run(self.context)
            else:
                threading.Thread(target=state_machine.run, args=(self.context,)).start()
        except Exception as e:
            logger.info(f"Error starting thread: {str(e)}")
        return True
    
    def abort(self):
        self.context.abort()
        return True