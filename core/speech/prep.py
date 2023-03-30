import os, re
import soundfile as sf
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import yt_dlp
import glob
import librosa
import numpy as np
import subprocess
import torch
from transformers import pipeline
from datasets import load_dataset
from pydub import AudioSegment, silence
from datetime import datetime

# Install the required libraries
# !pip install youtube_dl
# !pip install pydub
# !pip install SpeechRecognition

def split_wav_into_sentences(folder_path, output_folder, silence_thresh=-40, min_silence_len=500):
    wav_files = glob.glob(os.path.join(folder_path, '*.wav'))

    for wav_file in wav_files:
        audio = AudioSegment.from_wav(wav_file)
        # volume = audio.dBFS
        sentences = silence.split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

        base_filename = os.path.splitext(os.path.basename(wav_file))[0]
        for i, sentence in enumerate(sentences):
            output_path = os.path.join(output_folder, f"{base_filename}_sentence_{i}.wav")
            sentence.export(output_path, format="wav")

def convert_wavs_to_16k_sample_rate(ouput_dir, folder_path):
    os.makedirs(ouput_dir, exist_ok=True)

    wav_files = glob.glob(os.path.join(folder_path, '*.wav'))
    
    for wav_file in wav_files:
        audio = AudioSegment.from_wav(wav_file)
        audio_16k = audio.set_frame_rate(16000)
        output_path = os.path.join(ouput_dir, os.path.splitext(os.path.basename(wav_file))[0] + ".wav")
        audio_16k.export(output_path, format="wav")

def convert_mp3s(folder_path):
    input_folder = folder_path
    output_folder = folder_path

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Find all MP3 files in the input folder
    mp3_files = glob.glob(os.path.join(input_folder, '*.mp3'))

    # Convert each MP3 file to WAV format with a sample rate of 16,000 Hz
    for mp3_file in mp3_files:
        # Load the MP3 file and resample to 16,000 Hz
        audio, _ = librosa.load(mp3_file, sr=16000, mono=True)

        # Create an output file path with the same name but with a WAV extension
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(mp3_file))[0] + '.wav')

        # Save the audio to the output WAV file
        sf.write(output_file, audio, samplerate=16000)

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

def transcribe_audio(pipe, audio_file_path):
    sample_rate = 16000
    audio, _ = librosa.load(audio_file_path, sr=sample_rate, mono=True)

    # Convert the audio numpy array to a dataset format
    audio_dataset = {
        "array": audio,
        "sampling_rate": sample_rate,
    }

    # Get the prediction
    prediction = pipe(audio_dataset.copy())["text"]

    return prediction

def download_youtube_videos(output_dir, youtube_urls):
    for url in youtube_urls:
        id = url.split("watch?v=")[1]
        output_path = id
        download_youtube_audio(url, output_path)

def process_videos(pipe, local_wav_folders):
    idx = 0
    all_transcriptions = []
    for local_wav_files in local_wav_folders:
        wav_files = glob.glob(os.path.join(local_wav_files, '*.wav'))
        for wav_file in wav_files:
            audio = AudioSegment.from_wav(wav_file)
            duration_seconds = len(audio) / 1000

            if duration_seconds > 20:
                print(f"Skipping file {wav_file} due to duration > 20 seconds")
                continue

            idx += 1
            print(f"Iteration: {idx}")
            transcription = transcribe_audio(pipe, wav_file)
            all_transcriptions.append((wav_file, transcription))
    return all_transcriptions

if __name__ == '__main__':
    from normalize import normalize_transcription

    def normalize_transcriptions(transcriptions):
        return [(file_name, transcription, normalize_transcription(transcription)) for file_name, transcription in transcriptions]

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium.en",
        chunk_length_s=30,
        device=device,
    )

    # List of YouTube video URLs
    youtube_urls = [
        'https://www.youtube.com/watch?v=lzisVv4bzms',
    ]

    #   download_youtube_videos("/app/cache/audio/fdr/", youtube_urls)

    #   convert_mp3s("/app/cache/audio/fdr/")

    local_wav_files = [
        "/app/cache/audio/fdr/",
    ]

    os.makedirs("/app/cache/audio/fdr/split/", exist_ok=True)

    split_wav_into_sentences("/app/cache/audio/fdr/", "/app/cache/audio/fdr/split/")

    transcriptions = process_videos(pipe, ["/app/cache/audio/fdr/split/"])

    convert_wavs_to_16k_sample_rate("/app/cache/audio/fdr/16k/", "/app/cache/audio/fdr/split/")

    # Normalize the transcriptions
    normalized_transcriptions = normalize_transcriptions(transcriptions)

    # Format the text into LJ Speech Dataset format and save to transcripts.csv
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(" ", "_").replace(":", "_")
    filename = f"transcripts-{timestamp}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        for file_name, transcription, normalized_transcription in normalized_transcriptions:
            metadata = f"{file_name.replace('.wav', '')}|{transcription}|{normalized_transcription}\n"
            f.write(metadata)

    print("Metadata saved to transcripts.csv")
