
### Initialize the factories. All methods should inherit their factories
### from here.  This is to ensure that all interfaces are created in the
### same way and that the factories are not instantiated multiple times.

# from agentforge.interfaces.interface_factory import InterfaceFactory
# from agentforge.ai.agents.agent_factory import AgentFactory
from agentforge.factories.resource_factory import ResourceFactory
import os, importlib

DEFAULT_LLM = os.environ.get("DEFAULT_LLM")
RESOURCE = os.environ.get("RESOURCE")

resource_factory = ResourceFactory()
if RESOURCE == "LLM":
    resource_factory.create_llm_resource({})
if RESOURCE == "TTS":
    resource_factory.create_tts_resource()
if RESOURCE == "W2L":
    resource_factory.create_w2l_resource()
if RESOURCE == "VQA":
    resource_factory.create_vqa_resource({})