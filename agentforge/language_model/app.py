### Ensure local libs are available for Flask
from pathlib import Path
import sys

### RESTful API for the LLM services
### Maintains any necessary queue and rate limiting for
### accessing GPU/TPU resources

### Imports ###
import redis
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS

from agentforge.helpers import measure_time
from agentforge.language_model import LLM

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

app = Flask(__name__)
CORS(app)

### Load the LLM - single GPU example
llm = LLM({"multi_gpu": False, "device_map": {'':0}, "model_key":"alpaca-lora-7b"})

### Load the LLM - multi-GPU example
# llm = LLM({"multi_gpu ": True, "device_map": "auto", "model_key":"alpaca-lora-7b"})

# Load the defaiult model
llm.load_model(llm.model_key)

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://redis:6379/0"

redis_store = redis.StrictRedis().from_url(app.config["REDIS_URL"])

# Publish streaming data to the client
@app.route('/publish', methods=['POST'])
def publish():
    channel = request.form.get('channel')
    message = request.form.get('message')
    redis_store.publish(channel, message)
    return "Message sent to the channel."

# Given the following text request generate a wav file and return to the client
@app.route("/v1/completions", methods=["POST"])
@measure_time
def output():
  config = request.json
  response = llm.generate(**config)
  return jsonify({"choices": [{"text": response}]})

@app.route("/v1/update_model", methods=["POST"])
def update_model():
    global llm
    model_name = request.json["model_name"]
    llm.llm.switch_model(model_name)
    return jsonify({"message": f"Model state updated to {model_name}"})

if __name__ == "__main__":
    app.run(debug=True)
