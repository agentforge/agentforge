import importlib, re

def str_to_class(classname):
  my_module = importlib.import_module("transformers")
  return getattr(my_module, classname)

  # Removes the incomplete sentence using regex
def remove_hanging(phrase):
  phrase = re.match("(^.*[\.\?!]|^\S[^.\?!]*)", phrase)
  phrase = phrase.group()