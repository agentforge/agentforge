import os
from agentforge.ai import SimpleDecision, Decision

### Delivers decision logic to the agent
class DecisionFactory:
    def __init__(self) -> None:
      self.__interface = None

    def create_decision(self) -> None:
        decision_type = os.getenv("DECISION_TYPE")
        # Instantiate the correct LLM resource based on llm_type
        if decision_type == "simple":
            self.__interface = SimpleDecision()
            return self.__interface
        else:
            raise ValueError(f"Invalid Decision type: {decision_type}")

    def get_decision(self) -> Decision:
        if self.__interface is not None:
            return self.__interface
        else:
            raise Exception(f"Decision does not exist")
