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

  # Keyed to alpaca-7b, needs to be updated for other models
  # TODO: make this more robust
  def parse_llm_response(self, text):
      bad_output_delimeters = ['### Thought',
        '# End',
        '# end',
        "# noqa",
        "#noqa",
        '! # No answer',
        'Output:', '"""',
        "### Input:",
        "#noinstantiation",
        "## Output:",
        "# End of Instruction",
        "### End",
        "### Instruction",
        "# Instruction",
        "### Response",
        "# Python Responses",
        "# Output:",
        "#if __name__ == '__main__':",
        "#end document",
        "<# end of output #>",
        "% endinstruction",
        "# End of story",
        "# Ask a question",
        "#include",
        "// output"
      ]
      for i in bad_output_delimeters:
          text = text.split(i)
          text = text[0]
      text = text.replace("\n", "<br>") # use br for new line
      print(text)
      return text.strip()
