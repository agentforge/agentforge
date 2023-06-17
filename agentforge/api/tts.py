import os
from fastapi import Request
from pydantic import BaseModel
from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.factories import resource_factory
from dotenv import load_dotenv
from .app import init_api
load_dotenv('../../../.env')

app = init_api()
tts = resource_factory.get_resource("tts")

class TtsResponse(BaseModel):
  filename: str

# Given the following text request generate a wav file and return to the client
@app.post("/v1/tts")
@comprehensive_error_handler
@measure_time
async def text_to_speech(request: Request) -> TtsResponse:
  # Get the text and filename from the request
  prompt = request.json["prompt"]
  avatar = request.json["avatar"]

  filename = "/app/cache/out.wav"
  speaker_wav = os.environ.get('DST_PATH') + avatar["speaker_wav"] if "speaker_wav" in avatar else None
  speaker_idx = avatar["speaker_idx"] if "speaker_idx" in avatar else 0

  # Enqueue a job in the TTS pipeline
  filename = tts.synthesizer(
    prompt,
    filename, 
    speaker_wav=speaker_wav,
    speaker_idx=speaker_idx
  )
  # Return the wav file in the response
  return TtsResponse(filename=filename)
