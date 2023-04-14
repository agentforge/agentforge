### Parses output and input text

class Parser:
  def __init__(self):
    pass

  def parse_prompt(self, text):
    return text.strip()

  # Returns and AgentResponse object that 
  def parse_output(self, output):
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return candidate
