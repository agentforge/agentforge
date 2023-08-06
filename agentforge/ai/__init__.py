from .cognition.memory import Memory
from .subroutines.respond import Respond
from .subroutines.emote import Emote
from .subroutines.lipsync import Lipsync
from .subroutines.base import Subroutine
from .subroutines.parse import Parse
from .subroutines.remember import Remember
from .subroutines.recall import Recall
from .subroutines.speak import Speak
from .agents.agent import Agent
from .agents.simple import SimpleAgent

from agentforge.ai.agents.agent_factory import AgentFactory

agent_interactor = AgentFactory()

agent_interactor.create_agent()

__all__ = ["Memory", "ShortTermMemory", "LongTermMemory",
           "startup", "Subroutine", "Respond", "Agent",
           "Emote", "Lipsync", "Remember", "Parse", "Recall",
           "SimpleAgent", "Speak", "agent_interactor"]
