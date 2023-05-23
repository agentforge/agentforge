from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, jsonify, send_file, render_template, Response, make_response
from flask_cors import CORS
from flask_sse import sse
from redis import Redis
from rq import Queue
import redis, uuid
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename

# # importing the sys module
import sys, os
 
# # appending the directory of mod.py
# # in the sys.path list
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'/app/agentforge'))
print(sys.path)

from agentforge import DST_PATH
from agentforge.ai import ExecutiveCognition
# from agentforge.agent import startup
from agentforge.utils import measure_time
from agentforge.ai import User
from agentforge import db
from agentforge.utils import secure_wav_filename
import agentforge as af

# Create the worker queue TODO: Complete implementation
# queue = Queue(connection=Redis())
# worker = Worker()

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": af.ALLOWED_ORIGIN}})

# Setup database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DST_PATH}/test.db"
app.config['SESSION_TYPE'] = af.SESSION_TYPE
app.config["REDIS_URL"] = f"redis://{af.REDIS_HOST}:{af.REDIS_PORT}/{af.REDIS_DB}"

# Set the ALLOWED_ORIGIN and ALLOW_CREDENTIALS configuration variables
app.config["ALLOWED_ORIGIN"] = af.ALLOWED_ORIGIN
app.config["ALLOW_CREDENTIALS"] = af.ALLOW_CREDENTIALS

app.secret_key = af.AGENT_SECRET_KEY

app.register_blueprint(sse, url_prefix='/stream')

db.init_app(app)
migrate = Migrate(app, db)

# Setup redis connection
redis_conn = redis.StrictRedis(host=af.REDIS_HOST, port=af.REDIS_PORT, db=af.REDIS_DB)

# Setup Agent
executive = ExecutiveCognition()

# TODO: Ensure video fidelity by pointing video src to a central filestore
# startup()

# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "agentforge Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# def sse_stream_with_cors():
#     response = Response(sse.stream(), content_type='text/event-stream')
#     response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Cache-Control'] = 'no-cache'
#     return response

# app.view_functions['sse.stream'] = sse_stream_with_cors

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
    user = User.query.get(int(user_id)) 
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
        try:
            config = user.set_config(data["config"])
            return jsonify(config)
        except Exception as e:
            return jsonify({'message': str(e)}), 400

@app.route("/v1/whisper", methods=["POST"])
def whisper_api():
    # Save the uploaded wav file
    audio_file = request.files["audio"]

    wav_file_path = secure_wav_filename(audio_file.filename)
    audio_file.save(AUDIO_DST_PATH + "/" + wav_file_path)

    # Interpret the audio using the Whisper class
    generated_text = executive.interpret({"file": AUDIO_DST_PATH + "/" + wav_file_path, "type": "wav"})

    # Return the generated text
    return {"generated_text": generated_text}

# Define the API endpoint for prompting the language_model
@app.route("/v1/completions", methods=["POST"])
@measure_time
def prompt():
  # Get the message for the request
  prompt = request.json["prompt"]
  form_data = request.json
  # Run the LLM agent
  response = executive.respond(prompt, form_data, app)
  # Return the response
  return jsonify(response)

# TODO: DEPRECATE THIS
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

  return response_obj

# TODO Replace this with the ModelConfig API
# @app.route("/v1/avatars", methods=["GET"])
# def avatars():

#   # Get the avatars currently loaded into the config
#   response = executive.avatar.get_avatars()

#   # Create a response object with the avatars
#   return jsonify(response)

# TODO Replace this with the ModelConfig API

# @app.route("/v1/llm_models", methods=["GET"])
# def llm_models():

#   # Get the avatars currently loaded into the config
#   response = executive.service.get_llm_models()

#   # Create a response object with the avatars
#   return jsonify(response)
