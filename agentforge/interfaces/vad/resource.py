import io, torch, json
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
        self.reset()

    def reset(self):
        self.audio_queue = []
        self.previous_timestamp = 0

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
        timestamp_length = 8  # 8 bytes for 64-bit number
        audio_data = chunk[:-timestamp_length]
        timestamp_data = chunk[-timestamp_length:]

        # Interpret the bytes as a 64-bit unsigned integer in little-endian format
        current_timestamp = int.from_bytes(timestamp_data, byteorder='little', signed=False) / 1000.0

        # Convert to seconds by dividing by 1000 since the original timestamp was in milliseconds
        self.audio_queue.append(audio_data)
        combined_audio = b''.join(self.audio_queue)

        logger.info(f"Chunk length: {len(audio_data)}")
        logger.info(f"combined_audio length: {len(combined_audio)}")
        start_time = len(combined_audio) - len(audio_data)

        if self.is_valid_webm(combined_audio):
            logger.info("Valid WebM data")
        else:
            logger.info("Invalid WebM data")

        # Debugging: Print the first few bytes to ensure they look correct
        logger.info(f"First 10 bytes of chunk: {combined_audio[:10]}")

        try:
            # Convert audio_bytes from WebM to WAV
            audio_webm = AudioSegment.from_file(io.BytesIO(combined_audio), format="webm")
            buffer = io.BytesIO()
            audio_webm.export(buffer, format="wav")
            buffer.seek(0)
            logger.info("Conversion to WAV successful")
        except Exception as e:
            logger.error(f"An error occurred during conversion: {e}")

        # Additional debugging: Check the content of the buffer
        buffer_content = buffer.getvalue()
        logger.info(f"Buffer length: {len(buffer_content)}")
        if len(buffer_content) > 0:
            logger.info(f"First 10 bytes of buffer: {buffer_content[:10]}")
        else:
            logger.info("Buffer is empty, conversion may have failed")

        # Now load the WAV data
        wav, sr = torchaudio.load(buffer)

        print(wav.shape, sr)
        print(self.previous_timestamp, current_timestamp)
        if self.previous_timestamp == 0:
            self.previous_timestamp = current_timestamp

        if self.previous_timestamp is not None:
            # Convert the elapsed time from microseconds to seconds
            elapsed_time_seconds = current_timestamp - self.previous_timestamp

            print(elapsed_time_seconds)
            # Calculate the number of samples that corresponds to the elapsed time
            elapsed_samples = int(sr * elapsed_time_seconds)

            # Extract the last `elapsed_samples` from the wav tensor
            wav = wav[:, -elapsed_samples:]            

        self.previous_timestamp = current_timestamp  # Update the previous timestamp
        
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
            print(f"Original wav shape: {wav.shape}")

            # silence_duration = 1.0  # duration of silence in seconds
            # silence_samples = int(sr * silence_duration)  # Convert silence duration to number of samples

            # # Create a tensor of zeros for silence, with the same number of channels as `wav`
            # silence_tensor = torch.zeros(wav.shape[0], silence_samples)

            # # Concatenate the silence to the beginning and end of the waveform tensor
            # padded_wav = torch.cat((silence_tensor, wav, silence_tensor), dim=1)
            # print(f"Padded wav shape: {padded_wav.shape}")

            # # Create a path for the output file
            # output_path = f"./test-{current_timestamp}.wav"

            # # Save the tensor as a .wav file
            # torchaudio.save(output_path, wav, sr)

            wav = wav.squeeze(0)  # Squeeze the tensor to remove the first dimension
            input_features = self.processor(wav, sampling_rate=16000, return_tensors="pt").input_features
            predicted_ids = self.whisper_model.generate(input_features)
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)

            print(f"SPEECH DETECTED {transcription}")
            return json.dumps({'transcription': transcription[0], 'timestamp': current_timestamp})
        return json.dumps({'transcription': "", 'timestamp': current_timestamp})
