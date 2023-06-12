import json
import os

# Loads config from JSON
class Config:
  def __init__(self, config_name):
    self.CONFIG_DIR = os.getenv('CONFIG_DIR')
    
    # If no config name is provided, load Nothing
    if config_name is None:
      return
    config_name = config_name + ".json" if config_name is not None else "config.json"
    try:
      with open(self.CONFIG_DIR + config_name) as f:
        self._config = json.load(f)
      # store current config name
      self.config_name = config_name

    except FileNotFoundError:
      self._config = {}
      self.config_name = config_name

  def __getitem__(self, key):
    return self._config[key]

  def __setitem__(self, key, value):
    self._config[key] = value

  def __delitem__(self, key):
    del self._config[key]

  def to_dict(self):
    return self._config
  
  def load_config(self, CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
      self._loaded_configs = json.load(f)
    self.CONFIG_FILE = CONFIG_FILE

  # Loads a config ig it hasn't been loaded yet
  def get_config(self, key):
      if key not in self._loaded_configs:
          with open(self.CONFIG_FILE, "r") as f:
              configs = json.load(f)
          self._loaded_configs[key] = configs[key]

      return self._loaded_configs[key]
