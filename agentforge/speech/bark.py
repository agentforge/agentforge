# Import necessary libraries
# from espnet2.bin.tts_inference import Text2Speech
# from espnet2.utils.types import str_or_none
import soundfile as sf
from bark import SAMPLE_RATE, generate_audio
from IPython.display import Audio
from .normalize import normalize_transcription
from scipy.io.wavfile import write as write_wav

class BarkTextToSpeech():
  def __init__(self) -> None:
    pass

  def synthesizer(self, text, filename, speaker_wav=None, speaker_idx=-1):
    if speaker_idx != -1:
      audio_array = generate_audio(text, history_prompt=f"en_speaker_{speaker_idx}")
    else:
      audio_array = generate_audio(text)
    write_wav(filename, SAMPLE_RATE, audio_array)
    return filename

if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = BarkTextToSpeech()
  # Call the speech function
  wav_bytes = tts.synthesizer("Hello, I am a text-to-speech system.", "hello.wav")
  print(len(wav_bytes))
