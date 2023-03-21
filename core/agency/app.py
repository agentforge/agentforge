### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

### RESTful API for the LLM worker

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from core.worker.worker import Worker
from redis import Redis
from rq import Queue
import logging
from core.agency.executive import ExecutiveCognition
from core.helpers.helpers import measure_time

queue = Queue(connection=Redis())
worker = Worker()

#logging.basicConfig(filename='agent.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

executive = ExecutiveCognition()

### Main endpoint of the Agent API
### Agent API is responsible for managing the queue of requests
### and uses a ReAct/MERKL LLM to determine what tool service to use
### and what parameters to use for the request

# Define the API endpoint for prompting the agent
@app.route("/v1/completions", methods=["POST"])
@measure_time
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]

  # Run the LLM agent
  response = executive.respond(prompt)

  # Run text classification and intent detection
  ## TODO: Implement this

  print(response)
  # Return the response
  return jsonify(response)

# Define the API endpoint for hearing the agent speak
@app.route("/v1/tts", methods=["POST"])
@measure_time
def tts():
    # Get the message for the request
    prompt = request.json["prompt"]
    generate_lip_sync = request.json["generate_lip_sync"]
    generate_lip_sync = True if generate_lip_sync == "true" else False
    
    # Run the agent
    response = executive.speak(prompt, generate_lip_sync)
    filename = response["filename"]
    
    # Create a response object with the file data
    response_obj = send_file(
        filename,
        mimetype=response["type"],
        as_attachment=True
    )
    # Set the headers
    response_obj.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response_obj
