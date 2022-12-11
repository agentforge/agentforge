# Import necessary libraries
import requests
import os
import pytest

# Define the URL of the API
API_URL = "http://localhost:3000"

# Define the test data for the /tts endpoint
TTS_TEST_DATA = [
    {
        "text": "Hello, I am a text-to-speech system.",
        "filename": "hello.wav",
        "expected_output": "/app/hello.wav"
    },
    {
        "text": "This is a test of the text-to-speech system.",
        "filename": "test.wav",
        "expected_output": "/app/test.wav"
    }
]

# Define the test data for the /chat endpoint
CHAT_TEST_DATA = [
    {
        "message": "Hello, I am a human.",
        "context": "",
        "expected_output": "Hello, I am a robot. How can I help you?"
    },
    {
        "message": "I am feeling down.",
        "context": "Hello, I am a robot. How can I help you?",
        "expected_output": "I'm sorry to hear that. Is there anything specific that is causing you to feel this way?"
    }
]

# Define the test data for the /interpret endpoint
INTERPRET_TEST_DATA = [
    {
        "wav_file": "/path/to/file1.wav",
        "expected_output": "This is the text interpreted from file1.wav"
    },
    {
        "wav_file": "/path/to/file2.wav",
        "expected_output": "This is the text interpreted from file2.wav"
    }
]

# Test the /interpret endpoint
def test_interpret():
  for data in INTERPRET_TEST_DATA:
    # Make a POST request to the /interpret endpoint
    response = requests.post(f"{API_URL}/interpret", files={"wav_file": open(data["wav_file"], "rb")})

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains something
    assert len(response.json()["text"]) > 0

# Test the /tts endpoint
def test_tts():
  for data in TTS_TEST_DATA:
    # Make a POST request to the /tts endpoint
    response = requests.post(f"{API_URL}/tts", json=data)
    print(response)
    # Assert that the response status code is 200
    assert response.status_code == 200

     # Get the wav file from the response
    wav_file = response.content

    # Play the wav file using the os module
    os.system(f"play {wav_file}")

# Test the /chat endpoint
def test_chat():
  for data in CHAT_TEST_DATA:
    # Make a POST request to the /chat endpoint
    response = requests.post(f"{API_URL}/chat", json=data)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains something
    assert len(response.json()["response"]) > 0

# Run the tests
if __name__ == "__main__":
  test_tts()
  test_chat()
  test_interpret()
