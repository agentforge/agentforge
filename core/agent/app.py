### Ensure local libs are available for Flask
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

### RESTful API for the LLM worker

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.worker.worker import Worker
from redis import Redis
from rq import Queue
import logging
from core.agent.cognition import Agent
from core.helpers.parser import Parser

queue = Queue(connection=Redis())
worker = Worker()

logging.basicConfig(filename='agent.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

agent_instance = Agent()
agent_instance.setup()
parser = Parser()

### Main endpoint of the Agent API
### Agent API is responsible for managing the queue of requests
### and uses a ReAct/MERKL LLM to determine what tool service to use
### and what parameters to use for the request

# Define the API endpoint for prompting the agent
@app.route("/agent/prompt", methods=["POST"])
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]

  # Parse the input message to remove any unnecessary spaces
  parser.parse(prompt)

  # Run the agent
  agent_instance.run(prompt)

  # Run text classification and intent detection
  ## TODO: Implement this

  # Convert text to speech and cache the wav file

  # Use the chatbot to generate a response
  response = queue.enqueue(worker.generate, prompt)

  print(response)
  # Return the response
  return jsonify(response)

# Run the web server
if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('--model', dest='model', default='gpt2')
  parser.add_argument('--config', dest='config', default='gpt2')

  queue = Queue(connection=Redis())
  worker = Worker()

  # Create an instance of the Flask class
  app = Flask(__name__)
  CORS(app)

  agent_instance = Agent()
  agent_instance.setup()
  parser = Parser()

  app.run()
