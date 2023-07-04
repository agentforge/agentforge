# TODO: Implement default decision --> decisions are markov chains w/ subroutines as nodes
### i.e. the simplest example: generate text response -> generate wav file -> generate mp4 -> return
from typing import Dict, Any, List, Protocol, Optional
from agentforge.ai.subroutines.respond import Respond
from agentforge.ai.subroutines.parse import Parse
from agentforge.ai.subroutines.speak import Speak
from agentforge.ai.subroutines.lipsync import Lipsync
from agentforge.ai.subroutines.remember import Remember
from agentforge.ai.subroutines.recall import Recall
from agentforge.ai.routines.routine import Routine
from agentforge.ai.subroutines.prep import Prep
from agentforge.ai.subroutines.plan import Plan, EnsurePlan
from agentforge.ai.subroutines.intent import Intent
from agentforge.ai.subroutines.query import Query, Learn

### Simplest reactive routine for a decision timestep/run
class ReactiveRoutine(Routine):
    def __init__(self):
        super().__init__("reactive")
        self.subroutines = [Recall(), Parse(), Intent(), Prep()] #, Respond(), Remember(), Speak(), Lipsync(), Prep()]

### FLOWS: These routines have descriptions and thus can be referenced for our guardrails system
### i.e. if user query is similar to this desciption we will ask the user if they want to engage in this routine
### for instance when we are generating user intent
### Simplest planning routine for a decision timestep/run
class PlanningRoutine(Routine):
    def __init__(self):
        super().__init__("plan", "plan blueprint scheme design program project strategy outline agenda layout plot map proposal arrangement schedule idea intention method approach tactic system procedure roadmap model planning sketch diagram configuration setup matrix itinerary script conception prototype gameplan format concept formula archetype procedure draft framework initiative masterplan action plan organize orchestration procedure representation game plan protocol recipe structure course schedule template measure contrivance course of action line of action enterprise scenario delineation figure graph preparation drawing table chart illustration schematization action tactics machination stratagem process methodology modus operandi path steps progression prescription policy line maneuver chronicle timeline series composition vector plotline canvas form profile silhouette contour cast mould shape composition ground plan composition set-up guide flowchart platform recipe course plotting routemap line attack projection pattern measure apparatus theory proposition")
        self.subroutines = [Learn(), Plan(), Query()]
