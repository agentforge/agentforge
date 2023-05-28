
### Initialize the factories. All methods should inherit their factories
### from here.  This is to ensure that all interfaces are created in the
### same way and that the factories are not instantiated multiple times.

from agentforge.factories.interface_factory import InterfaceFactory
from agentforge.factories.decision_factory import DecisionFactory

interface_factory = InterfaceFactory()
decision_factory = DecisionFactory()

interface_factory.create_kvstore()
interface_factory.create_filestore()
interface_factory.create_embeddings()
interface_factory.create_vectorstore()
