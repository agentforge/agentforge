import importlib, re
from pygments import lex
from pygments.lexers import guess_lexer, ClassNotFound
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.token import Token
from collections import Counter
from pygments import highlight
import time, re, math
from functools import wraps
from flask import request
import inflect

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"API call: {request.path} took {elapsed_time:.4f} seconds")
        return response
    return wrapper

def str_to_class(classname):
  my_module = importlib.import_module("transformers")
  return getattr(my_module, classname)

  # Removes the incomplete sentence using regex
def remove_hanging(phrase):
  phrase = re.match("(^.*[\.\?!]|^\S[^.\?!]*)", phrase)
  phrase = phrase.group()
  
def convert_numbers_in_sentence(sentence):
    def convert_word_recursive(word):
        # Find the first occurrence of a math symbol in the word
        math_symbol = next((symbol for symbol in math_symbol_map if symbol in word), None)

        if math_symbol:
            # If a math symbol is found, split the word and convert recursively
            left_word, right_word = word.split(math_symbol, 1)
            return convert_word_recursive(left_word) + [math_symbol_map[math_symbol]] + convert_word_recursive(right_word)
        else:
            # Remove ',' and '.' characters
            cleaned_word = word.replace(',', '').replace('.', '')
            if cleaned_word.isdigit():
                return [p.number_to_words(int(cleaned_word))]
            else:
                return [word]

    p = inflect.engine()

    # Define a dictionary to map mathematical symbols to their English language equivalents
    math_symbol_map = {
        '+': ' plus ',
        '=': ' equals ',
        '-': ' minus ',
        '*': ' times ',
        '/': ' divided by ',
        '^': ' to the power of '
    }

    # Split the sentence into words and delimiters
    words_and_delimiters = re.split(r'(\s+)', sentence)

    # Iterate through the words and convert numbers and mathematical symbols to their word representation
    converted_words = []
    for word in words_and_delimiters:
        converted_words.extend(convert_word_recursive(word))

    # Join the words and delimiters back into a sentence
    converted_sentence = ''.join(converted_words)
    return converted_sentence

def is_code_segment(text, threshold=0.85, outer_weight=2):
    try:
        common_natural_language_words = {
            'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'at', 'before', 'behind', 'below',
            'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during',
            'except', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside',
            'over', 'past', 'regarding', 'round', 'since', 'through', 'throughout', 'toward', 'under', 'underneath', 'unlike', 'until',
            'up', 'upon', 'with', 'within', 'without', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
        }
        python_keywords_functions = {
            'def', 'return', 'class', 'if', 'else', 'elif', 'while', 'for', 'in', 'yield', 'import', 'from', 'as', 'try', 'except',
            'finally', 'with', 'lambda', 'print', 'input', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'sum', 'all', 'any'
        }

        # Remove any common natural language words that are also Python keywords or functions
        common_natural_language_words -= python_keywords_functions

        lexer = get_lexer_by_name("python", stripall=True)
        tokens = list(lexer.get_tokens(text))
        token_types_counts = Counter([token[0] for token in tokens])
        total_tokens = sum(token_types_counts.values())

        code_token_types = (
            Token.Keyword, Token.Name, Token.Literal,
            Token.Operator, Token.Punctuation
        )
        code_tokens = sum(
            token_types_counts.get(token_type, 0) for token_type in code_token_types
        )

        # Include Text tokens and Name tokens that are Python keywords or common functions
        code_tokens += sum(1 for token in tokens if token[0] in {Token.Text, Token.Name} and token[1] in python_keywords_functions)
        
        code_probability = code_tokens / total_tokens
    
        print(f"code_probability: {code_probability} = {code_tokens} / {total_tokens}")

        # Apply a penalty for shorter texts
        penalty_factor = math.log(max(len(text), 10)) / math.log(10)
        code_probability *= penalty_factor

        print(f"penalty_factor: {code_probability} *= {penalty_factor}")

        # Check for common natural language words
        words = text.lower().split()
        common_word_count = sum(1 for word in words if word in common_natural_language_words)
        common_word_probability = common_word_count / len(words)

        print(f"common_word_probability: {common_word_probability} = {common_word_count} / {len(words)}")

        # Give more weight to outermost parts
        first_last_tokens_weight = sum(1 for token in tokens[:3] + tokens[-3:] if token[0] in code_token_types)
        first_last_tokens_weight /= len(tokens[:3] + tokens[-3:])
        weighted_code_probability = (code_probability + first_last_tokens_weight * outer_weight) / (1 + outer_weight)

        print(f"weighted_code_probability: {weighted_code_probability} = ({code_probability} + {first_last_tokens_weight} * {outer_weight}) / (1 + {outer_weight})")

        is_code = (weighted_code_probability > threshold) and (weighted_code_probability > common_word_probability)

        print(f"({code_probability} > {threshold}) and ({code_probability} > {common_word_probability})")
        print(f"({weighted_code_probability} > {threshold}) and ({weighted_code_probability} > {common_word_probability})")

        if is_code:
            return is_code, "Python"
        else:
            return False, None

    except Exception:
        return False, None


def process_code_output(output):
    # Check if the entire string is code
    is_entire_string_code, language_name = is_code_segment(output)

    if is_entire_string_code:
        # If the entire string is code, wrap it with ``` and the language name
        return f"```{language_name}\n" + output.strip() + "\n```"
    else:
        # Split the text into segments using blank lines, ignoring newlines inside the code blocks
        segments = re.split(r'(?<=\n)\n(?!\n)', output.strip())

        processed_segments = []

        for segment in segments:
            is_code, language_name = is_code_segment(segment)
            if is_code:
                if segment.startswith("```") and segment.endswith("```"):
                    processed_segments.append(segment.strip())
                else:
                    processed_segments.append(f"```{language_name}\n" + segment.strip() + "\n```")
            else:
                processed_segments.append(segment.strip())

        return '\n\n'.join(processed_segments)