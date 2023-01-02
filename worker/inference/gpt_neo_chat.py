# Import necessary libraries
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForCausalLM, GPTJForCausalLM
import re
import torch
from .history import History
from config import Config
from helpers import str_to_class

class GPT2Chatbot:
  def __init__(self):
    self._c = Config()
    # Load the GPT-2 model and tokenizer from the transformers library
    klass = str_to_class(self._c.config["gpt_model_klass"])
    # self.model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", revision="float16", torch_dtype=torch.float16, low_cpu_mem_usage=True)
    self.model = klass.from_pretrained(self._c.config["gpt_model_cache"])
    self.tokenizer = AutoTokenizer.from_pretrained(self._c.config["tokenizer_cache"])

    # The default context forces the conversation into the POV of a chat
    self.default_context = self._c.config["default_context"]

    # Initialize an empty list for storing the conversation history
    self.history = History()

  def min_length(self, prompt):
    # Returns the optimal min_length for this model
    return len(prompt)
  
  def max_length(self, prompt):
    # Returns the optimal max_length for this model
    return len(prompt)+20

  def preprocess_input(self, input_str):
    # Use regular expressions to remove any leading or trailing whitespace
    input_str = re.sub(r"^\s+|\s+$", "", input_str)

    # Use regular expressions to replace any consecutive whitespace characters with a single space
    input_str = re.sub(r"\s+", " ", input_str)

    return input_str

  # Considers an input_str, a user supplied context, and name
  def handle_input(self, input_str, opts):
    self.context = opts["context"]
    self.name = opts["name"]
    # Default name helps
    if self.name == "": 
      self.name = "human"
    print("Processing...")
    print(f"input_str: {input_str}")
    print(f"context: {self.context}")
    # Preprocess the user input
    input_str = self.preprocess_input(input_str)

    # Update the conversation history
    self.history.append(f"[{self.name}]: {input_str}")

    # Generate a response to the user input
    hist = self.history.relevant_history(self._c.config['history_cache_stack'])
    print(f"actual input: {self.default_context + ' ' + self.context + ' '.join(hist) + ' [robot]:'}")

    # Use the GPT-2 model to generate a response to the given prompt
    prompt = self.default_context + " " + self.context + " " + "\n".join(hist) + " [robot]:"
    input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
    min_length = self.min_length(prompt)
    max_length = self.max_length(prompt)
    response = self.model.generate(input_ids=input_ids, do_sample=True, max_length=max_length, min_length=min_length, temperature=self._c.config["temperature"])

    # Extract the generated text from the response
    generated_text = self.tokenizer.decode(response[0])

    # Use regular expressions to remove any leading or trailing whitespace
    generated_text = re.sub(r"^\s+|\s+$", "", generated_text)

    total_context = self.default_context  + " " +  self.context
    new_phrase = self.history.find_new_phrase(generated_text, total_context, self.name)

    # Update the conversation history
    self.history.append(f"[robot]: {new_phrase}")

    return new_phrase

# TODO: Start a conversation if the module is run directly
if __name__ == "__main__":
  pass