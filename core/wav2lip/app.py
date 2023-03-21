### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.wav2lip.wav2lip import Wav2Lip

app = Flask(__name__)
CORS(app)
wav2lip = Wav2Lip()

FILES_DIR = "/app/files/"

# Define the /interpret endpoint
@app.route("/v1/lipsync", methods=["POST"])
def interpret():
  # Get the wav file from the request
  wav_file = FILES_DIR + request.json["wav_file"]
  mp4_file = '/app/cache/loop.mp4'

  output_file = "lipsync.mp4"

  # Interpret the wav file
  wav2lip.run(mp4_file, wav_file, output_file)

  # Return the text in the response
  return jsonify({"filename": output_file})

if __name__ == '__main__':
  app.run()
