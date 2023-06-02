
### Initialize the factories. All methods should inherit their factories
### from here.  This is to ensure that all interfaces are created in the
### same way and that the factories are not instantiated multiple times.

# from agentforge.interfaces.interface_factory import InterfaceFactory
# from agentforge.ai.decisions.decision_factory import DecisionFactory
from agentforge.factories.resource_factory import ResourceFactory
from agentforge.interfaces.model_profile import ModelProfile
import os

model_profile = ModelProfile()
DEFAULT_LLM = os.environ.get("DEFAULT_LLM")
print(DEFAULT_LLM)
model_configuration = model_profile.get_profile_by_name(DEFAULT_LLM)

resource_factory = ResourceFactory()
resource_factory.create_llm_resource(model_configuration)
# resource_factory.create_tts_resource()
# resource_factory.create_w2l_resource()