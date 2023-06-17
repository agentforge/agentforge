from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from agentforge.interfaces import interface_interactor
from base64 import b64encode
from agentforge.ai import decision_interactor
from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.interfaces.model_profile import ModelProfile

# Setup Agent
decision = decision_interactor.create_decision()

class AgentResponse(BaseModel):
  data: dict

router = APIRouter()
redis_store = interface_interactor.create_redis_connection()

def redis_pubsub_channel(redis_client, channel_name="mychannel"):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel_name)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            yield f"data: {data}\n\n"


@router.get("/stream")
async def stream():
    return StreamingResponse(redis_pubsub_channel(), media_type="text/event-stream")

@router.get("/")
def hello() -> AgentResponse:
    return AgentResponse(data={"response": "Hello world"})

@router.post('/v1/completions')
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
    
    output = decision.run({"input": data, "model_profile": model_profile})

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

    ## Return Decision output
    return AgentResponse(data=output)
