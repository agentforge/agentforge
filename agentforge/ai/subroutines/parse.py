from typing import Any, Dict
from agentforge.interfaces.model_profile import ModelProfile

### Final aggregation of prompt template and other prompt context into
### a single prompt string
class Parse:
    def __init__(self):
        self.model_profile = ModelProfile()
    
    """
    Example input:
    
    {'input': {'id': '4CdJEH2BS9Gedj7eL4OvZA', 'prompt': 'Hey!'}, 'context': {'_id': '4CdJEH2BS9Gedj7eL4OvZA', 'avatar_config': 
    {'name': 'Sam', 'biography': 'You are a general purpose open source AI model. You are able to process and understand large amounts of text,
    and can use this knowledge to provide accurate and informative responses to a wide range of questions.  Overall, you are a powerful tool 
    that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. You will do your best to 
    complete the task or answer any question. Your name is Sam and you are having a conversation with a user.'}, 
    'metadata': {'created_dt': '2023-06-04T10:25:22.188Z', 'updated_dt': '2023-06-04T12:07:13.452Z', 'user_id': 'test_user'}, 
    'generation_config': {'max_new_tokens': 512, 'top_k': 50, 'top_p': 1, 'temperature': 1, 'repetition_penalty': 1.2, 
    'early_stopping': False, 'do_sample': False, 'num_beams': 1, 'num_beam_groups': 1, 'use_cache': True, 'typical_p': 1, 
    'epsilon_cutoff': 0, 'eta_cutoff': 0, 'diversity_penalty': 0, 'encoder_repetition_penalty': 1, 'length_penalty': 1, 
    'no_repeat_ngram_size': 0, 'renormalize_logits': False, 'remove_invalid_values': False, 'num_return_sequences': 1, 
    'output_attentions': False, 'output_hidden_states': False, 'output_scores': False, 'return_dict_in_generate': False, 
    'encoder_no_repeat_ngram_size': 0}, 'model_config': 
    {'model_name': 'fragro/llama-7b-hf', 'tokenizer_name': 'fragro/llama-7b-hf', 'peft_model': 'tloen/alpaca-lora-7b', 
    'prompt_type': 'instruct_w_memory', 'model_class': 'AutoCasualModel', 'tokenizer_class': 'AutoTokenizer', 
    'bos_token': '<s>', 'eos_token': '</s>', 'load_in_8bit': True, 'load_in_4bit': False, 'device_map': 'cuda:0', 
    'speech': False, 'video': False, 'streaming': False}, 'prompt_config': 
    {'prompt_template': 'Below is an instruction that describes a task. Write a response that appropriately completes the request.
    Write a response that appropriately completes the request.\n        ### Instruction:\n        {instruction}\n        ### Response:'}}}
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt_template = context['model_profile']['prompt_config']['prompt_template']
        name = context['model_profile']['avatar_config']['name']
        biography = context['model_profile']['avatar_config']['biography']
        instruction = context['input']['prompt']
        recall = context['recall'] if 'recall' in context else ""

        prompt_template = prompt_template.replace("<name>", name)
        prompt_template = prompt_template.replace("<biography>", biography)
        prompt_template = prompt_template.replace("<instruction>", instruction)
        prompt_template = prompt_template.replace("<memory>", recall)

        context['input']['prompt'] = prompt_template
        context['input']['original_prompt'] = instruction

        # Parse ID from frontend and translate into model_profile
        return context
