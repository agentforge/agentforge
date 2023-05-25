import os
from typing import Any
from resources import LLMResource, TTSResource, STTResource

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

    def create_stt_resource(self) -> None:
        stt_type = os.getenv("W2L_TYPE")
        # Instantiate the correct STT resource based on stt_type
        if stt_type == "w2l":
            self.__resources["stt"] = Wav2Lip()
        elif stt_type == "type2":
            self.__resources["stt"] = STTResourceType2()
        else:
            raise ValueError(f"Invalid STT type: {stt_type}")

    def get_resource(self, resource_name: str) -> Any:
        if resource_name in self.__resources:
            return self.__resources[resource_name]
        else:
            raise Exception(f"Resource {resource_name} does not exist")
