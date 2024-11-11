import redis
import os
import json
from agentforge.adapters import APIService
from agentforge.interfaces.vllm_client import get_streaming_response, create_completion, get_completion_text
from typing import Optional
from agentforge.utils import logger
from agentforge.config import RedisConfig
from fastapi import HTTPException
from typing import Dict, Any
from collections import deque

class vLLMService(APIService):
  def __init__(self):
      super().__init__()
      self.url = os.getenv('LLM_URL', 'http://localhost:8000/v1/completions')
      self.service = "llm"
      self.redis_config = RedisConfig.from_env()

  def prepare_stop_sequences(self, form_data: Dict[str, Any]) -> list:
      """Prepare stop sequences from form data"""
      base_stops = ['<|eot_id|>']

      if 'generation_config' in form_data and 'stopping_criteria_string' in form_data['generation_config']:
          return form_data['generation_config']['stopping_criteria_string'].split(",") + base_stops
      return base_stops

  def handle_streaming(self, response: Any, user_id: str, user_name: str, 
                      agent_name: str, prompt: str, redis_server: Optional[redis.Redis] = None) -> str:
      """Handle streaming response from VLLM"""
      buffer = deque(maxlen=5)
      output = ""
      cur_seen = str(prompt)
      
      for chunk in response.iter_lines(decode_unicode=True):
          if not chunk or chunk == 'data: [DONE]':
              continue
              
          if chunk.startswith('data: '):
              chunk = chunk[6:]  # Remove 'data: ' prefix
          
          try:
              data = json.loads(chunk)
              new_text = data['choices'][0]['text']
              
              # Process new tokens
              new_tokens = new_text.replace(cur_seen, "").replace(prompt, "")
              buffer.extend(new_tokens)
              
              # Check for stop conditions
              buffer_text = ' '.join(buffer)
              if (buffer_text.endswith('/n ' + user_name) or 
                  new_tokens + agent_name == output or 
                  new_tokens + user_name == output):
                  break
              
              output += new_tokens
              cur_seen = new_text
              
              # Stream to Redis if enabled
              if redis_server and new_tokens:
                  redis_server.publish(f"streaming-{user_id}", new_tokens)
                  
          except json.JSONDecodeError:
              logger.error(f"Failed to decode chunk: {chunk}")
              continue
              
      return output.strip()

  def prepare_completion_params(self, form_data: Dict[str, Any], stream: bool) -> Dict[str, Any]:
      """Prepare complete set of completion parameters"""
      gen_config = form_data.get('generation_config', {})
      model_config = form_data.get('model_config', {})

      # Base parameters (required)
      params = {
          "api_url": self.url,
          "model": model_config.get('model_name', "default_model"),
          "prompt": form_data['prompt'],
          "stream": stream,
          "stop": self.prepare_stop_sequences(form_data),
      }

      # Standard OpenAI parameters
      openai_params = {
          "max_tokens": gen_config.get('max_tokens', 16),
          "temperature": gen_config.get('temperature', 0.7),
          "top_p": gen_config.get('top_p', 1.0),
          "n": gen_config.get('n', 1),
          "presence_penalty": gen_config.get('presence_penalty', 0.0),
          "frequency_penalty": gen_config.get('frequency_penalty', 0.0),
          "logit_bias": gen_config.get('logit_bias'),
          "user": gen_config.get('user'),
          "seed": gen_config.get('seed'),
      }
      params.update({k: v for k, v in openai_params.items() if v is not None})

      # VLLM-specific parameters
      vllm_params = {
          "use_beam_search": gen_config.get('use_beam_search', False),
          "top_k": gen_config.get('top_k', -1),
          "min_p": gen_config.get('min_p', 0.0),
          "repetition_penalty": gen_config.get('repetition_penalty', 1.0),
          "length_penalty": gen_config.get('length_penalty', 1.0),
          "stop_token_ids": gen_config.get('stop_token_ids'),
          "include_stop_str_in_output": gen_config.get('include_stop_str_in_output', False),
          "ignore_eos": gen_config.get('ignore_eos', False),
          "min_tokens": gen_config.get('min_tokens', 0),
          "skip_special_tokens": gen_config.get('skip_special_tokens', True),
          "spaces_between_special_tokens": gen_config.get('spaces_between_special_tokens', True),
          "truncate_prompt_tokens": gen_config.get('truncate_prompt_tokens'),
          "allowed_token_ids": gen_config.get('allowed_token_ids'),
          "prompt_logprobs": gen_config.get('prompt_logprobs'),
      }
      params.update({k: v for k, v in vllm_params.items() if v is not None})

      # Guided decoding parameters
      guided_params = {
          "guided_json": gen_config.get('guided_json') or form_data.get('schema'),
          "guided_regex": gen_config.get('guided_regex'),
          "guided_choice": gen_config.get('guided_choice'),
          "guided_grammar": gen_config.get('guided_grammar'),
          "guided_decoding_backend": gen_config.get('guided_decoding_backend'),
          "guided_whitespace_pattern": gen_config.get('guided_whitespace_pattern'),
      }
      params.update({k: v for k, v in guided_params.items() if v is not None})

      return params

  def call(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
      """Process request and return response in OpenAI format"""      
      stream = form_data.get('model_config', {}).get('streaming', False)
      user_id = form_data.get('user_id')
      
      # Initialize Redis for streaming if needed
      redis_server = None
      if user_id and stream:
          redis_server = redis.StrictRedis(
              host=self.redis_config.host,
              port=self.redis_config.port,
              db=self.redis_config.db
          )

      try:
          # Prepare complete set of parameters
          completion_params = self.prepare_completion_params(form_data, stream)

          logger.info(f"completion_params: {completion_params}\n")
          
          # Make request to VLLM
          response = create_completion(**completion_params)
          
          if stream:
              output = self.handle_streaming(
                  response,
                  user_id,
                  form_data.get('user_name', ''),
                  form_data.get('agent_name', ''),
                  form_data['prompt'],
                  redis_server
              )
          else:
              output = get_completion_text(response)
            #   output = output.replace(form_data['prompt'], "")

          # Clean up Redis connection
          if redis_server:
              redis_server.publish(f"streaming-{user_id}", '<|endoftext|>')
              redis_server.close()

          logger.info(f"Response from vLLM: {output}")
          
          return output
          
      except Exception as e:
          logger.error(f"Error in vLLM service: {str(e)}")
          raise

class PixArtService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('PIXART_URL')
    self.service = "pixart"

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

class TokenizerService(APIService):
  def __init__(self):
    super().__init__()
    self.url = os.getenv('TOKENIZER_URL')
    self.service = "tokenizer"

class VQAService(APIService):
    def __init__(self):
        super().__init__()
        self.url = os.getenv('VQA_URL')
        self.service = "vqa"

    def process(self,  prompt: str, img_bytes: bytes) -> Dict[str, Any]:
        form_data = {
            'img': img_bytes,
            'prompt': prompt
        }

        try:
            response_data = self.call(form_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return response_data