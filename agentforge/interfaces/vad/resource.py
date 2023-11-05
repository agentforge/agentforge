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

class VadWhisper:
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
        self.whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

        # Load Silero model and utilities
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
        (self.get_speech_timestamps, self.save_audio, self.read_audio, self.VADIterator, self.collect_chunks) = utils

        self.webm_init_data = None

    def is_valid_webm(self, data: bytes) -> bool:
        matroska_magic_number = b'\x1A\x45\xDF\xA3'
        return data.startswith(matroska_magic_number)

    def extract_initialization_data(self, webm_data: bytes) -> bytes:
        cluster_id = b'\x1F\x43\xB6\x75'
        idx = webm_data.find(cluster_id)
        if idx == -1:
            raise ValueError('Cluster ID not found')
        return webm_data[:idx]

    async def process_chunk(self, chunk: bytes) -> str:
        # message = ""
        # if self.webm_init_data is None:
        #     try:
        #         self.webm_init_data = self.extract_initialization_data(chunk)
        #     except ValueError as e:
        #         return str(e)
        message += f"Chunk length: {len(chunk)}\n"
        if self.is_valid_webm(chunk):
            message += "Valid WebM data"
        else:
            message += "Invalid WebM data"
        
        logger.info(message)

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
            speech_prob = self.model(chunk, sr).item()
            speech_probs.append(speech_prob)
        
        self.model.reset_states()  # Reset model states after each audio

        # If voice detected
        if any(prob > 0.9 for prob in speech_probs):  # Threshold can be adjusted
            # Forward to Whisper for transcription
            wav = wav.squeeze(0)  # Squeeze the tensor to remove the first dimension
            input_features = self.processor(wav, sampling_rate=16000, return_tensors="pt").input_features
            predicted_ids = self.whisper_model.generate(input_features)
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)

            print(f"SPEECH DETECTED {transcription}")
            return transcription[0]
        return ""
