import gc, json, os
from transformers import AutoTokenizer, AutoModelForCausalLM

CONFIG_DIR = os.environ["CONFIG_DIR"]
CONFIG_FILE = os.path.join(CONFIG_DIR, "models.json")

class LLMModelManager:
    def __init__(self, config):
      self.config = config
      self.key = None
      self._loaded_configs = {}

    def load_model(self, key):
      # Check key and load logic according to key
      self.current_config = self.load_model(key)
      self.key = key

    def unload_model(self):
      if self.tokenizer is not None:
          del self.tokenizer
          self.tokenizer = None

      if self.model is not None:
          del self.model
          self.model = None

      gc.collect()

    def switch_model(self, config):
      self.unload_model()
      self.config = config
      self.load_model()

    def load_config(self, key):
      if key not in self._loaded_configs:
        with open(CONFIG_FILE, "r") as f:
          configs = json.load(f)
        self._loaded_configs[key] = configs[key]

      return self._loaded_configs[key]