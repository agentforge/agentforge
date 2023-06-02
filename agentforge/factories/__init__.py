
### Initialize the factories. All methods should inherit their factories
### from here.  This is to ensure that all interfaces are created in the
### same way and that the factories are not instantiated multiple times.

# from agentforge.interfaces.interface_factory import InterfaceFactory
# from agentforge.ai.decisions.decision_factory import DecisionFactory
from agentforge.factories.resource_factory import ResourceFactory

# interface_interactor = InterfaceFactory()
# descision_interactor = DecisionFactory()

# interface_interactor.create_kvstore()
# interface_interactor.create_filestore()
# interface_interactor.create_embeddings()
# interface_interactor.create_vectorstore()

# interface_interactor.create_service("llm")
# interface_interactor.create_service("tts")
# interface_interactor.create_service("w2l")

# descision_interactor.create_decision()
resource_factory = ResourceFactory()
resource_factory.create_llm_resource()
resource_factory.create_tts_resource()
resource_factory.create_w2l_resource()