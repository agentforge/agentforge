import os
from agentforge.ai.agents.agent import Agent
from agentforge.ai.agents.simple import SimpleAgent

### Create the Agent
class AgentFactory:
    def __init__(self) -> None:
      self.__interface = None

    def create_agent(self) -> None:
        agent_type = os.getenv("AGENT_TYPE")
        # Instantiate the correct LLM resource based on llm_type
        if agent_type == "simple":
            self.__interface = SimpleAgent()
            return self.__interface
        else:
            raise ValueError(f"Invalid Agent type: {agent_type}")

    def get_agent(self) -> Agent:
        if self.__interface is not None:
            return self.__interface
        else:
            raise Exception(f"Agent does not exist")
