### Parses output and input text
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter
from pygments.lexers.special import TextLexer

PREFIXES = ["My response would be:", "My response is:", "### Response:", "<s>"]
POSTFIXES = ['### Thought',
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
        "### Instruction"
        "### Instruction:",
        "# Instruction",
        "# Python Responses",
        "# Output:",
        "#if __name__ == '__main__':",
        "#end document",
        "<# end of output #>",
        "% endinstruction",
        "# End of story",
        "# Ask a question",
        "#include",
        "// output",
        "Note:",
        "</s>",
        "<|endoftext|>",
        "##",
        "###",
        '```',
        '\n(',
        '<|eot_id|>',
        '\n---\n',
        '\nPlease proceed'
      ]

def clean_newlines(self, input_string: str):
    return input_string.replace("\n", "<br>")

def convert_html(self, input_string: str, remove_code: bool = False):
    code_language_start_index = input_string.find("```") + 3
    code_language_end_index = input_string.find("\n", code_language_start_index)
    code_end_index = input_string.find("```", code_language_end_index + 1)

    if code_language_end_index >= 0 and code_end_index >= 0:
        code_language = input_string[code_language_start_index:code_language_end_index]
        code = input_string[code_language_end_index + 1:code_end_index]
        code_language = code_language.replace("{", "").strip()
        try:
            lexer = get_lexer_by_name(code_language, stripall=True)
        except ClassNotFound:
            lexer = TextLexer(stripall=True)

        formatter = HtmlFormatter(style='solarizeddark', oclasses=True)
        highlighted_code = highlight(code, lexer, formatter)
        if remove_code:
            highlighted_code = "\n"
        output = (
            input_string[:code_language_start_index - 3]
            + highlighted_code
            + input_string[code_end_index + 3:]
        )
        if "```" in output:
            return self.convert_html(output)
        return self.clean_newlines(output)
    else:
        return self.clean_newlines(input_string)


class Parser:
  def __init__(self):
    self.POSTFIXDICT = {}
    for i in POSTFIXES:
        self.POSTFIXDICT[i] = True

  def parse_prompt(self, text):
    return text.strip()

  # Returns and AgentResponse object that 
  def parse_output(self, output):
    responses = output.split("### Response:")
    candidate = responses[len(responses)-1].strip()
    # candidate = helpers.process_code_output(candidate)
    candidate = candidate.lstrip('\n')
    return candidate

  def parse_llm_stream(self, text):
    return self.POSTFIXDICT[text.strip()]

  # Keyed to alpaca-7b, needs to be updated for other models
  # TODO: make this more robust -- IMPLEMENT FOR STREAMING!
  def parse_llm_response(self, text, skip_tokens=[]):
      for i in POSTFIXES + skip_tokens:
          text = text.split(i)
          text = text[0]
      for i in PREFIXES:
          text = text.split(i)
          if len(text) > 1:
            text = text[1]
          else:
            text = text[0]
      # if "\n" not in skip_tokens:
      #   text = text.replace("\n", "<br>") # use br for new line
      return text.strip()
