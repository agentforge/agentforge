import os, re
import soundfile as sf
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import yt_dlp
import glob
import librosa
import numpy as np
import subprocess

# Install the required libraries
# !pip install youtube_dl
# !pip install pydub
# !pip install SpeechRecognition

def download_youtube_videos(url_list):
    for url in url_list:
        download_youtube_video(url)

def download_youtube_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(audio_input: str) -> str:
    audio_file = "temp_converted_audio.wav"
    subprocess.run(["ffmpeg", "-y", "-i", audio_input, "-ar", "16000", audio_file])
    
    # Load the converted file
    speech_array, sample_rate = sf.read(audio_file)

    # # Convert stereo audio to mono by averaging the channels
    # if speech_array.ndim > 1 and speech_array.shape[1] == 2:
    #     speech_array = np.mean(speech_array, axis=1)

    # Print the shape of the audio array for debugging
    print(f"Speech array shape: {speech_array.shape}")
    # Load model and processor
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")
    model.config.forced_decoder_ids = None

    # Load the audio file
    audio, sample_rate = librosa.load(audio_file, sr=None)

    # Add a new axis to the audio array to make it 2D
    # audio_input = np.expand_dims(audio, axis=0)

    # Process the audio input
    input_features = processor(audio, sampling_rate=sample_rate, return_tensors="pt").input_features

    # Generate token ids
    predicted_ids = model.generate(input_features)

    # Decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription[0]

def process_videos(youtube_urls, local_wav_files):
    all_transcriptions = []

    for url in youtube_urls:
        id = url.split("watch?v=")[1]
        output_path = id
        download_youtube_audio(url, output_path)
        transcription = transcribe_audio(output_path + ".wav")
        all_transcriptions.append((id + ".wav", transcription))
        # os.remove(output_path + ".wav")

    for wav_file in local_wav_files:
        transcription = transcribe_audio(wav_file)
        all_transcriptions.append((wav_file, transcription))

    return all_transcriptions

if __name__ == '__main__':
  from normalize import normalize_transcription

  def normalize_transcriptions(transcriptions):
      return [(file_name, transcription, normalize_transcription(transcription)) for file_name, transcription in transcriptions]

  # List of YouTube video URLs
  youtube_urls = [
      'https://www.youtube.com/watch?v=lzisVv4bzms',
  ]

  local_wav_files = [
      # "path/to/your/local/audio1.wav",
      # "path/to/your/local/audio2.wav",
  ]

  transcriptions = process_videos(youtube_urls, local_wav_files)

  # Normalize the transcriptions
  normalized_transcriptions = normalize_transcriptions(transcriptions)

  # Format the text into LJ Speech Dataset format and save to transcripts.csv
  with open("transcripts.csv", "w", encoding="utf-8") as f:
      for file_name, transcription, normalized_transcription in normalized_transcriptions:
          metadata = f"{file_name}|{transcription}|{normalized_transcription}\n"
          f.write(metadata)

  print("Metadata saved to transcripts.csv")
