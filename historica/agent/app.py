from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from redis import Redis
from rq import Queue
import logging, redis, uuid
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint

from historica.agent import ExecutiveCognition
from historica.agent import startup
from historica.helpers import measure_time
from historica.worker import Worker
from historica.models import User
from historica import db

# Create the worker queue TODO: Complete implementation
# queue = Queue(connection=Redis())
# worker = Worker()

# Setup logging
#logging.basicConfig(filename='agent.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/v1/*": {"origins": "*"}})

# Setup database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/cache/test.db'
app.secret_key = '0e529d8e-31b9-4e54-a63f-55d6b76e6d14'
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)
migrate = Migrate(app, db)

# Setup redis connection
redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)

# Setup Agent
executive = ExecutiveCognition()
startup()

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Historica Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.authenticate(username, password)
    if user:
        # Generate a UUID token
        token = uuid.uuid4().hex

        # Store the token in Redis with a max life of 1 day
        redis_conn.set(token, user.id, ex=timedelta(days=1))

        # Return the token and a success response
        return jsonify({'message': 'Login successful', 'token': token})
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

@app.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    token = token.split(' ')[1]  # Remove the 'Bearer' prefix from the token
    user_id = redis_conn.get(token)
    if user_id:
        User.logout(user_id)
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "User ID is missing"}), 400

@app.route('/v1/configure', methods=['POST', 'GET'])
def configure():
    ## Verify auth
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    token = token.split(' ')[1]
    user_id = redis_conn.get(token)
    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401
    print(user_id)
    user = User.query.get(int(user_id)) 
    print(user)
    ## For GET requests get the configuration
    if request.method == 'GET':
        try:
            config = user.get_config()
            return jsonify(config)
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    ## For POST requests set the configuration
    if request.method == 'POST':
        data = request.json
        print(data["config"])
        try:
            config = user.set_config(data["config"])
            return jsonify(config)
        except Exception as e:
            return jsonify({'message': str(e)}), 400

# Define the API endpoint for prompting the language_model
@app.route("/v1/completions", methods=["POST"])
@measure_time
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]
  form_data = request.json

  # Run the LLM agent
  response = executive.respond(prompt, form_data)

  print(response)
  # Return the response
  return jsonify(response)

# Define the API endpoint for hearing the agent speak
@app.route("/v1/tts", methods=["POST"])
@measure_time
def tts():
  # Get the message for the request
  prompt = request.json["prompt"]
  form_data = request.json

  # Run the agent
  response = executive.speak(prompt, form_data)
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
