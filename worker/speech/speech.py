# Import necessary libraries
from gtts import gTTS
from pathlib import Path

class TTS:
  def speech(self, text, filename):
    # Use the gTTS library to generate a wav file from the given text
    tts = gTTS(text=text, lang="en")

    # Save the wav file to the filesystem
    tts.save(filename)

    # Print a success message
    print(f"Successfully generated wav file at {Path(filename).resolve()}")

    # Return the path to the generated wav file
    return Path(filename).resolve()


if __name__ == "__main__":
  # Create an instance of the TTS class
  tts = TTS()
  # Call the speech function
  tts.speech("Hello, I am a text-to-speech system.", "hello.wav")