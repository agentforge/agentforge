# # importing the sys module
import sys, os
 
# # appending the directory of mod.py
# # in the sys.path list
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'/app/agentforge'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from agentforge.utils import measure_time
from agentforge import DST_PATH
from agentforge.factories import resource_factory

app = Flask(__name__)
CORS(app)

from dotenv import load_dotenv
load_dotenv('../../../.env')

w2l = resource_factory.get_resource("w2l")

@app.route("/v1/lipsync", methods=["POST"])
@measure_time
def lipsync():
  # Get the wav file from the request
  wav_file = request.json["audio_response"]
  avatar = request.json["avatar_config"]

  # Interpret the wav file
  opts = {
    "avatar": "default", # TODO: pull this from avatar, add to frontend
    "face": "/app/cache/default.mp4", # TODO: pull this from avatar, add to frontend
    "audio": wav_file,
    "outfile": "/app/cache/lipsync.mp4"
  }

  response = w2l.run(opts)

  # Return the text in the response
  return jsonify(response)

if __name__ == '__main__':
  app.run()
