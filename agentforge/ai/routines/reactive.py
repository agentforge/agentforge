from agentforge.ai.subroutines.respond import Respond
from agentforge.ai.subroutines.parse import Parse
from agentforge.ai.subroutines.speak import Speak
from agentforge.ai.subroutines.lipsync import Lipsync
from agentforge.ai.subroutines.remember import Remember
from agentforge.ai.subroutines.recall import Recall
from agentforge.ai.routines.routine import Routine
from agentforge.ai.subroutines.prep import Prep
from agentforge.ai.subroutines.intent import Intent
from agentforge.ai.agents.statemachine import Node

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
