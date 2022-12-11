import requests
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
QUERY = """
This is a discussion between a [human] and a [robot]. 
The [robot] is very nice and empathetic.

[human]: Hello nice to meet you.
[robot]: Nice to meet you too.
###
[human]: How is it going today?
[robot]: Not so bad, thank you! How about you?
###
[human]: I am ok, but I am a bit sad...
[robot]: Oh? Why that?
###
[human]: I broke up with my girlfriend...
[robot]: 
"""
headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
output = query({"inputs": QUERY})