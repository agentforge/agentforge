### Ensure local libs are available for Flask
from pathlib import Path
import sys

### RESTful API for the LLM services
### Maintains any necessary queue and rate limiting for
### accessing GPU/TPU resources

### Imports ###
import requests, json, redis
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from flask_sse import sse
import logging

from historica.language_model import Alpaca
from historica.helpers import measure_time

#logging.basicConfig(filename='agent.log', level=logging.DEBUG)
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

app = Flask(__name__)
CORS(app)

# llm = Agent()
# llm.setup_agent()
# llm.load_agent()

### Alpaca -- Stanford's davinci-003 model
llm = Alpaca()
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://redis:6379/0"
app.register_blueprint(sse, url_prefix='/stream')

redis_store = redis.StrictRedis().from_url(app.config["REDIS_URL"])

def send_to_rails_api(channel, message):
    rails_api_url = "http://your_rails_api_domain.com/publish"
    payload = {"channel": channel, "message": message}
    response = requests.post(rails_api_url, data=payload)
    return response

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
  print(request.json)
  prompt = request.json["prompt"]
  config = request.json
  print(f"Prompt: {prompt}")
  print(f"Config: {config }")
  llm.configure(config)
  response = llm.generate(prompt)
  print(response)
  return jsonify({"choices": [{"text": response}]})

@app.route("/v1/update_model", methods=["POST"])
def update_model():
    global llm
    model_name = request.json["model_name"]
    llm.llm.switch_model(model_name)
    return jsonify({"message": f"Model state updated to {model_name}"})

if __name__ == "__main__":
    app.run(debug=True)
