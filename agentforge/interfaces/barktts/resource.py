# Import necessary libraries
# from espnet2.bin.tts_inference import Text2Speech
# from espnet2.utils.types import str_or_none
import soundfile as sf
from agentforge.utils import dynamic_import
from scipy.io.wavfile import write as write_wav

class BarkTextToSpeech():
  def __init__(self) -> None:
    self.module = dynamic_import('bark', ['SAMPLE_RATE', 'generate_audio'])
    self.generate_audio = self.module.generate_audio
    self.SAMPLE_RATE = self.module.SAMPLE_RATE

  def synthesizer(self, text, filename, speaker_wav=None, speaker_idx=-1):
    if speaker_idx != -1:
      audio_array = self.generate_audio(text, history_prompt=f"en_speaker_{speaker_idx}")
    else:
      audio_array = self.generate_audio(text)
    write_wav(filename, self.SAMPLE_RATE, audio_array)
    return filename

if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = BarkTextToSpeech()
  # Call the speech function
  wav_bytes = tts.synthesizer("Hello, I am a text-to-speech system.", "hello.wav")
  print(len(wav_bytes))
