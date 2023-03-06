# Import necessary libraries
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
from pathlib import Path
import time
import torch
import soundfile as sf
import io
from scipy.io.wavfile import write

class TTS:
  def __init__(self) -> None:
    model_tag = "espnet/kan-bayashi_ljspeech_vits"
    vocoder_tag = None
    self.text2speech = Text2Speech.from_pretrained(
      model_tag=str_or_none(model_tag),
      device="cuda",
      # Only for Tacotron 2 & Transformer
      threshold=0.5,
      # Only for Tacotron 2
      minlenratio=0.0,
      maxlenratio=10.0,
      use_att_constraint=False,
      backward_window=1,
      forward_window=3,
      # Only for FastSpeech & FastSpeech2 & VITS
      speed_control_alpha=1.0,
      # Only for VITS
      noise_scale=0.667,
      noise_scale_dur=0.8,
    )

  def synthesizer(self, text, filename):
    # synthesis
    print(f"TTS: {text}")
    with torch.no_grad():
      start = time.time()
      wav = self.text2speech(text)["wav"]
    rtf = (time.time() - start) / (len(wav) / self.text2speech.fs)
    print(f"RTF = {rtf:5f}")
    # let us listen to generated samples
    sf.write(filename, wav.cpu().numpy(), self.text2speech.fs, "PCM_16")

    return filename

if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = TTS()
  # Call the speech function
  wav_bytes = tts.synthesizer("Hello, I am a text-to-speech system.", "hello.wav")
  print(len(wav_bytes))
