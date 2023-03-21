### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

### RESTful API for the LLM services
### Maintains any necessary queue and rate limiting for
### accessing GPU/TPU resources

### Imports ###
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from core.cognition.agent import Agent
from core.cognition.alpaca import Alpaca
import logging
from core.helpers.helpers import measure_time

logging.basicConfig(filename='agent.log', level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
#llm = Agent()
llm = Alpaca()
llm.setup_alpaca()

llm.init_tools()
llm.create_prompt()
llm.load_agent()

# Given the following text request generate a wav file and return to the client
@app.route("/v1/completions", methods=["POST"])
@measure_time
def output():
  prompt = request.json["prompt"]
  response = llm.generate(prompt)
  print(response.response)
  return jsonify({"response": response.response, "output": response.output, "thought": response.thought})
