from typing import Any, Dict

### Identify user intent
class Intent:
    def __init__(self, service):
        self.service = service

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
      pass # TODO: do a vector search on all the canonical form examples included in the guardrails configuration, #
      #take the top 5 and include them in a prompt, and ask the LLM to generate the canonical form for the current user utterance.
