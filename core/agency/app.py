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

queue = Queue(connection=Redis())
worker = Worker()

logging.basicConfig(filename='agent.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

executive = ExecutiveCognition()

### Main endpoint of the Agent API
### Agent API is responsible for managing the queue of requests
### and uses a ReAct/MERKL LLM to determine what tool service to use
### and what parameters to use for the request

# Define the API endpoint for prompting the agent
@app.route("/agent/prompt", methods=["POST"])
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]

  # Run the agent
  response = executive.respond(prompt)

  # Run text classification and intent detection
  ## TODO: Implement this

  # Convert text to speech and cache the wav file

  # Use the chatbot to generate a response
  # response = queue.enqueue(worker.generate, prompt)

  print(response)
  # Return the response
  return jsonify(response)

# Define the API endpoint for hearing the agent speak
@app.route("/tts", methods=["POST"])
def tts():
  # Get the message for the request
  prompt = request.json["prompt"]

  # Run the agent
  filename = executive.speak(prompt)
  print(filename)
  return send_file(
    filename,
    mimetype="audio/wav",
  )
