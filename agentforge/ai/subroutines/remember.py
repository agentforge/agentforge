from typing import Any, Dict

### Stores a context for a user in the memory
class Remember:
    def __init__(self):
        pass
    
    """
    Exception: {'input': {'id': '4CdJEH2BS9Gedj7eL4OvZA', 'prompt': 'Below is an instruction that describes a task.
    Write a response that appropriately completes the request. Write a response that appropriately completes the request.\n 
                ### Instruction:\n        You are a general purpose open source AI model. You are able to process and u
                nderstand large amounts of text, and can use this knowledge to provide accurate and informative responses
                    to a wide range of questions.  Overall, you are a powerful tool that can help with a wide range of task
                    s and provide valuable insights and information on a wide range of topics. You will do your best to co
                    mplete the task or answer any question. Your name is Sam and you are having a conversation with a user.
                    You are Sam conversing with a Human. Write from the perspective of Sam.\n        Hi! What is your nam
                    e?\n        ### Response:'}, 'model_profile': {'_id': '4CdJEH2BS9Gedj7eL4OvZA', 'avatar_config': {'nam
                    e': 'Sam', 'biography': 'You are a general purpose open source AI model. You are able to process and u
                    nderstand large amounts of text, and can use this knowledge to provide accurate and informative respons
                    es to a wide range of questions.  Overall, you are a powerful tool that can help with a wide range of t
                    asks and provide valuable insights and information on a wide range of topics. You will do your best to 
                    complete the task or answer any question. Your name is Sam and you are having a conversation with a user.'},
                        'metadata': {'created_dt': '2023-06-04T10:25:22.188Z', 'updated_dt': '2023-06-04T12:47:23.973Z', 'user_id': 'test_user'},
                        'generation_config': {'max_new_tokens': 512, 'top_k': 50, 'top_p': 1, 'temperature': 1, 'repetition_penalty': 1.2
                , 'min_new_tokens': None, 'early_stopping': False, 'max_time': None, 'do_sample': False, 'num_beams': 1,
                    'num_beam_groups': 1, 'penalty_alpha': None, 'use_cache': True, 'typical_p': 1, 'epsilon_cutoff': 0,
                'eta_cutoff': 0, 'diversity_penalty': 0, 'encoder_repetition_penalty': 1, 'length_penalty': 1, 
                'no_repeat_ngram_size': 0, 'bad_words': '', 'force_words': '', 'renormalize_logits': False,
                    'forced_bos_token': '', 'forced_eos_token': '', 'remove_invalid_values': False, 
                'exponential_decay_length_penalty': '', 'suppress_tokens': '', 'begin_suppress_tokens': '', 'forced_decoder_ids': '',
                'num_return_sequences': 1, 'output_attentions': False, 'output_hidden_states': False, 'output_scores': False,
                    'return_dict_in_generate': False, 'encoder_no_repeat_ngram_size': 0, 'decoder_start_token': ''},
                    'model_config': {'model_name': 'fragro/llama-7b-hf', 'tokenizer_name': 'fragro/llama-7b-hf', 
                    'peft_model': 'tloen/alpaca-lora-7b', 'prompt_type': 'instruct_w_memory', 'model_class': 'AutoCasualModel', 
                    'tokenizer_class': 'AutoTokenizer', 'pad_token': '', 'bos_token': '<s>', 'eos_token': '</s>', 
                    'load_in_8bit': True, 'load_in_4bit': False, 'attn_impl': '', 'device_map': 'cuda:0', 'speech': False, 
                    'video': False, 'streaming': False}, 'prompt_config': {'prompt_template': 'Below is an instruction 
                    that describes a task. Write a response that appropriately completes the request. Write a response 
                    that appropriately completes the request.\n        ### Instruction:\n        <biography> You are <
                    name> conversing with a Human. Write from the perspective of <name>.\n        <instruction>\n    
                            ### Response:'}}, 'memory': <agentforge.ai.cognition.memory.Memory object at 0x7feab5b8fee0>
                            , 'response': "Hi there! My name is Sam. It's nice to meet you."}

    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if 'memory' not in context:
            return # No memory setup
        # raise Exception(context)
        context['memory'].remember(
            context['model_profile']['metadata']['user_id'],
            context['model_profile']['avatar_config']['name'],
            context['input']['original_prompt'],
            context['response']
        )

        return context