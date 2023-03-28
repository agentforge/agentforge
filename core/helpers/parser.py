### Parses output and input text

class Parser:
  def __init__(self):
    pass

  def parse_prompt(self, text):
    return text.strip()

  def parse_response(self, text):
    bad_output_delimeters = ['"""', "## Output:", "# End of Instruction.", "### End", "### Instruction", "### Response", "# Python Responses"]
    for i in bad_output_delimeters:
      text = text.split(i)
      text = text[0]    
    return text.strip()
