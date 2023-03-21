### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from core.speech.tts import TTS
from speech.whisper import Whisper

app = Flask(__name__)
CORS(app)
tts_inst = TTS()
whisper = Whisper()

# Given the following text request generate a wav file and return to the client
@app.route("/tts/speech", methods=["POST"])
def text_to_speech():
  # Get the text and filename from the request
  prompt = request.json["prompt"]
  filename = "out.wav"

  # Enqueue a job in the TTS pipeline
  filename = tts_inst.synthesizer(prompt, filename)

  # Return the wav file in the response
  print(filename)
  return jsonify({"filename": filename})

# Define the /interpret endpoint
@app.route("/interpret", methods=["POST"])
def interpret():
  # Get the wav file from the request
  wav_file = request.files["wav_file"]

  # Interpret the wav file
  text = whisper.interpret(wav_file)

  # Return the text in the response
  return jsonify({"text": text})

if __name__ == '__main__':
  app.run()
