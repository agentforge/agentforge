### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from core.wav2lip.wav2lip import Wav2Lip

app = Flask(__name__)
CORS(app)
wav2lip = Wav2Lip()

# Define the /interpret endpoint
@app.route("/lip_sync", methods=["POST"])
def interpret():
  # Get the wav file from the request
  wav_file = request.files["wav_file"]
  mp4_file = request.files["mp4_file"]

  output_file = "lipsync.mp4"

  # Interpret the wav file
  output_vid = wav2lip.run(mp4_file, wav_file, output_file)

  # Return the text in the response
  return jsonify({"text": output_file})

if __name__ == '__main__':
  app.run()

if __name__ == '__main__':
  app.run()
