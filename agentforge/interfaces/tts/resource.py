# Import necessary libraries
# from espnet2.bin.tts_inference import Text2Speech
# from espnet2.utils.types import str_or_none
import soundfile as sf
from agentforge.utils import normalize_transcription, dynamic_import

class TextToSpeech():
  def __init__(self) -> None:
    module = dynamic_import('TTS.api', ['TTS'])
    TTS = module["TTS"]
    # Init TTS
    self.tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=True)
    self.tts_custom = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)

  def synthesizer(self, text, filename, speaker_wav=None, speaker_idx=0):
    if speaker_wav is not None:
      self.tts_custom.tts_to_file(text=normalize_transcription(text), file_path=filename, speaker_wav=speaker_wav, language="en")
    else:
      if speaker_idx is None:
        speaker_idx = 0
      self.tts.tts_to_file(text=text, speaker=self.tts.speakers[speaker_idx], file_path=filename)
    return filename

if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = TextToSpeech()
  # Call the speech function
  wav_bytes = tts.synthesizer("Hello, I am a text-to-speech system.", "hello.wav")
  print(len(wav_bytes))
