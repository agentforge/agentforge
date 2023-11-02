from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agentforge.interfaces import interface_interactor
from base64 import b64encode
from agentforge.ai import agent_interactor
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.api.auth import get_api_key, verify_token_exists
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

@router.get("/", operation_id="helloWorld", dependencies=[Depends(get_api_key)])
def hello() -> AgentResponse:
    return AgentResponse(data={"response": "Hello world"})

@router.get("/abort", operation_id="abort", dependencies=[Depends(get_api_key)])
def abort() -> AgentResponse:
    agent = agent_interactor.get_agent()
    agent.abort()
    return AgentResponse(data={"response": "aborted"})

@router.post('/completions', operation_id="createChatCompletion") #, dependencies=[Depends(get_api_key)])
async def agent(request: Request, session: SessionContainer = Depends(verify_session())) -> AgentResponse:
    ## Parse Data --  from web acceptuseChat JSON, from client we need to pull ModelConfig
    session = await get_session(request)

    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    user_id = session.get_user_id()

    # You can learn more about the `User` object over here https://github.com/supertokens/core-driver-interface/wiki
    user = await get_user_by_id(user_id)
    user_name = user.email.split("@")[0]

    print(f"userId {user_id}")
    ## and add add the prompt and user_id to the data
    data = await request.json()
    ## First check API key for legitimacy
    # valid_token = verify_token_exists(data)
    # if valid_token is None:
    #     return {"error": "Invalid Token."}

    # TODO: Bail on this response properly
    data['user_id'] = user_id #valid_token['user_id']
    data['user_name'] = user_name

    ## TODO: Verify auth, rate limiter, etc -- should be handled by validation layer
    if 'id' not in data:
        return {"error": "No model profile specified."}
    
    logger.info(data)

    # TODO: To make this faster we should ideally cache these models, gonna be a lot of reads and few writes here
    model_profiles = ModelProfile()

    if 'model_id' in data:
        model_profile = model_profiles.get(data['model_id'])
    else:
        model_profile = model_profiles.get(data['id'])

    if model_profile['model_config']['streaming']:
        ## Get agent from agent Factory and run it
        agent = agent_interactor.get_agent()
        output = agent.run({"input": data, "model": model_profile})

        async def event_generator():
            redis = Redis.from_url('redis://redis:6379/0')
            async with redis.client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe(f"streaming-{user_id}")
                id_counter = 0  # Initialize an ID counter
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
        ## Get agent from agent Factory and run it
        agent = agent_interactor.get_agent()
        # print("[DEBUG][api][agent][agent] agent: ", agent)
        output = agent.run({"input": data, "model": model_profile})
        # print("[DEBUG][api][agent][agent] agent: ", output)

        ### Parse video if needed
        if 'video' in output:
            filename = output['video']["lipsync_response"]

            with open(filename, 'rb') as fh:
                return AgentResponse(
                    data = {
                        'choices': [{"text": output["response"]}],
                        'video': b64encode(fh.read()).decode()
                    }
                )

        ### Parse audio if needed
        if 'audio' in output:
            filename = output['audio']["audio_response"]

            with open(filename, 'rb') as fh:
                return AgentResponse(
                    data = {
                        'choices': [{"text": output["response"]}],
                        'audio': b64encode(fh.read()).decode()
                    }
                )

        # print("[DEBUG][api][agent][agent] output: ", output)

        ## Return agent output
        return AgentResponse(data=output)

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