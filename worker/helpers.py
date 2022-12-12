import importlib

def str_to_class(classname):
  my_module = importlib.import_module("transformers")
  return getattr(my_module, classname)
