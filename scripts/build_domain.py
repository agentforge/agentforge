from agentforge.interfaces import interface_interactor
from agentforge.ai.planning.planner import DomainBuilder

db = interface_interactor.get_interface("db")
d = DomainBuilder(db)
d.upload_documents_from_folder('garden', '/app/agentforge/agentforge/config/configs/planner/domains/garden', 'p_example')
print("Done!")