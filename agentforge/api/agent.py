from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agentforge.interfaces import interface_interactor
from base64 import b64encode
from agentforge.ai import agent_interactor
from agentforge.interfaces.model_profile import ModelProfile
import asyncio, uuid
from aioredis import Redis
import traceback, json
from agentforge.utils import logger
from agentforge.utils.parser import Parser
from supertokens_python.recipe.session.asyncio import get_session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.emailpassword.asyncio import get_user_by_id
from fastapi import Depends

### PRETTY PRINT THE REQUEST -- TODO: MOVE TO UTILS
async def pretty_print_request(request: Request) -> None:
    """
    Prints the details of a Starlette request in a readable format.
    """
    # Get basic request details
    request_details = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
    }

    # Try to extract the body if it's JSON, handle other types or errors gracefully
    try:
        body = await request.json()
        request_details["body"] = body
    except json.JSONDecodeError:
        body = await request.body()
        request_details["body"] = body.decode() if body else "No body"

    # Pretty print the request details
    print(json.dumps(request_details, indent=4, sort_keys=True))


# Setup Agent
agent = agent_interactor.create_agent()
parser = Parser() # for quick stream parsing

class AgentResponse(BaseModel):
  data: dict

router = APIRouter()
# redis_store = interface_interactor.create_redis_connection()
import os
import nltk

# Function to check if wordnet is downloaded
def is_wordnet_downloaded(nltk_data_path):
    for path in nltk.data.path:
        if os.path.exists(os.path.join(path, 'corpora/wordnet.zip')):
            return True
    return False

# Check if wordnet is downloaded, if not, download it
if not is_wordnet_downloaded(nltk.data.path):
    nltk.download('wordnet')

@router.get("/", operation_id="helloWorld")
def hello() -> AgentResponse:
    return AgentResponse(data={"response": "Hello world"})

@router.get("/abort", operation_id="abort")
def abort() -> AgentResponse:
    agent = agent_interactor.get_agent()
    agent.abort()
    return AgentResponse(data={"response": "aborted"})

"""OpenAI-compatible agent API endpoint with direct configuration handling"""

@router.post('/completions', operation_id="createChatCompletion")
async def agent(request: Request) -> AgentResponse:
    request_val = await pretty_print_request(request)
    logger.info(request_val)
    session = await get_session(request)

    if session is None:
        return {"message": "unauthorized"}

    user_id = session.get_user_id()
    # user = await get_user_by_id(user_id)

    # Parse request data
    data = await request.json()
    logger.info("DATA")
    logger.info(data)

    # Add user information
    # data['user_id'] = user_id
    # if 'user_name' not in data:
    #     user_name = user.email.split("@")[0]
    #     data['user_name'] = user_name
    # else:
    #     user_name = data['user_name']

    # logger.info(f"user_name: {user_name}")

    # Construct model profile from request data instead of DB
    model_profile = {
        "model_config": {
            "model_name": data.get("model", "default_model"),
            "streaming": data.get("stream", False),
        },
        "generation_config": {
            # Standard OpenAI parameters
            "max_tokens": data.get("max_tokens", 16),
            "temperature": data.get("temperature", 1.0),
            "top_p": data.get("top_p", 1.0),
            "n": data.get("n", 1),
            "presence_penalty": data.get("presence_penalty", 0.0),
            "frequency_penalty": data.get("frequency_penalty", 0.0),
            
            # VLLM specific parameters if provided
            "use_beam_search": data.get("use_beam_search", False),
            "top_k": data.get("top_k", -1),
            "min_p": data.get("min_p", 0.0),
            "repetition_penalty": data.get("repetition_penalty", 1.0),
            "length_penalty": data.get("length_penalty", 1.0),
            "stop_token_ids": data.get("stop_token_ids"),
            "include_stop_str_in_output": data.get("include_stop_str_in_output", False),
            "ignore_eos": data.get("ignore_eos", False),
            "min_tokens": data.get("min_tokens", 0),
            "skip_special_tokens": data.get("skip_special_tokens", True),
            "spaces_between_special_tokens": data.get("spaces_between_special_tokens", True),
        }
    }

    # Add optional parameters if present
    optional_params = [
        "truncate_prompt_tokens", "allowed_token_ids", "prompt_logprobs",
        "guided_json", "guided_regex", "guided_choice", "guided_grammar",
        "guided_decoding_backend", "guided_whitespace_pattern"
    ]
    for param in optional_params:
        if param in data:
            model_profile["generation_config"][param] = data[param]

    # Add any stop sequences
    if "stop" in data:
        model_profile["generation_config"]["stop"] = data["stop"]

    if model_profile['model_config']['streaming']:
        agent = agent_interactor.get_agent()
        output = agent.run({"input": data, "model": model_profile})

        async def event_generator():
            redis = Redis.from_url('redis://redis:6379/0')
            async with redis.client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe(f"streaming-{user_id}")
                while True:
                    message = await pubsub.get_message()
                    if message and message['type'] == 'message':
                        try:
                            val = message['data'].decode('utf-8')
                        except Exception as e:
                            print(e)
                            traceback.print_exc()
                            val = "ERR"
                        # Strip off the </s> if it's there
                        if len(val) >= 4 and val[-4:] == '</s>':
                            val = val[:-4]
                            yield str(val)
                            break
                        elif len(val) >= 13 and val[-13:] == '<|endoftext|>':
                            val = val[:-13]
                            yield str(val)
                            break
                        yield str(val)
                    else:
                        await asyncio.sleep(1)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    else:
        agent = agent_interactor.get_agent()
        output = agent.run({"input": data, "model": model_profile})
        logger.info("[DEBUG][api][agent][agent] agent: " + output.pretty_print())

        # Handle video response
        if output.has_key('video'):
            filename = output.get("video.lipsync_response")
            with open(filename, 'rb') as fh:
                return AgentResponse(
                    data = {
                        'choices': [{"text": output.get("response")}],
                        'video': b64encode(fh.read()).decode()
                    }
                )

        # Handle audio response
        if output.has_key('audio'):
            filename = output.get("audio.audio_response")
            with open(filename, 'rb') as fh:
                return AgentResponse(
                    data = {
                        'choices': [{"text": output.get("response")}],
                        'audio': b64encode(fh.read()).decode()
                    }
                )

        return AgentResponse(data=output.get_model_outputs())

### Streaming for old Forge
@router.get("/completions/stream/{channel}")
def stream(channel: str):
    id = 5
    async def event_generator():
        redis = Redis.from_url('redis://redis:6379/0')
        async with redis.client() as client:
            pubsub = client.pubsub()
            await pubsub.subscribe('video')
            while True:
                message = await pubsub.get_message()
                if message and message['type'] == 'message' and message['data'] == b'<|endofvideo|>':
                    yield '<|endofvideo|>'
                    break
                if message and message['type'] == 'message':
                    try:
                        data = json.loads(message['data']) 
                        val = data['data']
                        _id = data['id']
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        val = "ERR"
                    response = f"id: {str(_id)}\ndata: {str(val)}\n\n"  # Include the ID in the response
                    yield response
                else:
                    response = f"id: {0}\ndata: {str('data')}\n\n"  # Include the ID in the response
                    yield response
                    await asyncio.sleep(1)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "text/event-stream; charset=utf-8",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache, no-transform",
        "X-Accel-Buffering": "no",
        "Content-Encoding": "none",
    }
    
    response = StreamingResponse(event_generator(), media_type="text/event-stream")
    response.init_headers(headers)
    return response
