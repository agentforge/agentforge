from agentforge.ai.communication.respond import Respond
from agentforge.ai.observation.parse import Parse
from agentforge.ai.communication.speak import Speak
from agentforge.ai.communication.lipsync import Lipsync
from agentforge.ai.beliefs.remember import Remember
from agentforge.ai.beliefs.recall import Recall
from agentforge.ai.routines.routine import Routine
from agentforge.ai.communication.prep import Prep
from agentforge.ai.attention.intent import Intent
from agentforge.ai.observation.image_processor import ImageProcessor
from agentforge.ai.agents.statemachine import Node
from agentforge.ai.reasoning.summarization import Summarizer

class ReactiveRoutine(Routine):
    def __init__(self):
        super().__init__("reactive", [])
        parse = Node(Parse().execute, [])
        recall = Node(Recall().execute, [parse])
        intent = Node(Intent().execute, [parse])
        summarizer = Node(Summarizer().execute, [parse])
        image_processor = Node(ImageProcessor().execute, [parse])
        speak = Node(Speak().execute, [recall, parse, intent, image_processor])
        respond = Node(Respond().execute, [recall, parse, intent, image_processor, summarizer])
        remember = Node(Remember().execute, [speak, respond])
        self.subroutines = [
            parse,
            recall,
            intent,
            summarizer,
            image_processor,
            respond,
            speak,
            remember,
            Node(Prep().execute, [remember]),
        ]
