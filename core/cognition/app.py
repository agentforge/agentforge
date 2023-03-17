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

logging.basicConfig(filename='agent.log', level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
#llm = Agent()
llm = Alpaca()
# Given the following text request generate a wav file and return to the client
@app.route("/llm/inference", methods=["POST"])
def output():
  prompt = request.json["prompt"]
  output = llm.generate(prompt)
  return jsonify({"output": output})

if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('-model', dest='model', default='gpt2')
  args = parser.parse_args()
  model = args.model
  llm.load(model, "llm")
  app.run()
