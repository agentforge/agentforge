### Parses output and input text

class Parser:
  def __init__(self):
    pass

  def parse_prompt(self, text):
    return text.strip()

  def parse_response(self, text):
    text = text.split("## Output:")
    return text[0].strip()