"""Response handler for game engine with complete OpenAI and VLLM parameter support"""
from typing import Any, Dict, Optional, Union
from agentforge.interfaces import interface_interactor
from agentforge.utils import Parser, logger
from copy import deepcopy


class GenerationConfig:
    """
    Complete set of generation parameters combining OpenAI and VLLM options
    """
    def __init__(self, config: Dict[str, Any]):
        # Standard OpenAI parameters
        self.max_tokens: int = config.get('max_tokens', 16)
        self.temperature: float = config.get('temperature', 1.0)
        self.top_p: float = config.get('top_p', 1.0)
        self.n: int = config.get('n', 1)
        self.stream: bool = config.get('stream', False)
        self.stop: Optional[Union[str, list]] = config.get('stop', None)
        self.presence_penalty: float = config.get('presence_penalty', 0.0)
        self.frequency_penalty: float = config.get('frequency_penalty', 0.0)
        self.logit_bias: Optional[Dict[str, float]] = config.get('logit_bias', None)
        self.user: Optional[str] = config.get('user', None)
        self.seed: Optional[int] = config.get('seed', None)
        
        # VLLM-specific parameters
        self.use_beam_search: bool = config.get('use_beam_search', False)
        self.top_k: int = config.get('top_k', -1)
        self.min_p: float = config.get('min_p', 0.0)
        self.repetition_penalty: float = config.get('repetition_penalty', 1.0)
        self.length_penalty: float = config.get('length_penalty', 1.0)
        self.stop_token_ids: Optional[list] = config.get('stop_token_ids', None)
        self.include_stop_str_in_output: bool = config.get('include_stop_str_in_output', False)
        self.ignore_eos: bool = config.get('ignore_eos', False)
        self.min_tokens: int = config.get('min_tokens', 0)
        self.skip_special_tokens: bool = config.get('skip_special_tokens', True)
        self.spaces_between_special_tokens: bool = config.get('spaces_between_special_tokens', True)
        self.truncate_prompt_tokens: Optional[int] = config.get('truncate_prompt_tokens', None)
        self.allowed_token_ids: Optional[list] = config.get('allowed_token_ids', None)
        self.prompt_logprobs: Optional[int] = config.get('prompt_logprobs', None)
        
        # VLLM guided decoding parameters
        self.guided_json: Optional[Union[str, dict]] = config.get('guided_json', None)
        self.guided_regex: Optional[str] = config.get('guided_regex', None)
        self.guided_choice: Optional[list] = config.get('guided_choice', None)
        self.guided_grammar: Optional[str] = config.get('guided_grammar', None)
        self.guided_decoding_backend: Optional[str] = config.get('guided_decoding_backend', None)
        self.guided_whitespace_pattern: Optional[str] = config.get('guided_whitespace_pattern', None)
        
        # Game-specific parameters
        self.stopping_criteria_string: Optional[str] = config.get('stopping_criteria_string', None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary, excluding None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class Respond:
    def __init__(self):
        self.service = interface_interactor.get_interface("llm")
        self.parser = Parser()

    def clean_special_tokens(self, text: str, context: Dict[str, Any]) -> str:
        """Remove special tokens from text"""
        special_tokens = ['eos_token', 'bos_token', 'prefix', 'postfix']
        for tok in special_tokens:
            token_path = f"model.model_config.{tok}"
            if context.has_key(token_path):
                text = text.replace(context.get(token_path), "")
        return text

    def prepare_request(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the complete request with all parameters"""
        # Get user and model names
        # username = context.get("input.user_name") + ":"
        # agentname = context.get("model.persona.display_name") + ":"
        
        # Get base generation config and add stop sequence
        gen_config = deepcopy(context.get('model.generation_config', {}))
        # gen_config["stopping_criteria_string"] = f"{username},{agentname}"
        
        # Create complete generation config
        generation_config = GenerationConfig(gen_config)
        
        # Get model config
        model_config = context.get('model.model_config', {})
        model_name = model_config.get('model_name', 'default_model')
        
        # Prepare formatted prompt
        formatted = context.get_formatted()
        formatted = self.clean_special_tokens(formatted, context)
        
        # Construct complete request
        request = {
            "model": model_name,
            "prompt": formatted,
            "generation_config": generation_config.to_dict(),
            "model_config": model_config,
            "user_id": context.get("input.user_id"),
            "user_name": context.get("input.user_name"),
            "agent_name": context.get("model.persona.display_name"),
        }
        
        # Add any additional configurations
        if context.has_key("model.response_format"):
            request["response_format"] = context.get("model.response_format")
            
        return request

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Skip if response already exists
        if context.has_key("response"):
            logger.info("Response already exists, skipping response generation")
            return context

        try:
            # Prepare complete request with all parameters
            request = self.prepare_request(context)
            
            # Make request to VLLM service
            response = self.service.call(request)

            # Process response
            if response and "choices" in response:
                text = response["choices"][0]["text"]
                
                # Clean and parse response
                text = text.replace(request["prompt"], "")
                text = self.parser.parse_llm_response(text)
                text = self.clean_special_tokens(text, context)
                
                context.set("response", text)
                
            return context
            
        except Exception as e:
            logger.error(f"Error in response generation: {str(e)}")
            raise