from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.factories import resource_factory


app = FastAPI()

cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
load_dotenv('../../../.env')

w2l = resource_factory.get_resource("w2l")

class lipsyncResponse(BaseModel):
  filename: str

@app.post("/v1/lipsync", operation_id="createVideoResponse")
async def lipsync(request: Request) -> lipsyncResponse:
  # Get the wav file from the request
  try:
    data = await request.json()

    wav_file = data["audio_response"]
    # avatar = data["avatar_config"]

    # Interpret the wav file
    opts = {
      "avatar": "default", # TODO: pull this from avatar, add to frontend
      "face": "/app/cache/default.mp4", # TODO: pull this from avatar, add to frontend
      "audio": wav_file,
      "outfile": "/app/cache/lipsync.mp4"
    }
    print(wav_file)
    response = w2l.run(opts)

    # Return the text in the response
    return lipsyncResponse(filename=response['filename'])
  except Exception as e:
    print(e)
    print("Error in lipsync")
    import traceback
    traceback.print_exc()
    return lipsyncResponse(filename="error")
if __name__ == '__main__':
  app.run()
