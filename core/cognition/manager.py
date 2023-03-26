import gc, json, os
### Imports ###
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM

CONFIG_DIR = os.environ["CONFIG_DIR"]
CONFIG_FILE = os.path.join(CONFIG_DIR, "models.json")

class LLMModelManager:
    def __init__(self, config):
        self.config = config
        self.key = None
        self._loaded_configs = {}

    def load_model(self, key):
        # Check key and load logic according to key
        self.config = self.load_config(key)
        if key == "Alpaca":
            self.load_alpaca(self.config)
        else:
            self.load_huggingface(self.config)
        self.key = key

    def unload_model(self):
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        if self.model is not None:
            del self.model
            self.model = None

        gc.collect()

    # Switches model to a new model
    def switch_model(self, key):
        self.unload_model()
        self.config = self.load_config(key)
        self.load_model()
    
    def load_config(self, key):
        if key not in self._loaded_configs:
            with open(CONFIG_FILE, "r") as f:
                configs = json.load(f)
            self._loaded_configs[key] = configs[key]

        return self._loaded_configs[key]

    def load_alpaca(self):
        self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"])

        self.model = LlamaForCausalLM.from_pretrained(
            self.config["model_name"],
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map={'':0},
        )

        self.model = PeftModel.from_pretrained(
            self.model, self.current_config["peft_model"], torch_dtype=torch.float16, device_map={'':0}
        )

    def load_huggingface(self):
        if self.config["model_name"] == None:
            raise ValueError("model_name must be defined")

        revision = self.config.get("revision", "float16")
        torch_dtype = self.config.get("torch_dtype", torch.float16)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.config["model_name"],
            torch_dtype=torch_dtype,
            revision=revision,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.config["tokenizer_name"])

        device = torch.device("cuda") if self.gpu() else torch.device("cpu")
        print("gpu: ", self.gpu())
        self.model = self.model.to(device)

        print("Model loaded and online...")
