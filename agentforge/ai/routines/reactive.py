# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
import threading
from typing import Dict, Any, List, Protocol, Optional, Callable
from agentforge.ai.subroutines.respond import Respond
from agentforge.ai.subroutines.parse import Parse
from agentforge.ai.subroutines.speak import Speak
from agentforge.ai.subroutines.lipsync import Lipsync
from agentforge.ai.subroutines.remember import Remember
from agentforge.ai.subroutines.recall import Recall
from agentforge.ai.routines.routine import Routine
from agentforge.ai.subroutines.prep import Prep
from agentforge.ai.subroutines.plan import Plan
from agentforge.ai.subroutines.intent import Intent
from agentforge.ai.subroutines.query import Query, Learn
from agentforge.ai.decisions.statemachine import Node

class ReactiveRoutine(Routine):
    def __init__(self):
        super().__init__("reactive")
        recall = Node(Recall().execute, [])
        parse = Node(Parse().execute, [recall])
        intent = Node(Intent().execute, [parse])
        speak = Node(Speak().execute, [parse, intent])
        respond = Node(Respond().execute, [parse, intent])
        remember = Node(Remember().execute, [speak, respond])
        self.subroutines = [
            parse,
            recall,
            intent,
            respond,
            speak,
            remember,
            Node(Lipsync().execute, [remember]),
            Node(Prep().execute, [remember]),
        ]
    
### FLOWS: These routines have descriptions and thus can be referenced for our guardrails system
### i.e. if user query is similar to this desciption we will ask the user if they want to engage in this routine
### for instance when we are generating user intent
### Simplest planning routine for a decision timestep/run
class PlanningRoutine(Routine):
    def __init__(self):
        plan_prompts = [
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
        super().__init__("plan", plan_prompts)
        self.subroutines = [
            Node(Plan().execute, []),
            Node(Speak().execute, [])
        ]
