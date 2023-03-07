from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from core.speech.tts import TTS
from speech.whisper import Whisper

app = Flask(__name__)
CORS(app)
tts = TTS()

# Given the following text request generate a wav file and return to the client
@app.route("/speech", methods=["POST"])
def tts():
  # Get the text and filename from the request
  text = request.json["text"]
  filename = "out.wav"

  # Enqueue a job in the TTS pipeline
  filename = tts.synthesizer(text, filename)

  # Return the wav file in the response
  print(filename)
  return send_file(
    filename,
    mimetype="audio/wav",
  )

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
