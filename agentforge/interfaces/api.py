import redis
import os
from agentforge.adapters import APIService
from agentforge.interfaces.vllm_client import post_http_request, get_streaming_response, clear_line, get_response
from agentforge.utils import logger
from agentforge.config import RedisConfig

class vLLMService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('LLM_URL')
    self.service = "llm"
    self.redis_config = RedisConfig.from_env()

  def call(self, form_data):
    self.user_id = user_id = form_data['user_id']
    self.redis_server = redis.StrictRedis(host=self.redis_config.host, port=self.redis_config.port, db=self.redis_config.db)
    response = post_http_request(
      self.url,
      form_data['prompt'],
      form_data['generation_config']['max_new_tokens'],
      form_data['generation_config']['temperature'],
      form_data['generation_config']['repetition_penalty'],
      form_data['generation_config']['top_p'],
      form_data['generation_config']['top_k'],
      [], # stopping strings
      form_data['model_config']['streaming']
    )

    num_printed_lines = 0
    cur_seen = form_data['prompt']
    output = ""
    if form_data['model_config']['streaming']:
      for h in get_streaming_response(response):
        clear_line(num_printed_lines)
        num_printed_lines = 0
        for i, line in enumerate(h):
            num_printed_lines += 1
            # print(line)
            new_tokens = line.replace(cur_seen, "")
            output += new_tokens
            self.redis_server.publish(f"streaming-{self.user_id}", new_tokens)
            cur_seen = line
            print(f"Beam candidate {i}: {line!r}", flush=True)

    else:
      output = get_response(response)
      for i, line in enumerate(output):
          print(f"Beam candidate {i}: {line!r}", flush=True)

    self.redis_server.publish(f"streaming-{self.user_id}", '<|endoftext|>')
    self.redis_server.close()
    return {'text': [output]}

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