from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from historica.config import Config

class Whisper:
  def __init__(self):
    # Initialize the AutoProcessor and AutoModelForSpeechSeq2Seq instances
    config = Config("config")
    self.processor = AutoProcessor.from_pretrained("openai/whisper-large")
    self.model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large")

  def interpret(self, wav_file_path):
    # Use the openai/whisper transformers API to interpret the wav file
    processed_data = self.processor(wav_file_path)
    output = self.model.generate(**processed_data, max_length=2048)

    # Return the text from the response
    return output[0]["generated_text"]