# Import necessary libraries
from flask import Flask, request, jsonify, send_file, Response
# from inference.gpt_neo_chat import GPTChatbot
from inference.langchain_bot import GPTChatbot
from speech.speech import TTS
from speech.whisper import Whisper
import io
import torch
from flask_cors import CORS

import logging
logging.basicConfig(filename='gpt.log', level=logging.DEBUG)

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

# Create an instance of the GPTChatbot class
chatbot = GPTChatbot()
tts_pipeline = TTS()

# Create a Whisper instance
whisper = Whisper()

print("CUDA AVAILABLE: ", torch.cuda.is_available())

# Define the API endpoint for generating a wav file from text
@app.route("/tts", methods=["POST"])
def tts():
  # Get the text and filename from the request
  text = request.json["text"]
  filename = "out.wav"

  # Use the gTTS library to generate a wav file from the given text
  # Call the speech function
  filename = tts_pipeline.synthesizer(text, filename)

  # Return the wav file in the response
  print(filename)
  return send_file(
    filename,
    mimetype="audio/wav",
  )

# Define the API endpoint for chatting with the prompts-ai (openAPI mimic)
@app.route("/completions", methods=["POST"])
def completions():
  # Get the message and context from the request
  message = request.json["prompt"]

  # Use the chatbot to generate a response
  response = chatbot.simple_input(message)

  print(response)
  # Return the response
  return jsonify({"choices": [{"text":response}]})

# Define the API endpoint for chatting with the RAILS app
@app.route("/chat", methods=["POST"])
def chat():
  # Get the message and context from the request
  message = request.json["message"]
  context = request.json["context"]
  robot_name = request.json["robot_name"]
  name = request.json["name"]

  opts = {"name": name, "context": context, "robot_name": robot_name, "app": app}

  # Use the chatbot to generate a response
  response = chatbot.handle_input(message, opts)

  print(response)
  # Return the response
  return jsonify(response)

# Define the API endpoint for chatting with the chatbot
@app.route("/reset_history", methods=["POST"])
def reset_history():
  # Reset the history of the chatbot
  chatbot.reset_history()
  # Return the response
  return jsonify({"success": True})

# Define the /interpret endpoint
@app.route("/interpret", methods=["POST"])
def interpret():
  # Get the wav file from the request
  wav_file = request.files["wav_file"]

  # Interpret the wav file
  text = whisper.interpret(wav_file)

  # Return the text in the response
  return jsonify({"text": text})

# Run the web server
if __name__ == "__main__":
  app.run()
