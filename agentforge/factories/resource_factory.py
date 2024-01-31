import os
from typing import Any
import importlib

### ResourceFactory brings together the resources and adapters
### to provide access to either local GPU containers or remote
class ResourceFactory:
    def __init__(self) -> None:
        self.__resources: dict[str, Any] = {}

    def create_pixart_resource(self, config: dict = {}) -> None:
        # Instantiate the correct LLM resource based on llm_type
        pixart = getattr(importlib.import_module('agentforge.interfaces.pixart.resource'), 'PixArtResource')
        self.__resources["image_gen"] = pixart(config)

    def create_llm_resource(self, config: dict = {}) -> None:
        llm_type = os.getenv("LLM_TYPE")
        # Instantiate the correct LLM resource based on llm_type
        if llm_type == "local":
            LocalLLM = getattr(importlib.import_module('agentforge.interfaces.localllm.resource'), 'LocalLLM')
            self.__resources["llm"] = LocalLLM(config)
        if llm_type == "vllm":
            vllm = getattr(importlib.import_module('agentforge.interfaces.vllm.resource'), 'vLLMResource')
            self.__resources["llm"] = vllm(config)
        else:
            raise ValueError(f"Invalid LLM type: {llm_type}")

    def create_tts_resource(self) -> None:
        tts_type = os.getenv("TTS_TYPE")
        # Instantiate the correct TTS resource based on tts_type
        if tts_type == "tts":
            TextToSpeech = getattr(importlib.import_module('agentforge.interfaces.tts.resource'), 'TextToSpeech')
            self.__resources["tts"] = TextToSpeech()
        elif tts_type == "bark":
            BarkTextToSpeech = getattr(importlib.import_module('agentforge.interfaces.barktts.resource'), 'BarkTextToSpeech')
            self.__resources["tts"] = BarkTextToSpeech()
        else:
            raise ValueError(f"Invalid TTS type: {tts_type}")

    def create_w2l_resource(self) -> None:
        w2l_type = os.getenv("W2L_TYPE")
        # Instantiate the correct w2l resource based on w2l_type
        if w2l_type == "w2l":
            Wav2LipModel = getattr(importlib.import_module('agentforge.interfaces.wav2lip.resource'), 'Wav2LipModel')
            self.__resources["w2l"] = Wav2LipModel()
        elif w2l_type == "sadtalker":
            SadTalker = getattr(importlib.import_module('agentforge.interfaces.sadtalker.resource'), 'SadTalker')
            self.__resources["w2l"] = SadTalker()

        else:
            raise ValueError(f"Invalid W2L type: {w2l_type}")

    def create_vqa_resource(self) -> None:
        vqa_type = os.getenv("VQA_TYPE")
        # Instantiate the correct VQA resource based on vqa_type
        if vqa_type == "vqa":
            LocalVQA = getattr(importlib.import_module('agentforge.interfaces.vqa.resource'), 'LocalVQA')
            self.__resources["vqa"] = LocalVQA()
        else:
            raise ValueError(f"Invalid VQA type: {vqa_type}")

    def get_resource(self, resource_name: str) -> Any:
        if resource_name in self.__resources:
            return self.__resources[resource_name]
        else:
            raise Exception(f"Resource {resource_name} does not exist")
