# Big model

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")

model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b")

# Small example
from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

generator("What is a good tool for social interaction?", do_sample=True, min_length=50)


# MS Dialog GPT

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large", padding_side='left')
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# Let's chat for 5 lines
for step in range(10):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')
    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
    # generated a response while limiting the total chat history to 1000 tokens,
    print(bot_input_ids)
    chat_history_ids = model.generate(bot_input_ids, min_length=50, pad_token_id=tokenizer.eos_token_id)
    # pretty print last ouput tokens from bot
    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))


from transformers import pipeline
import torch
model_tag = 'pszemraj/gpt-peter-2.7B'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
my_chatbot = pipeline('text-generation', 
                      model_tag,
                      device=0 if device == 'cuda' else -1,
                    )

prompt = """
Did you ever hear the tragedy of Darth Plagueis The Wise?

Peter Szemraj:
"""
response = my_chatbot(prompt,
                      do_sample=True,
                      max_length=128,
                      temperature=0.6,
                      no_repeat_ngram_size=3,
                      repetition_penalty=3.5,
                    )
print(response[0]['generated_text'])


# Best So Far

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


text = "Hi, do you like star trek?"
model_inputs = tokenizer(text)

translation = model.generate(model_inputs)


from transformers import AutoTokenizer, AutoModelForCausalLM, GPTJForCausalLM
tokenizer = AutoTokenizer.from_pretrained("./EleutherAI-gpt-neo-1.3B-tokenizer")
model = AutoModelForCausalLM.from_pretrained("./EleutherAI-gpt-neo-1.3B")
prompt = """This is a discussion between a [human] and a [robot]. 
The [robot] is very nice and empathetic.
[human]: Hello
[robot]:
"""
input_ids = tokenizer(prompt, return_tensors="pt").input_ids
# generate up to 30 tokens
outputs = model.generate(input_ids, do_sample=True, max_length=64)
tokenizer.batch_decode(outputs, skip_special_tokens=True)
