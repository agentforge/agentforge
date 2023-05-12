from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from agentforge.config import Config
import torchaudio
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from transformers import WhisperProcessor, WhisperForConditionalGeneration

class Whisper:
  def __init__(self):
    # Initialize the AutoProcessor and AutoModelForSpeechSeq2Seq instances
    # config = Config("config")
    # self.processor = AutoProcessor.from_pretrained("openai/whisper-large")
    # self.model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large")

    # Load the pre-trained Whisper model and processor
    self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")
    self.processor = WhisperProcessor.from_pretrained("openai/whisper-large")
    self.model.config.forced_decoder_ids = None
    if torch.cuda.is_available():    
      self.model = self.model.to("cuda")

  def interpret(self, wav_file_path):
    # Use the openai/whisper transformers API to interpret the wav file
    # processed_data = self.processor(wav_file_path)
    # print(processed_data)
    # output = self.model.generate(**processed_data, max_length=2048)
    # print(output)

    # # Return the text from the response
    # return output[0]["generated_text"]

    # Load the local .wav file
    print(wav_file_path)
    audio_input, sample_rate = torchaudio.load(wav_file_path)

    # # Resample the audio to the required sample rate (16kHz)
    # if sample_rate != 16000:
    #     resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
    #     audio_input = resampler(audio_input)

    # Process the audio input
    input_features = self.processor(audio_input[0].numpy(), return_tensors="pt", sampling_rate=16000).input_features

    if torch.cuda.is_available():
      input_features = input_features.to("cuda")

    # Perform the transcription
    predicted_ids = self.model.generate(input_features)

    # Decode the transcription
    transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
    # transcription = self.processor.decode(predicted_ids[0])

    return transcription
