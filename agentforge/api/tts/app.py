### Ensure local libs are available for Flask
from pathlib import Path
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from agentforge.helpers import measure_time
from agentforge import DST_PATH

from agentforge.factories import ResourceFactory

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
app = Flask(__name__)
CORS(app, resources={r"/v1/*": {"origins": "*"}})
# tts_inst = TextToSpeech()
# whisper = Whisper()

factory = ResourceFactory()
factory.create_tts_resource()
llm = factory.get_resource("tts")

# Given the following text request generate a wav file and return to the client
@app.route("/v1/tts", methods=["POST"])
@measure_time
def text_to_speech():
  # Get the text and filename from the request
  prompt = request.json["prompt"]
  avatar = request.json["avatar"]

  filename = "/app/cache/out.wav"
  speaker_wav = DST_PATH + avatar["speaker_wav"] if "speaker_wav" in avatar else None
  speaker_idx = avatar["speaker_idx"] if "speaker_idx" in avatar else 0

  # Enqueue a job in the TTS pipeline
  filename = tts_inst.synthesizer(
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
