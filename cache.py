# Caches model locally so we can embed it into the Docker container image
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
model.save_pretrained("./EleutherAI-gpt-neo-1.3B")