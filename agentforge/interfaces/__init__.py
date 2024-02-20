import os
from agentforge.interfaces.interface_factory import InterfaceFactory

RESOURCE = os.environ.get('RESOURCE')

if RESOURCE == "AGENT":
    interface_interactor = InterfaceFactory()
    interface_interactor.create_db()
    interface_interactor.create_kvstore()
    interface_interactor.create_filestore()
    interface_interactor.create_vectorstore()
    interface_interactor.create_working_memory()
    interface_interactor.create_keygenerator() # requires kvstore
    # interface_interactor.create_service("llm")
    interface_interactor.create_service("vllm")
    interface_interactor.create_service("tts")
    interface_interactor.create_service("w2l")
    interface_interactor.create_service("tokenizer")
    interface_interactor.create_image_generator("pixart")
