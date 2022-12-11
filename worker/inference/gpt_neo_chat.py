# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
from config import Config

class GPT2Chatbot:
  def __init__(self):
    self._c = Config()
    # Load the GPT-2 model and tokenizer from the transformers library
    self.model = AutoModelForCausalLM.from_pretrained(self._c.config["gpt_model_cache"])
    self.tokenizer = AutoTokenizer.from_pretrained(self._c.config["tokenizer_cache"])

    # Initialize an empty list for storing the conversation history
    self.history = []

  def generate_response(self, prompt, temperature=0.5):

    # Use the GPT-2 model to generate a response to the given prompt
    input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
    response = self.model.generate(input_ids=input_ids, max_length=self._c.config["max_length"], temperature=temperature)

    # Extract the generated text from the response
    generated_text = self.tokenizer.decode(response[0])

    # Use regular expressions to remove any leading or trailing whitespace
    generated_text = re.sub(r"^\s+|\s+$", "", generated_text)

    return generated_text

  def preprocess_input(self, input_str):
    # Use regular expressions to remove any leading or trailing whitespace
    input_str = re.sub(r"^\s+|\s+$", "", input_str)

    # Use regular expressions to replace any consecutive whitespace characters with a single space
    input_str = re.sub(r"\s+", " ", input_str)

    return input_str

  def handle_input(self, input_str, context):
    # Preprocess the user input
    input_str = self.preprocess_input(input_str)

    # Update the conversation history
    self.history.append(f"[human]: {input_str}")

    # Generate a response to the user input
    # response = self.generate_response("\n".join(self.history))
    response = self.generate_response(input_str)

    # Update the conversation history
    self.history.append(f"[robot]: {response}")

    return response

  def start_conversation(self):
    # Print a greeting message
    print("Hello! I am a chatbot trained on the GPT-2 model. I am very nice and empathetic. To start a conversation, simply type a message and press enter.")

    # Continuously get user input and generate responses until the user types "goodbye"
    while True:
      # Get user input
      input_str = input(">> User: ")

      # Check if the user wants to end the conversation
      if input_str.lower() == "goodbye":
        print("Goodbye! It was nice talking with you.")
        break

      # Otherwise, generate a response and print it
      response = self.handle_input(input_str)
      print(response)

# Start a conversation if the module is run directly
if __name__ == "__main__":
  chatbot = GPT2Chatbot()
  chatbot.start_conversation()
