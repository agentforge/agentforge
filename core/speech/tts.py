# Import necessary libraries
# from espnet2.bin.tts_inference import Text2Speech
# from espnet2.utils.types import str_or_none
import soundfile as sf
from TTS.api import TTS

class TextToSpeech():
  def __init__(self) -> None:
    # Init TTS
    # self.tts = TTS(model_name="tts_models/en/ek1/tacotron2", progress_bar=False, gpu=True)
    self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)


  def synthesizer(self, text, filename):
    # synthesis
    print(f"TTS: {text}")
    # with torch.no_grad():
    # start = time.time()
    # self.tts.tts_to_file(text=text, file_path=filename)
    self.tts.tts_to_file(text=text, file_path=filename, speaker_wav="/app/cache/voice.wav", language="en")

    # wav = self.text2speech(text)["wav"]
    # rtf = (time.time() - starts) / (len(wav) / self.text2speech.fs)
    # print(f"RTF = {rtf:5f}")
    # let us listen to generated samples
    # sf.write(filename, wav.cpu().numpy(), self.text2speech.fs, "PCM_16")
    return filename

if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = TTS()
  # Call the speech function
  wav_bytes = tts.synthesizer("Hello, I am a text-to-speech system.", "hello.wav")
  print(len(wav_bytes))
