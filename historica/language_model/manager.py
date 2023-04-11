import gc, json, os
### Imports ###
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM

from historica import CONFIG_FILE

class LLMModelManager:
    def __init__(self):
        self.key = None
        with open(CONFIG_FILE, "r") as f:
            self._loaded_configs = json.load(f)
        self.tokenizer = None
        self.model = None
        self.multi_gpu = False

    def load_model(self, key):
        # Check key and load logic according to key
        self.config = self.load_config(key)
        if key == "alpaca-lora-7b":
            # Needs PEFT
            self.load_alpaca()
        else:
            # Load standard huggingface model
            self.load_huggingface()
        self.key = key

    def unload_model(self):
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        if self.model is not None:
            if not self.multi_gpu:
                self.model = self.model.cpu()
            del self.model
            self.model = None

        gc.collect()
        torch.cuda.empty_cache()

    # Switches model to a new model
    def switch_model(self, key):
        if self.key != key:
            self.unload_model()
            self.load_model(key)
            self.key = key
    
    def load_config(self, key):
        if key not in self._loaded_configs:
            with open(CONFIG_FILE, "r") as f:
                configs = json.load(f)
            self._loaded_configs[key] = configs[key]

        return self._loaded_configs[key]
 
    def load_alpaca(self, device="cuda", device_map="auto"):
        print("Loading alpaca...")
        self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"],decode_with_prefix_space=True, clean_up_tokenization_spaces=True)

        self.model = LlamaForCausalLM.from_pretrained(
            self.config["model_name"],
            # load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map=device_map,
        )

        self.model = PeftModel.from_pretrained(
            self.model, self.config["peft_model"],
            torch_dtype=torch.float16,
            device_map=device_map
        )

        # LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)
            self.multi_gpu = True

    def load_huggingface(self, device="cuda", device_map="auto"):
        print("Loading huggingface...")
        if self.config["model_name"] == None:
            raise ValueError("model_name must be defined")

        revision = self.config.get("revision", "main")
        load_in_8bit = self.config.get("load_in_8bit", True)
        torch_dtype = self.config.get("torch_dtype", torch.float16)
        cfg = self.config["model_name"]

        print(f"Loading model... {cfg}")
        self.model = AutoModelForCausalLM.from_pretrained(
            cfg,
            load_in_8bit=load_in_8bit,
            torch_dtype=torch_dtype,
            device_map=device_map,
            revision=revision,
        )
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config["tokenizer_name"])

        # LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)
            self.multi_gpu = True
    
        self.model = self.model.to(device)
        self.model.eval()  # Set the model to evaluation mode
        print(f"Model loaded and online... {self.model}")
