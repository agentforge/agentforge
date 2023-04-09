### Ensure local libs are available for Flask
from pathlib import Path
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from historica.helpers import measure_time

from . import Whisper
from . import TextToSpeech

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
app = Flask(__name__)
CORS(app, resources={r"/v1/*": {"origins": "*"}})
tts_inst = TextToSpeech()
whisper = Whisper()

@app.route("/v1/whisper", methods=["POST"])
def whisper_api():
    # Save the uploaded wav file
    audio_file = request.files["audio"]
    wav_file_path = secure_filename(audio_file.filename)
    audio_file.save(wav_file_path)

    # Interpret the audio using the Whisper class
    generated_text = whisper.interpret(wav_file_path)

    # Return the generated text
    return {"generated_text": generated_text}

# Given the following text request generate a wav file and return to the client
@app.route("/v1/tts", methods=["POST"])
@measure_time
def text_to_speech():
  # Get the text and filename from the request
  prompt = request.json["prompt"]
  avatar = request.json["avatar"]

  filename = "/app/files/out.wav"
  speaker_wav = avatar["speaker_wav"] if "speaker_wav" in avatar else None
  speaker_idx = avatar["speaker_idx"] if "speaker_idx" in avatar else 0

  # Enqueue a job in the TTS pipeline
  filename = tts_inst.synthesizer(
    prompt,
    filename, 
    speaker_wav=speaker_wav,
    speaker_idx=speaker_idx
  )
  # Return the wav file in the response
  print(filename)
  return jsonify({"filename": filename})

# Define the /interpret endpoint
@app.route("/v1/interpret", methods=["POST"])
@measure_time
def interpret():
  # Get the wav file from the request
  wav_file = request.files["wav_file"]

  # Interpret the wav file
  text = whisper.interpret(wav_file)

  # Return the text in the response
  return jsonify({"text": text})

if __name__ == '__main__':
  app.run()
