from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agentforge.interfaces import interface_interactor
from base64 import b64encode
from agentforge.ai import decision_interactor
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.api.auth import get_api_key
import asyncio

# Setup Agent
decision = decision_interactor.create_decision()

class AgentResponse(BaseModel):
  data: dict

router = APIRouter()
# redis_store = interface_interactor.create_redis_connection()

@router.get("/stream/{channel}")
def stream(channel: str):
    pubsub = app.state.redis.pubsub()
    pubsub.subscribe(channel)
    async def event_generator():
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                yield {"data": message["data"].decode("utf-8")}
            else:
                asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/", operation_id="helloWorld", dependencies=[Depends(get_api_key)])
def hello() -> AgentResponse:
    return AgentResponse(data={"response": "Hello world"})

@router.post('/v1/completions', operation_id="createChatCompletion") #, dependencies=[Depends(get_api_key)])
async def agent(request: Request) -> AgentResponse:
    ## Parse Data --  from web accept JSON, from client we need to pull ModelConfig
    ## and add add the prompt and user_id to the data
    data = await request.json()

    ## TODO: Verify auth, rate limiter, etc -- should be handled by validation layer
    if 'id' not in data:
        return {"error": "No model profile specified."}

    model_profiles = ModelProfile()
    model_profile = model_profiles.get(data['id'])
    
    ## Get Decision from Decision Factory and run it
    decision = decision_interactor.get_decision()

    # print("[DEBUG][api][agent][agent] decision: ", decision)

    output = decision.run({"input": data, "model_profile": model_profile})

    # print("[DEBUG][api][agent][agent] decision: ", output)

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

    ## Return Decision output
    return AgentResponse(data=output)
