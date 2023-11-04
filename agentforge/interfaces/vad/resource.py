import io, torch
from pydub import AudioSegment
from typing import List
import torchaudio
import soundfile as sf
import io
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
from agentforge.utils import logger
import numpy as np

processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

# Load Silero model and utilities
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

def is_valid_webm(data: bytes) -> bool:
    # The magic number for Matroska file format (which includes WebM)
    matroska_magic_number = b'\x1A\x45\xDF\xA3'
    return data.startswith(matroska_magic_number)

async def process_chunk(chunk: bytes):
    print(len(chunk))
    if is_valid_webm(chunk):
        logger.info("Valid WebM data")
    else:
        logger.info("Invalid WebM data")
        return

    # Convert audio_bytes from WebM to WAV
    audio_webm = AudioSegment.from_file(io.BytesIO(chunk), format="webm")
    buffer = io.BytesIO()
    audio_webm.export(buffer, format="wav")
    buffer.seek(0)
    
    # Now load the WAV data
    wav, sr = torchaudio.load(buffer)
    
    # Assuming your model expects audio data with a sample rate of 16000 Hz,
    # resample the audio data if necessary
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
        wav = resampler(wav)
        sr = 16000

    # Now proceed with processing the audio data
    speech_probs = []
    window_size_samples = 512  # Adjust as necessary for your model
    for i in range(0, wav.size(1), window_size_samples):
        chunk = wav[:, i:i+window_size_samples]
        if chunk.size(1) < window_size_samples:
            break
        speech_prob = model(chunk, sr).item()
        speech_probs.append(speech_prob)
    
    model.reset_states()  # Reset model states after each audio

    # If voice detected
    if any(prob > 0.9 for prob in speech_probs):  # Threshold can be adjusted
        # Forward to Whisper for transcription
        wav = wav.squeeze(0)  # Squeeze the tensor to remove the first dimension
        input_features = processor(wav, sampling_rate=16000, return_tensors="pt").input_features
        predicted_ids = whisper_model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

        print(f"SPEECH DETECTED {transcription}")
        return transcription[0]
    return ""
