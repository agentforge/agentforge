### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from agentforge.utils import measure_time
from agentforge import DST_PATH
from agentforge.factories import resource_factory

app = Flask(__name__)
CORS(app)

from dotenv import load_dotenv
load_dotenv('../../../.env')

CHKPT_PTH = DST_PATH + "/weights/wav2lip_gan.pth"
# Default face loop
# TODO: When we introduce multiple avatars this will need refactoring
faces = [
  ("default", DST_PATH + "/videos/default.mp4"),
  ("caretaker", DST_PATH + "/videos/default.mp4"),
  ("makhno", DST_PATH + "/videos/makhno.mp4"),
  ("fdr", DST_PATH + "/videos/fdr.mp4"),
  ("sankara", DST_PATH + "/videos/sankara.mp4"),
]
opts = {}

w2l = resource_factory.get_resource("w2l")

# wav2lip = Wav2Lip()
# Define the /interpret endpoint

@app.route("/v1/lipsync", methods=["POST"])
@measure_time
def lipsync():
  # Get the wav file from the request
  wav_file = request.json["wav_file"]
  avatar = request.json["avatar"]

  output_file = "/app/cache/lipsync.mp4"

  # Interpret the wav file
  opts = {
    "face": avatar["mp4"],
    "audio": wav_file,
    "outfile": output_file,
    "avatar": avatar["avatar"]
  }

  w2l.run(opts)

  # Return the text in the response
  return jsonify({"filename": output_file})

if __name__ == '__main__':
  app.run()
