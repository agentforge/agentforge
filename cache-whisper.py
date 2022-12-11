# Caches model locally so we can embed it into the Docker container image
from transformers import AutoModelForSpeechSeq2Seq

model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large")
model.save_pretrained("./openai-whisper-large")