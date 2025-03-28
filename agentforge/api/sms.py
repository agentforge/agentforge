from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from agentforge.ai import agent_interactor
from agentforge.interfaces.model_profile import ModelProfile

router = APIRouter()

@router.post("/", operation_id="createSmsCompletion")
def sms_reply(request: Request) -> PlainTextResponse:
    # Get message body
    data = request.form.get('Body')

    model_profiles = ModelProfile()
    model_profile = model_profiles.get_profile_by_name('sms')
    
    ## Get agent from agent Factory and run it
    agent = agent_interactor.get_agent()

    output = agent.run({"input": {"prompt": data}, "model_profile": model_profile})
    # Respond to the SMS
    twilio_resp = MessagingResponse()
    twilio_resp.message(output["response"])
    return PlainTextResponse(str(twilio_resp))