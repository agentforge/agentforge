#!/usr/bin/python3
# Path: core/wav2lip/app.py

### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.wav2lip.wav2lip2 import Wav2LipModel
from core.helpers.helpers import measure_time

app = Flask(__name__)
CORS(app)
CHKPT_PTH = "/app/cache/wav2lip_gan.pth"
wav2lip = Wav2LipModel(CHKPT_PTH)

# Define the /interpret endpoint
@app.route("/v1/lipsync", methods=["POST"])
@measure_time
def lipsync():
  # Get the wav file from the request
  wav_file = request.json["wav_file"]
  avatar = request.json["avatar"]
  mp4_file = "/app/cache/#{avatar}.mp4"

  output_file = "/app/files/lipsync.mp4"

  # Interpret the wav file
  wav2lip.run({"face": mp4_file, "audio": wav_file, "outfile": output_file})

  # Return the text in the response
  return jsonify({"filename": output_file})

if __name__ == '__main__':
  app.run()
