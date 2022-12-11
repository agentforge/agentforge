# Import necessary libraries
from flask import Flask, request, jsonify, send_file
from inference.gpt_neo_chat import GPT2Chatbot
from speech.speech import TTS
from speech.whisper import Whisper
import io


# Create an instance of the Flask class
app = Flask(__name__)

# Create an instance of the GPT2Chatbot class
chatbot = GPT2Chatbot()
tts_pipeline = TTS()

# Create a Whisper instance
whisper = Whisper()


# Define the API endpoint for generating a wav file from text
@app.route("/tts", methods=["POST"])
def tts():
  # Get the text and filename from the request
  text = request.json["text"]
  filename = request.json["filename"]

  # Use the gTTS library to generate a wav file from the given text
  # Call the speech function
  wav_file = tts_pipeline.speech("Hello, I am a text-to-speech system.", "speech.wav")
  
  with open(wav_file, "rb") as f:
    wav_data = f.read()

  # Return the wav file in the response
  return send_file(
    io.BytesIO(wav_data),
    mimetype="audio/wav",
    attachment_filename="speech.wav"
  )

# Define the API endpoint for chatting with the chatbot
@app.route("/chat", methods=["POST"])
def chat():
  # Get the message and context from the request
  message = request.json["message"]
  context = request.json["context"]

  # Use the chatbot to generate a response
  response = chatbot.handle_input(message, context)

  # Return the response
  return jsonify({"response": response})

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