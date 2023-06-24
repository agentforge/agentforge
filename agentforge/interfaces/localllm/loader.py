import torch, logging, importlib
from agentforge.utils import dynamic_import
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, GPTNeoXTokenizerFast
from agentforge.utils import logger
import importlib

def import_transformer_model_class(class_name):
    # Try to import the model class dynamically and return the model
    try:
        transformers_module = importlib.import_module("transformers")
        return getattr(transformers_module, class_name)
    except AttributeError:
        raise ImportError(f"Class {class_name} was not found in the transformers module")

## Loaders for different models
class LocalLoader:
    def __init__(self, config, device_map={'':0}, multi_gpu=False, device="cuda"):
        self.config = config
        self.device_map = device_map if 'device_map' not in config else config['device_map'] 
        self.multi_gpu = multi_gpu if 'multi_gpu' not in config else config['device_map'] 
        self.device = device
        self.model = None

    def load(self, config, device="cuda"):
        self.config = config
        if "llama" in config and bool(config["llama"]):
            self.llama(device)
        else:
            self.huggingface(device)
        return self.model, self.tokenizer


    # LOADING PEFT LORA
    def load_adapter(self, orig_model, lora_apply_dir=None, lora_config=None, ddp=None):
        print(f"Loading {lora_apply_dir}")
        module = dynamic_import('peft', ['PeftModel'])
        if ddp:
            device_map = {'': 0}
        else:
            if torch.cuda.device_count() > 1:
                device_map = "auto"
            else:
                device_map = {'': 0}

        print('Device map for lora:', device_map)

        model = module["PeftModel"].from_pretrained(
            orig_model, lora_apply_dir, device_map=device_map,
            torch_dtype=torch.float32, is_trainable=True)

        model.to(orig_model.device)
        print(lora_apply_dir, 'loaded')

        return model


    def llama(self, device="cuda"):
        # from transformers import LlamaTokenizer, LlamaForCausalLM
        LlamaForCausalLM = getattr(importlib.import_module('transformers'), 'LlamaForCausalLM')
        LlamaTokenizer = getattr(importlib.import_module('transformers'), 'LlamaTokenizer')
        logger.info("Loading llama...")
        # self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"], decode_with_prefix_space=True, clean_up_tokenization_spaces=True)
        self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"], decode_with_prefix_space=True, clean_up_tokenization_spaces=True)
        self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = "left"
        load_in_8bit = self.config.get("load_in_8bit", False)
        load_in_4bit = self.config.get("load_in_4bit", False)
        half = self.config.get("half", False)

        self.model = LlamaForCausalLM.from_pretrained(
            self.config["model_name"],
            load_in_8bit=bool(load_in_8bit),
            load_in_4bit=bool(load_in_4bit),
            torch_dtype=torch.float16,
            device_map=self.device_map,
        )
        if "peft_model" in self.config and self.config["peft_model"] != "":
            module = dynamic_import('peft', ['PeftModel'])
            self.model = module["PeftModel"].from_pretrained(
                self.model, self.config["peft_model"],
                torch_dtype=torch.float16,
                # device_map=device_map
            )

        #LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1 and self.multi_gpu:
            logger.info(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)
        
        if not self.multi_gpu and half and not load_in_4bit and not load_in_8bit:
            self.model.half()

    def huggingface(self, device="cuda", mpt=False):
        logger.info("Loading huggingface...")
        if self.config["model_name"] == None:
            raise ValueError("model_name must be defined")

        revision = self.config.get("revision", "main")
        load_in_8bit = self.config.get("load_in_8bit", False)
        load_in_4bit = self.config.get("load_in_4bit", False)
        torch_dtype = self.config.get("torch_dtype", "torch.float16")
        if torch_dtype == "torch.bfloat16":
            computed_torch = torch.bfloat16
        else:
            computed_torch = torch.float16
        padding_side = self.config.get("padding_side", "left")
        model_name = self.config["model_name"]

        model_klass = import_transformer_model_class(self.config["model_class"])
        tokenizer_klass = import_transformer_model_class(self.config["tokenizer_class"])

        logger.info(f"Loading model... {model_name}")

        config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
        if 'attn_impl' in self.config and self.config['attn_impl'] == 'triton':
            config.attn_config['attn_impl'] = 'triton'

        self.model = model_klass.from_pretrained(
            model_name,
            config=config,
            load_in_8bit=bool(load_in_8bit),
            load_in_4bit=bool(load_in_4bit),
            torch_dtype=computed_torch,
            device_map=self.device_map,
            revision=revision,
            trust_remote_code=True
        )


        if "peft_model" in self.config and self.config["peft_model"] != "":
            logger.info(f"Loading PEFT... {self.config['peft_model']}")
            if self.config["peft_model"][0] == "/": # hack to check for dirs -- this is what we use locally
                self.model = self.load_adapter(self.model, lora_apply_dir=self.config["peft_model"])
            else:
                # Coming from the HF repo
                module = dynamic_import('peft', ['PeftModel'])
                self.model = module["PeftModel"].from_pretrained(
                    self.model, self.config["peft_model"],
                    torch_dtype=torch_dtype,
                )

        logger.info(f"Loading AutoTokenizer... {tokenizer_klass}")
        self.tokenizer = tokenizer_klass.from_pretrained(
            self.config["tokenizer_name"],
            padding=False,
            add_special_tokens=False
        )

        # if self.config["tokenizer_name"] == "OpenAssistant/oasst-sft-1-pythia-12b":
        #     special_tokens_dict = {'additional_special_tokens': ['<|prompter|>', '<|assistant|>']}
        #     num_added_toks = self.tokenizer.add_special_tokens(special_tokens_dict)
        #     print('We have added', num_added_toks, 'tokens')
        #     self.model.resize_token_embeddings(len(self.tokenizer))  # Notice: resize_token_embeddings expect to receive the full size of the new vocabulary, i.e. the length of the tokenizer.

        # # LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1 and self.multi_gpu:
            logger.info(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)

        if not load_in_4bit and not load_in_8bit:
            self.model = self.model.to(self.device)
        self.model.eval()  # Set the model to evaluation mode
        logger.info(f"Model loaded and online...")
