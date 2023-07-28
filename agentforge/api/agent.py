from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agentforge.interfaces import interface_interactor
from base64 import b64encode
from agentforge.ai import decision_interactor
from agentforge.interfaces.model_profile import ModelProfile
from agentforge.api.auth import get_api_key
import asyncio
from aioredis import Redis
import traceback
# Setup Agent
decision = decision_interactor.create_decision()

class AgentResponse(BaseModel):
  data: dict

router = APIRouter()
# redis_store = interface_interactor.create_redis_connection()

@router.get("/", operation_id="helloWorld", dependencies=[Depends(get_api_key)])
def hello() -> AgentResponse:
    return AgentResponse(data={"response": "Hello world"})

@router.post('/v1/completions', operation_id="createChatCompletion") #, dependencies=[Depends(get_api_key)])
async def agent(request: Request) -> AgentResponse:
    ## Parse Data --  from web acceptuseChat JSON, from client we need to pull ModelConfig
    ## and add add the prompt and user_id to the data
    data = await request.json()

    ## TODO: Verify auth, rate limiter, etc -- should be handled by validation layer
    if 'id' not in data:
        return {"error": "No model profile specified."}

    # TODO: To make this faster we should ideally cache these models, gonna be a lot of reads and few writes here
    model_profiles = ModelProfile()
    print("data", data)
    if 'modelId' in data:
        model_profile = model_profiles.get(data['modelId'])
    else:
        model_profile = model_profiles.get(data['id'])

    print("model_profile", model_profile)
    print(model_profile['model_config']['streaming'])
    if model_profile['model_config']['streaming']:
        ## Get Decision from Decision Factory and run it
        decision = decision_interactor.get_decision()
        # print("[DEBUG][api][agent][agent] decision: ", decision)
        output = decision.run({"input": data, "model_profile": model_profile})
        print("return")

        async def event_generator():
            redis = Redis.from_url('redis://redis:6379/0')
            async with redis.client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe('channel')
                while True:
                    message = await pubsub.get_message()
                    if message and message['type'] == 'message':
                        try:
                            val = message['data'].decode('utf-8')
                        except Exception as e:
                            print(e)
                            traceback.print_exc()
                            val = "ERR"
                        if val.strip() in ['</s>', '<|endoftext|>']:
                            return
                        yield str(val)
                    else:
                        await asyncio.sleep(1)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    else:
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

### Streaming for old Forge
@router.get("/stream/{channel}")
def stream(channel: str):
    print("streaming")
    # pubsub = app.state.redis.pubsub()
    # pubsub.subscribe(channel)
    async def event_generator():
        redis = Redis.from_url('redis://redis:6379/0')
        async with redis.client() as client:
            pubsub = client.pubsub()
            await pubsub.subscribe('video')
            while True:
                message = await pubsub.get_message()
                if message and message['type'] == 'message':
                    print(message)
                    try:
                        val = message['data'].decode('utf-8')
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        val = "ERR"
                    if val.strip() in ['</s>', '<|endoftext|>']:
                        return
                    yield f"data: {str(val)}\n\n"
                else:
                    yield f"data: {str('data')}\n\n"
                    await asyncio.sleep(1)
    
    # async def event_generator():
    #     for i in range(10):
    #         print(i)
    #         yield f"data: {str(i)}\n\n"  # format the event data correctly
    #         await asyncio.sleep(1)  # Give control back to the event loop
    # while True:
    #     message = pubsub.get_message(ignore_subscribe_messages=True)
    #     if message:
    #         yield {"data": message["data"].decode("utf-8")}
    #     else:
    #         asyncio.sleep(1)
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