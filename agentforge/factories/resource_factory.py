import os
from typing import Any
from agentforge.interfaces import LocalLLM, TextToSpeech, BarkTextToSpeech, Wav2LipModel

### ResourceFactory brings together the resources and adapters
### to provide access to either local GPU containers or remote
class ResourceFactory:
    def __init__(self) -> None:
        self.__resources: dict[str, Any] = {}

    def create_llm_resource(self) -> None:
        llm_type = os.getenv("LLM_TYPE")
        # Instantiate the correct LLM resource based on llm_type
        if llm_type == "local":
            self.__resources["llm"] = LocalLLM()
        else:
            raise ValueError(f"Invalid LLM type: {llm_type}")

    def create_tts_resource(self) -> None:
        tts_type = os.getenv("TTS_TYPE")
        # Instantiate the correct TTS resource based on tts_type
        if tts_type == "tts":
            self.__resources["tts"] = TextToSpeech()
        elif tts_type == "bark":
            self.__resources["tts"] = BarkTextToSpeech()
        else:
            raise ValueError(f"Invalid TTS type: {tts_type}")

    def create_w2l_resource(self) -> None:
        w2l_type = os.getenv("W2L_TYPE")
        # Instantiate the correct w2l resource based on w2l_type
        if w2l_type == "w2l":
            self.__resources["w2l"] = Wav2LipModel()
        elif w2l_type == "sadtalker":
            raise NotImplementedError("SADTalker is not yet implemented")
        else:
            raise ValueError(f"Invalid W2L type: {w2l_type}")

    def get_resource(self, resource_name: str) -> Any:
        if resource_name in self.__resources:
            return self.__resources[resource_name]
        else:
            raise Exception(f"Resource {resource_name} does not exist")
