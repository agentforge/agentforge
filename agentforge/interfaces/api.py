import os
from agentforge.adapters import APIService

### TODO: Create mock test fixtures for each service and return when config is set to test
class LLMService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('LLM_URL')
    self.service = "llm"

  def test(self):
    return {
      "choices": [
        { "text": "This is a test response from LLM" }
      ]
    }

class TTSService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('TTS_URL')
    self.service = "tts"

class W2LService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('W2L_URL')
    self.service = "w2l"

class VQAService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('VQA_URL')
    self.service = "vqa"