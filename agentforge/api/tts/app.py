### Ensure local libs are available for Flask
from pathlib import Path
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
# # importing the sys module
import sys, os
 
# # appending the directory of mod.py
# # in the sys.path list
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'/app/agentforge'))
print(sys.path)

# # importing the sys module
import sys, os
 
# # appending the directory of mod.py
# # in the sys.path list
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'/app/agentforge'))
print(sys.path)

from agentforge.utils import measure_time
from agentforge import DST_PATH

from agentforge.factories import resource_factory

# Setup environmental variables
from dotenv import load_dotenv
load_dotenv('../../../.env')

app = Flask(__name__)
CORS(app, resources={r"/v1/*": {"origins": "*"}})

tts = resource_factory.get_resource("tts")

# Given the following text request generate a wav file and return to the client
@app.route("/v1/tts", methods=["POST"])
@measure_time
def text_to_speech():
  # Get the text and filename from the request
  prompt = request.json["input"]["prompt"]
  avatar = request.json["avatar_config"]

  filename = "/app/cache/out.wav"
  speaker_wav = DST_PATH + avatar["speaker_wav"] if "speaker_wav" in avatar else None
  speaker_idx = avatar["speaker_idx"] if "speaker_idx" in avatar else 0

  # Enqueue a job in the TTS pipeline
  filename = tts.synthesizer(
    prompt,
    filename, 
    speaker_wav=speaker_wav,
    speaker_idx=speaker_idx
  )
  # Return the wav file in the response
  return jsonify({"filename": filename})

# Define the /interpret endpoint
@app.route("/v1/interpret", methods=["POST"])
@measure_time
def interpret():
  # Get the wav file from the request
  wav_file_path = request.json["file"]

  # Interpret the wav file
  text = whisper.interpret(wav_file_path)

  # Return the text in the response
  return jsonify({"text": text})

if __name__ == '__main__':
  app.run()
