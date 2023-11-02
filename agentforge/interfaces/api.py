import redis
import os
from agentforge.adapters import APIService
from agentforge.interfaces.vllm_client import post_http_request, get_streaming_response, clear_line, get_response
from agentforge.utils import logger
from agentforge.config import RedisConfig
from fastapi import HTTPException
from typing import Dict, Any

class vLLMService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('LLM_URL')
    self.service = "llm"
    self.redis_config = RedisConfig.from_env()

  def call(self, form_data):
    print(form_data)
    stream = form_data['model_config']['streaming']
    if 'user_id' in form_data:
      user_id = form_data['user_id']
    else:
      user_id = None
    if 'stopping_criteria_string' in form_data['generation_config']:
      stop = form_data['generation_config']['stopping_criteria_string'].split(",")
    else:
      stop = []
    if user_id is not None and stream:
      redis_server = redis.StrictRedis(host=self.redis_config.host, port=self.redis_config.port, db=self.redis_config.db)
    response = post_http_request(
      self.url,
      form_data['prompt'],
      form_data['generation_config']['max_new_tokens'],
      form_data['generation_config']['temperature'],
      form_data['generation_config']['repetition_penalty'],
      form_data['generation_config']['top_p'],
      form_data['generation_config']['top_k'],
      stop, # stopping strings
      form_data['model_config']['streaming']
    )

    num_printed_lines = 0
    cur_seen = form_data['prompt']
    output = ""
    if stream:
      for h in get_streaming_response(response):
        num_printed_lines = 0
        for i, line in enumerate(h):
            num_printed_lines += 1
            # print(line)
            new_tokens = line.replace(cur_seen, "")
            output += new_tokens
            if user_id is not None:
              redis_server.publish(f"streaming-{user_id}", new_tokens)
            cur_seen = line
            # print(f"Beam candidate {i}: {line!r}", flush=True)

    else:
      output = get_response(response)
      output = output[0].replace(form_data['prompt'], "")

    if user_id is not None and stream:
      redis_server.publish(f"streaming-{user_id}", '<|endoftext|>')
      redis_server.close()
    return {'choices': [{'text': output}]} #OAI output format

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

    def process(self, img_bytes: bytes, prompt: str) -> Dict[str, Any]:
        form_data = {
            'img': ('image.jpg', img_bytes, 'image/jpeg'),
            'prompt': prompt
        }

        try:
            response_data = self.call(form_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return response_data