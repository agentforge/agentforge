from typing import Dict, Any
from agentforge.ai.routines.reactive import ReactiveRoutine
from agentforge.ai.routines.planning import PlanningRoutine
from agentforge.ai.beliefs.memory import Memory
from agentforge.ai.agents.statemachine import StateMachine
from agentforge.ai.agents.context import Context
from agentforge.ai.reasoning.query_engine import QueryEngine

import threading

class SimpleAgent:
    def __init__(self):
        ### Primary Reactive Routine - handles user input
        self.routine = ReactiveRoutine()

        ### Demo Task Routines - gardening plan
        garden_prompts = [
            "Plan a garden for me.",
            "Could you help me design a garden?",
            "I need assistance in planning my garden.",
            "Can you help me with garden planning?",
            "Let's plan my garden.",
            "Assist me in designing a garden.",
            "I'd like your help to plan a garden.",
            "Could you assist me in garden planning?",
            "Help me come up with a garden plan.",
            "I need help in designing my garden.",
            "Can you aid me in planning my garden?",
            "Help me design a garden.",
            "Support me in planning a garden.",
            "Let's work together to plan my garden.",
            "Guide me in planning my garden.",
            "Can we plan my garden together?",
            "I'd like to plan a garden with your help.",
            "Help me with the garden planning process.",
            "Can you support me in designing a garden?",
            "I'd like assistance with garden planning.",
            "Could we plan a garden together?",
            "Aid me in planning my garden.",
            "Let's design a garden.",
            "Could you guide me in planning a garden?",
            "I need your assistance to plan a garden.",
            "Let's develop a plan for my garden.",
            "Can you help me create a garden plan?",
            "I require your assistance in garden planning.",
            "Could you help me devise a plan for my garden?",
            "Support me in designing my garden.",
            "Can you guide me in designing a garden?",
            "Help me formulate a plan for my garden.",
            "I'd like you to help me plan my garden.",
            "Can you assist me in creating a garden plan?",
            "I need your help to design my garden.",
            "Could you support me in planning a garden?",
            "I want your assistance to plan a garden.",
            "Can we design my garden together?",
            "Help me draft a plan for my garden.",
            "Let's devise a plan for my garden.",
            "Could you aid me in designing a garden?",
            "I need you to assist me in garden planning.",
            "Can you help me draft a garden plan?",
            "Let's collaborate on planning my garden.",
            "I want you to help me plan a garden.",
            "Can you help me formulate a garden plan?",
            "Support me in the process of garden planning.",
            "Let's come up with a plan for my garden.",
            "I'd like your support in planning my garden."
        ]
        # Goals are the end point of each possible state of the plan
        garden_goals = [
            "growing ?plant",
            "harvest ?plant",
        ]
        self.task_routines = {"garden": PlanningRoutine("garden", garden_prompts, garden_goals)}

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        self.context = Context(input)
        self.context.memory =  Memory()
        self.context.task_routines = self.task_routines #add to context for reference in routines

        state_machine = StateMachine(self.routine.subroutines, self.task_routines)
        threading.Thread(target=state_machine.run, args=(self.context,)).start()
        return True
    
    def abort(self):
        self.context.abort()
        return True