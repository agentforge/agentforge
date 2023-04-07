import json
import os

class Config:
  def __init__(self, config_name):
    self.CONFIG_DIR = os.getenv('CONFIG_DIR')
    config_name = config_name + ".json" if config_name is not None else "config.json"
    try:
      with open(self.CONFIG_DIR + config_name) as f:
        self._config = json.load(f)
      # store current config name
      self.config_name = config_name

    except FileNotFoundError:
      print(f"Config file {config_name} not found")
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
  