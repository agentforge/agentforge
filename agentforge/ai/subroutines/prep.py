from typing import Any, Dict
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

### Preps output for end-user, stripping PII/IDs and anything else unserializable
### Also implements presentation layer
class Prep:
    def __init__(self):
        pass

    def convert_html(self, input_string: str):
        code_language_start_index = input_string.find("```") + 3
        code_language_end_index = input_string.find("\n", code_language_start_index)
        code_end_index = input_string.find("```", code_language_end_index + 1)

        if code_language_end_index >= 0 and code_end_index >= 0:
            code_language = input_string[code_language_start_index:code_language_end_index]
            code = input_string[code_language_end_index + 1:code_end_index]

            lexer = get_lexer_by_name(code_language, stripall=True)
            formatter = HtmlFormatter(style='solarizedlight', oclasses=True)
            highlighted_code = highlight(code, lexer, formatter)

            output = (
                input_string[:code_language_start_index - 3]
                + highlighted_code
                + input_string[code_end_index + 3:]
            )
            if "```" in output:
                return self.convert_html(output)
            return output
        else:
            return input_string

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        del context['memory']
        presentation = context['model_config']['presentation'] if 'model_config' in context and 'presentation' in context['model_config'] else "html"
        if presentation == 'html':
            context['response'] = self.convert_html(context['response'])
        context['choices'] = [{"text": context['response']}] # OAI backwargs compatible
        return context
