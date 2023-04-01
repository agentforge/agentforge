from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from redis import Redis
from rq import Queue
import logging

from historica.agent import ExecutiveCognition
from historica.agent import startup
from historica.helpers import measure_time
from historica.worker import Worker
from historica.models import User
from historica import db

# Create the worker queue TODO: Complete implementation
queue = Queue(connection=Redis())
worker = Worker()

# Setup logging
#logging.basicConfig(filename='agent.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

# Setup database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/cache/test.db'
db.init_app(app)
migrate = Migrate(app, db)

# Setup Agent
executive = ExecutiveCognition()
startup()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.authenticate(username, password)
    if user:
        # If authentication is successful, return a token and a success response
        return jsonify({'message': 'Login successful', 'token': 'your_token'})
    else:
        # If authentication fails, return an error response
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.register(username, password)
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Define the API endpoint for prompting the language_model
@app.route("/v1/completions", methods=["POST"])
@measure_time
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]
  config = request.json["config"] if "config" in request.json else None

  # Run the LLM agent
  response = executive.respond(prompt, config)

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
  config = request.json["config"]
  
  # Run the agent
  response = executive.speak(prompt, config)
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
