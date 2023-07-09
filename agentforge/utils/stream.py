import redis
import time
from agentforge.interfaces import interface_interactor

### Simulates streaming a hard-coded response
def stream_string(channel_name, input_string, delay=0.05):
    redis_store = interface_interactor.create_redis_connection()

    # Tokenize the string into words
    words = input_string.split()

    # Iterate over the words
    for word in words:
        # Publish each word to the specified Redis channel
        redis_store.publish(channel_name, word)

        # Wait for the specified delay before sending the next word
        time.sleep(delay)

    redis_store.close()