# Import necessary libraries
# from espnet2.bin.tts_inference import Text2Speech
# from espnet2.utils.types import str_or_none
import soundfile as sf
from TTS.api import TTS
from core.helpers.helpers import convert_numbers_in_sentence, process_date_terms, process_date_sentence

class TextToSpeech():
  def __init__(self) -> None:
    # Init TTS
    self.tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=True)
    # self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)

  # Some parsing is really only appropriate for the TTS so we do it here
  def parse_for_tts(self, text) -> None:
    print(text)
    text = process_date_sentence(text)
    print(text)
    text = process_date_terms(text)
    print(text)
    return convert_numbers_in_sentence(text)

  def synthesizer(self, text, filename, speaker_wav="/app/cache/audio/voice.wav", speaker_idx=0):
    # synthesis
    print(f"TTS: {text}")
    # with torch.no_grad():
    # start = time.time()
    self.tts.tts_to_file(text=text, speaker=self.tts.speakers[speaker_idx], file_path=filename)
    # self.tts.tts_to_file(text=self.parse_for_tts(text), file_path=filename, speaker_wav=speaker_wav, language="en")

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
