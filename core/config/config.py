import json
import os

class Config:
  def __init__(self, config_name):
    CONFIG_DIR = os.getenv('CONFIG_DIR')
    config_name = config_name + ".json" if config_name is not None else "config.json"
    with open(CONFIG_DIR + config_name) as f:
      self._config = json.load(f)

  def __getitem__(self, key):
    return self._config[key]

  def __setitem__(self, key, value):
    self._config[key] = value

  def __delitem__(self, key):
    del self._config[key]

  def to_dict(self):
    return self._config
  