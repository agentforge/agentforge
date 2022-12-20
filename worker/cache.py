# Caches model locally so we can embed it into the Docker container image
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSpeechSeq2Seq, AutoProcessor, GPTJForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
tokenizer.save_pretrained("./EleutherAI-gpt-neo-1.3B-tokenizer")

processor = AutoProcessor.from_pretrained("openai/whisper-large")
processor.save_pretrained("./openai-whisper-large-processor")

model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
model.save_pretrained("./EleutherAI-gpt-neo-1.3B")

whispermodel = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large")
whispermodel.save_pretrained("./openai-whisper-large")

gptj = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", torch_dtype=torch.float32)
gptj.save_pretrained("./EleutherAI-gpt-j-6B")