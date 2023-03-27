### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.wav2lip.wav2lip2 import Wav2LipModel
from core.helpers.helpers import measure_time
from core.wav2lip.wav2lip import Wav2Lip

app = Flask(__name__)
CORS(app)
CHKPT_PTH = "/app/cache/wav2lip_gan.pth"
# Default face loop
# TODO: When we introduce multiple avatars this will need refactoring
faces = [
  ("loop", "/app/cache/loop.mp4"),
  ("makhno", "/app/cache/makhno.mp4"),
]
opts = {}
wav2lip = Wav2LipModel(CHKPT_PTH, opts, faces)
# wav2lip = Wav2Lip()
# Define the /interpret endpoint

@app.route("/v1/lipsync", methods=["POST"])
@measure_time
def lipsync():
  # Get the wav file from the request
  wav_file = request.json["wav_file"]
  avatar = request.json["avatar"]
  mp4_file = f"/app/cache/{avatar}.mp4"

  output_file = "/app/files/lipsync.mp4"

  # Interpret the wav file
  wav2lip.run({"face": mp4_file, "audio": wav_file, "outfile": output_file, "avatar": avatar})

  # Return the text in the response
  return jsonify({"filename": output_file})

if __name__ == '__main__':
  app.run()
