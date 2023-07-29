import redis
import time
from agentforge.interfaces import interface_interactor

def stream_string(channel_name, input_string, delay=0.2):
    redis_store = interface_interactor.create_redis_connection()

    # Tokenize the string into words
    words = input_string.split()

    # Iterate over the words
    for idx, word in enumerate(words):
        # Publish the word to the specified Redis channel
        redis_store.publish(channel_name, word)

        # If this is not the last word, publish a space
        if idx != len(words) - 1:
            redis_store.publish(channel_name, " ")

        # Wait for the specified delay before sending the next word
        time.sleep(delay)

    redis_store.publish(channel_name, "<|endoftext|>")
    redis_store.close()
