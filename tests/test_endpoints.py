# Import necessary libraries
import requests
import os
import pytest
from httpx import AsyncClient
from main import app

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

# Test the /reset_history endpoint
def test_reset():
    # Make a POST request to the /reset_history endpoint
    response = requests.post(f"{API_URL}/reset_history")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains True
    assert len(response.json()["success"]) == True

@pytest.fixture
def client():
    return AsyncClient(app=app, base_url=API_URL)

async def test_create_schedule(client):
    response = await client.post(
        "/v1/create-schedule",
        json={"event_name": "Test Event", "interval": 60},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "id" in data

async def test_create_schedule_invalid_input(client):
    response = await client.post("/v1/create-schedule", json={})
    assert response.status_code == 400

async def test_delete_schedule(client):
    # Create a schedule to test deletion
    create_response = await client.post(
        "/v1/create-schedule",
        json={"event_name": "Test Event", "interval": 60},
    )
    schedule_id = create_response.json()["id"]

    # test deletion
    response = await client.delete(f"/v1/delete-schedule/{schedule_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

async def test_delete_schedule_invalid_id(client):
    response = await client.delete("/v1/delete-schedule/invalid_id")
    assert response.status_code == 422

async def test_delete_schedule_not_found(client):
    response = await client.delete("/v1/delete-schedule/6064aef63d6b67669e836912")
    assert response.status_code == 404

async def test_view_schedule(client):
    response = await client.get("/v1/view-schedule")
    assert response.status_code == 200
    data = response.json()
    assert "schedules" in data

async def test_update_schedule(client):
    # Create a schedule to test updating
    create_response = await client.post(
        "/v1/create-schedule",
        json={"event_name": "Test Event", "interval": 60},
    )
    schedule_id = create_response.json()["id"]

    # test updating
    response = await client.put(
        f"/v1/update-schedule/{schedule_id}",
        json={"interval": 120, "validation_logic": "updated_logic"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

async def test_update_schedule_invalid_id(client):
    response = await client.put("/v1/update-schedule/invalid_id", json={})
    assert response.status_code == 422

async def test_update_schedule_not_found(client):
    response = await client.put(
        "/v1/update-schedule/6064aef63d6b67669e836912",
        json={"interval": 120},
    )
    assert response.status_code == 404

async def test_subscribe_schedule(client):
    response = await client.post("/v1/subscribe-schedule")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

async def test_unsubscribe_schedule(client):
    response = await client.post("/v1/unsubscribe-schedule")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_subscribe_notifications():
    # Test when all required fields are present
    response = client.post("/v1/subscribe-notifications", json={"endpoint": "test-endpoint", "keys": {"p256dh": "test-p256dh", "auth": "test-auth"}})
    assert response.status_code == 201

    # Test when request is missing required fields
    response = client.post("/v1/subscribe-notifications", json={})
    assert response.status_code == 400

def test_unsubscribe_notifications():
    # Test when subscription exists
    response = client.post("/v1/unsubscribe-notifications", json={"endpoint": "test-endpoint"})
    assert response.status_code == 200

    # Test when subscription does not exist
    response = client.post("/v1/unsubscribe-notifications", json={"endpoint": "nonexistent-endpoint"})
    assert response.status_code == 404

    # Test when request is missing required fields
    response = client.post("/v1/unsubscribe-notifications", json={})
    assert response.status_code == 400

# Run the tests
if __name__ == "__main__":
  test_tts()
  test_chat()
  test_interpret()
  test_reset()
  test_create_schedule()
  test_create_schedule_invalid_input()
  test_delete_schedule()
  test_delete_schedule_invalid_id()
  test_delete_schedule_not_found()
  test_view_schedule()
  test_update_schedule()
  test_update_schedule_invalid_id()
  test_update_schedule_not_found()
  test_subscribe_schedule()
  test_unsubscribe_schedule()
  test_subscribe_notifications()
  test_unsubscribe_notifications()



