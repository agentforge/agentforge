### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

### RESTful API for the LLM services
### Maintains any necessary queue and rate limiting for
### accessing GPU/TPU resources

### Imports ###
import json
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from core.cognition.alpaca import Alpaca
import logging
from core.helpers.helpers import measure_time

#logging.basicConfig(filename='agent.log', level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

### Alpaca -- Stanford's davinci-003 model
LLM_MODEL="decapoda-research/llama-7b-hf"
PEFT_MODEL="tloen/alpaca-lora-7b"

#LLM_MODEL="decapoda-research/llama-13b-hf-int4"
#PEFT_MODEL="chansung/alpaca-lora-13b"

CONFIG_NAME="llm/logical"

# llm = Agent()
# llm.setup_agent()
llm = Alpaca({"model_name": LLM_MODEL, "generation_config": CONFIG_NAME, "peft_model": PEFT_MODEL })
llm.setup_alpaca()

llm.init_tools()
llm.load_agent()

# Given the following text request generate a wav file and return to the client
@app.route("/v1/completions", methods=["POST"])
@measure_time
def output():
  prompt = request.json["prompt"]
  config = request.json["config"]
  config = config.replace("=>", ":") # Fix for ruby hash syntax
  print(f"Prompt: {prompt}")
  print(f"Config: {config }")
  llm.configure(json.loads(config))
  response = llm.generate(prompt)
  print(response.response)
  return jsonify({"response": response.response, "output": response.output, "thought": response.thought})


@app.route("/v1/update_model", methods=["POST"])
def update_model():
    global llm
    model_name = request.json["model_name"]
    config_name = request.json["config_name"]
    peft_name = request.json["peft_name"]
    llm = Alpaca({"model_name": model_name, "config": config_name, "peft_name": peft_name})
    llm.setup_alpaca()
    return jsonify({"message": f"Model state updated to {model_name}"})


if __name__ == "__main__":
    app.run(debug=True)
