from typing import Dict, Any
from .reactive import ReactiveRoutine
from agentforge.ai import Routine

class SimpleDecision:
    def decide(self, context: Dict[str, Any], config: Dict[str, Any], user_id: str) -> Routine:
        # Use the context, config, and user_id to decide on a routine
        routine = ReactiveRoutine([LLM(), TTS(), W2L()])
        return routine