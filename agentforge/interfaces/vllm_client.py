"""Example Python client for vllm.entrypoints.api_server"""

import argparse
import json
from typing import Iterable, List
from agentforge.utils import logger
import requests

def clear_line(n: int = 1) -> None:
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for _ in range(n):
        print(LINE_UP, end=LINE_CLEAR, flush=True)

def post_http_request(api_url: str,
                      prompt: str,
                      max_tokens: int = 16,
                      temperature: float = 0.0,
                      repetition_penalty: float = 1.0,
                      top_p: float = 1.0,
                      top_k: int = -1,
                      stop: List[List[str]] = [],
                      stream: bool = False,
                      n: int = 1) -> requests.Response:
    headers = {"User-Agent": "Test Client"}
    pload = {
        "prompt": prompt,
        "n": n,
        "use_beam_search": False,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
        "repetition_penalty": repetition_penalty,
        "presence_penalty": 1.5,
        "top_p": top_p,
        "top_k": top_k,
        "stop": stop,
    }
    logger.info(f"Prompt Length: {len(prompt)}")
    response = requests.post(api_url, headers=headers, json=pload, stream=True)
    return response

def get_streaming_response(response: requests.Response) -> Iterable[List[str]]:
    for chunk in response.iter_lines(chunk_size=8192,
                                     decode_unicode=False,
                                     delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode("utf-8"))
            output = data["text"]
            yield output


def get_response(response: requests.Response) -> List[str]:
    data = json.loads(response.content)
    output = data["text"]
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--base_prompt", type=str, default="San Francisco is a beautiful city. It is known for its hills and the Golden Gate Bridge. The city is surrounded by water on three sides. The city is also known for its diverse population. There are many different cultures in San Francisco.") 
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    prompt = """San Francisco is a beautiful city. It is known for its hills and the Golden Gate Bridge. The city is surrounded by water on three sides. The city is also known for its diverse population. There are many different cultures in San Francisco. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love. Beautiful city that we all love."""
    api_url = f"http://{args.host}:{args.port}/generate"
    n = args.n

    # Define default values for additional parameters
    max_tokens = 16
    temperature = 0.0
    repetition_penalty = 1.0
    top_p = 1.0
    top_k = -1
    stop = []
    stream = args.stream
    word_to_add = "Yes"
    # Initialize the tokenizer for the specified model
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("uukuguy/speechless-llama2-luban-orca-platypus-13b")

    def estimate_token_count(prompt: str) -> int:
            
        """
        Estimate the number of tokens in a given prompt.
        """
        return len(tokenizer.encode(prompt))

    while True:
        try:
            # Print current prompt and estimated token count
            token_count = estimate_token_count(prompt)
            print(f"\nCurrent Prompt: {prompt!r}")
            print(f"Estimated Token Count: {token_count}")

            # Make API request
            response = post_http_request(
                api_url, 
                prompt, 
                max_tokens=max_tokens, 
                temperature=temperature, 
                repetition_penalty=repetition_penalty, 
                top_p=top_p, 
                top_k=top_k, 
                stop=stop, 
                stream=stream, 
                n=n
            )
            if response.status_code == 200:
                # Process response
                if stream:
                    output = next(get_streaming_response(response))
                else:
                    output = get_response(response)
                print(f"API Response: {output}")
            else:
                print(f"API Request Failed with status code {response.status_code}")
                break

            # Add another word to the prompt
            prompt += " " + word_to_add

        except Exception as e:
            print(f"An error occurred: {e}")
            break