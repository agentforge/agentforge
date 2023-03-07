### RESTful API for the LLM worker

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.worker.worker import Worker
from redis import Redis
from rq import Queue
import logging

queue = Queue(connection=Redis())
worker = Worker()

logging.basicConfig(filename='api.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

### Main endpoint of the Agent API
### Agent API is responsible for managing the queue of requests
### and uses a ReAct/MERKL LLM to determine what tool service to use
### and what parameters to use for the request

# Define the API endpoint for chatting with the RAILS app
@app.route("/agent", methods=["POST"])
def agent():
  # Get the message for the request
  prompt = request.json["prompt"]

  # Parse the input message to remove any unnecessary spaces

  # Determine the tool service to use

  # Run text classification and intent detection

  # Convert text to speech and cache the wav file

  # 

  # Use the chatbot to generate a response
  response = queue.enqueue(worker.generate, prompt)

  print(response)
  # Return the response
  return jsonify(response)

# Run the web server
if __name__ == "__main__":
  app.run()
