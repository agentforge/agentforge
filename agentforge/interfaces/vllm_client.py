"""Comprehensive HTTP client for VLLM's OpenAI-compatible API server with completions and embeddings support"""
import json
from typing import Iterable, List, Dict, Optional, Union, Any
from dataclasses import dataclass
from agentforge.utils import logger
import requests


@dataclass
class ResponseFormat:
    """Response format specification"""
    type: str  # 'json_object', 'json_schema', or 'text'


def create_completion(
    # Required parameters
    api_url: str,
    prompt: str,
    model: str,
    
    # Basic OpenAI parameters
    max_tokens: int = 16,
    temperature: float = 0.0,
    top_p: float = 1.0,
    stream: bool = False,
    stop: Optional[List[str]] = None,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    
    # VLLM sampling parameters
    use_beam_search: bool = False,
    top_k: int = -1,
    min_p: float = 0.0,
    repetition_penalty: float = 1.0,
    length_penalty: float = 1.0,
    stop_token_ids: Optional[List[int]] = None,
    include_stop_str_in_output: bool = False,
    ignore_eos: bool = False,
    min_tokens: int = 0,
    skip_special_tokens: bool = True,
    spaces_between_special_tokens: bool = True,
    truncate_prompt_tokens: Optional[int] = None,
    allowed_token_ids: Optional[List[int]] = None,
    prompt_logprobs: Optional[int] = None,
    
    # VLLM extra parameters
    add_special_tokens: bool = True,
    response_format: Optional[ResponseFormat] = None,
    guided_json: Optional[Union[str, dict, Any]] = None,
    guided_regex: Optional[str] = None,
    guided_choice: Optional[List[str]] = None,
    guided_grammar: Optional[str] = None,
    guided_decoding_backend: Optional[str] = None,
    guided_whitespace_pattern: Optional[str] = None,
    priority: int = 0,
    
    # Request customization
    extra_headers: Optional[Dict[str, str]] = None,
    n: Optional[int] = None,
    best_of: Optional[int] = None,
    logit_bias: Optional[Dict[int, float]] = None,
    user: Optional[str] = None,
    **kwargs: Any,  # Catch any other parameters we don't explicitly handle
) -> requests.Response:
    """
    Creates a completion request using VLLM's OpenAI-compatible API with all supported parameters.
    [Previous docstring remains the same...]
    """
    headers = {
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    # [Previous payload construction remains the same...]
    payload = {
        # "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stream": stream,
        "stop": stop,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        
        # VLLM sampling parameters
        "use_beam_search": use_beam_search,
        "top_k": top_k,
        "min_p": min_p,
        "repetition_penalty": repetition_penalty,
        "length_penalty": length_penalty,
        "include_stop_str_in_output": include_stop_str_in_output,
        "ignore_eos": ignore_eos,
        "min_tokens": min_tokens,
        "skip_special_tokens": skip_special_tokens,
        "spaces_between_special_tokens": spaces_between_special_tokens,
        "add_special_tokens": add_special_tokens,
        "priority": priority,
    }
    
    # [Previous optional parameter handling remains the same...]
    if stop_token_ids:
        payload["stop_token_ids"] = stop_token_ids
    if truncate_prompt_tokens:
        payload["truncate_prompt_tokens"] = truncate_prompt_tokens
    if allowed_token_ids:
        payload["allowed_token_ids"] = allowed_token_ids
    if prompt_logprobs is not None:
        payload["prompt_logprobs"] = prompt_logprobs
    if response_format:
        payload["response_format"] = response_format.__dict__
    if guided_json:
        payload["guided_json"] = guided_json
    if guided_regex:
        payload["guided_regex"] = guided_regex
    if guided_choice:
        payload["guided_choice"] = guided_choice
    if guided_grammar:
        payload["guided_grammar"] = guided_grammar
    if guided_decoding_backend:
        payload["guided_decoding_backend"] = guided_decoding_backend
    if guided_whitespace_pattern:
        payload["guided_whitespace_pattern"] = guided_whitespace_pattern

    logger.info(f"Prompt Length: {len(prompt)}")
    return requests.post(api_url, headers=headers, json=payload, stream=stream)


def create_embeddings(
    api_url: str,
    model: str,
    input: Union[str, List[str]],
    messages: Optional[List[Dict[str, str]]] = None,
    encoding_format: Optional[str] = None,
    add_special_tokens: bool = True,
    priority: int = 0,
    additional_data: Optional[Any] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> requests.Response:
    """
    Creates embeddings using VLLM's OpenAI-compatible embeddings API.
    
    Args:
        api_url: The URL of the VLLM embeddings endpoint
        model: Model identifier
        input: String or array of strings to embed
        messages: Optional list of messages in chat format for embedding
        encoding_format: Optional format specification for encoding ('float' or 'base64')
        add_special_tokens: Whether to add special tokens to the input
        priority: Request priority (lower = higher priority)
        additional_data: Additional data to pass to the API
        extra_headers: Additional HTTP headers to include
    
    Returns:
        requests.Response: The HTTP response containing embeddings
        
    Note:
        - Server must be started with --task embedding for embedding support
        - Can pass either input strings or messages (chat format), not both
    """
    headers = {
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    payload = {
        "model": model,
        "add_special_tokens": add_special_tokens,
        "priority": priority,
    }

    # Add either input or messages, not both
    if messages is not None:
        payload["messages"] = messages
    else:
        payload["input"] = input

    if encoding_format:
        payload["encoding_format"] = encoding_format
    if additional_data is not None:
        payload["additional_data"] = additional_data

    return requests.post(api_url, headers=headers, json=payload)


def get_streaming_response(response: requests.Response) -> Iterable[str]:
    """
    Yields text from a streaming response.
    [Previous implementation remains the same...]
    """
    for line in response.iter_lines(decode_unicode=True):
        if line:
            if line.startswith('data: '):
                line = line[6:]  # Remove 'data: ' prefix
            if line != '[DONE]':
                data = json.loads(line)
                yield data['choices'][0]['text']


def get_completion_text(response: requests.Response) -> str:
    """
    Gets completion text from a non-streaming response.
    [Previous implementation remains the same...]
    """
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}\n{response.text}")
    return response.json()['choices'][0]['text']


def get_embeddings(response: requests.Response) -> List[List[float]]:
    """
    Gets embeddings from an embedding response.
    
    Args:
        response: Response from create_embeddings
        
    Returns:
        List of embedding vectors
        
    Raises:
        Exception: If the request failed
    """
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}\n{response.text}")
    return [data["embedding"] for data in response.json()["data"]]