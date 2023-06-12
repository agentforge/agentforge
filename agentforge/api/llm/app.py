### Ensure local libs are available for Flask
from pathlib import Path
from dotenv import load_dotenv
import sys, os
import redis
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.factories import resource_factory

# Setup app and environment
load_dotenv('../../../.env')
app = Flask(__name__)
CORS(app)
llm = resource_factory.get_resource("llm")

# Given the following text request generate a wav file and return to the client
@app.route("/v1/completions", methods=["POST"])
@measure_time
def output():
  config = request.json
  response = llm.generate(**config)
  return jsonify({"choices": [{"text": response}]})

if __name__ == "__main__":
    app.run(debug=True)
