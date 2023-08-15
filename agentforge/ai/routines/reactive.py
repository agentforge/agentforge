from agentforge.ai.communication.respond import Respond
from agentforge.ai.observation.parse import Parse
from agentforge.ai.reasoning.query import AskQuery
from agentforge.ai.communication.speak import Speak
from agentforge.ai.communication.lipsync import Lipsync
from agentforge.ai.beliefs.remember import Remember
from agentforge.ai.beliefs.recall import Recall
from agentforge.ai.routines.routine import Routine
from agentforge.ai.communication.prep import Prep
from agentforge.ai.attention.intent import Intent
from agentforge.ai.agents.statemachine import Node

class ReactiveRoutine(Routine):
    def __init__(self):
        super().__init__("reactive")
        recall = Node(Recall().execute, [])
        parse = Node(Parse().execute, [recall])
        intent = Node(Intent().execute, [parse])
        # query = Node(AskQuery().execute, [parse, intent])
        speak = Node(Speak().execute, [parse, intent])
        respond = Node(Respond().execute, [parse, intent])
        remember = Node(Remember().execute, [speak, respond])
        self.subroutines = [
            parse,
            recall,
            intent,
            # query,
            respond,
            speak,
            remember,
            Node(Prep().execute, [remember]),
        ]
