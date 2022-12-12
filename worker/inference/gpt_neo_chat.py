# Import necessary libraries
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForCausalLM
import re
from config import Config
from helpers import str_to_class

class GPT2Chatbot:
  def __init__(self):
    self._c = Config()
    # Load the GPT-2 model and tokenizer from the transformers library
    klass = str_to_class(self._c.config["gpt_model_klass"])
    self.model = klass.from_pretrained(self._c.config["gpt_model_cache"])
    self.tokenizer = AutoTokenizer.from_pretrained(self._c.config["tokenizer_cache"])

    # Initialize an empty list for storing the conversation history
    self.history = []

  def min_length(self, prompt):
    # Returns the optimal min_length for this model
    return len(prompt)+24
  
  def max_length(self, prompt):
    # Returns the optimal max_length for this model
    return len(prompt)+24

  def find_new_phrase(self, new_phrase, context):
    # Remove the context
    new_phrase = new_phrase.replace(context, "")
    # Split the strings into a list of strings separated by [human] and [robot]
    new_phrases = re.split('\[robot\]|\[human\]', new_phrase)
    new_phrases = filter(lambda x: not (x.isspace() or len(x) == 0), new_phrases)
    new_phrases = list(new_phrases)
    print(new_phrases)
    print(self.history)
    # Loop through the phrases in the new string
    for phrase in new_phrases:
      fixed = phrase.replace(":", "").strip()
      print(fixed)
      print(f"[robot]: {fixed}" not in self.history and f"[human]: {fixed}" not in self.history)
      # Check if the phrase exists in the previous string
      if f"[robot]: {fixed}" not in self.history and f"[human]: {fixed}" not in self.history:
        # Return the phrase if it is not in the previous string
        return fixed
    # Return None if no new phrase was found
    return None

  def generate_response(self, prompt):
    # Use the GPT-2 model to generate a response to the given prompt
    input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
    min_length = self.min_length(prompt)
    max_length = self.max_length(prompt)
    response = self.model.generate(input_ids=input_ids, do_sample=True, max_length=max_length, min_length=min_length, temperature=self._c.config["temperature"])

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

  def relevant_history(self):
    return self.history[-self._c.config["history_cache_stack"]:]

  def reset_history(self):
    self.history = []
    print(self.history)

  # Considers an input_str, a user supplied context, and 
  def handle_input(self, input_str, context):
    print("Processing...")
    print(f"input_str: {input_str}")
    print(f"context: {context}")
    # Preprocess the user input
    input_str = self.preprocess_input(input_str)

    # The default context forces the conversation into the POV of a chat
    default_context = self._c.config["default_context"]

    # Update the conversation history
    self.history.append(f"[human]: {input_str}")

    # Generate a response to the user input
    print(f"actual input: {context + '\n'.join(self.relevant_history()) + ' [robot]:'}")
    response = self.generate_response(default_context + " " + context + "\n".join(self.relevant_history()) + " [robot]:")
    print(f"eesponse: {response}")
    # response = self.generate_response(input_str)

    new_phrase = self.find_new_phrase(response, default_context  + " " +  context)

    # Update the conversation history
    self.history.append(f"[robot]: {new_phrase}")

    return new_phrase

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
  print(chatbot.generate_response("Hi there!", ""))
