import inflect
import re

# TTS Normalization 

def clean_word(word):
    return word.replace('.', '').replace(',', '').strip()

def tokenize(sentence):
    return re.findall(r'\b\w+\b', sentence)

def is_year(token):
    year_pattern = re.compile(r'(\d{4})')
    if year_pattern.match(token):
        year = int(token)
        return 1000 <= year <= 2100
    return False

def process_year(year, p):
    if 1000 <= year < 2000:
        tens = year % 100
        if tens == 0:
            return f'{p.number_to_words(year // 100)} hundred'
        else:
            return f'{p.number_to_words(year // 100)}-{p.number_to_words(tens, group=2)}'
    else:
        return p.number_to_words(year, group=2)

def process_year_fragments(sentence, p = inflect.engine()):
    tokens = tokenize(sentence)
    processed_tokens = []

    for i, token in enumerate(tokens):
        if is_year(token):
            prev_token = tokens[i - 1] if i > 0 else ""
            next_token = tokens[i + 1] if i < len(tokens) - 1 else ""

            if not (re.match(r'\d', prev_token) or re.match(r'\d', next_token) or re.match(r'[\+\-\*/]', prev_token) or re.match(r'[\+\-\*/]', next_token)):
                year = int(token)
                processed_year = process_year(year, p)
                token = processed_year

        processed_tokens.append(token)

    return " ".join(processed_tokens)

def process_date_sentence(sentence, p = inflect.engine()):
    # Define mappings for month and day abbreviations
    month_mapping = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
        'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
        'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }

    day_mapping = {
        'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday',
        'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'
    }

    # Regular expression to match date patterns
    date_pattern = re.compile(r'(\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b[.,]? ?)?(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b[.,]? ?)(\d{1,2})(?:st|nd|rd|th)?,? (\d{4})')
    date_pattern2 = re.compile(r'(\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b[.,]? ?)?(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b[.,]? ?)(\d{1,2})?(?:st|nd|rd|th)?,? ?(\d{4})?')
        
    p = inflect.engine()

    def replace_date(match):
        day_abbr, month_abbr, day, year = match.groups()
        day = int(day)
        year = int(year)
        day_str = p.ordinal(day)
        month_map = clean_word(month_abbr)
        month_str = month_mapping[month_map] if month_map in month_mapping else month_map
        year_str = process_year(year)

        if day_abbr:
            day_val = clean_word(day_abbr)
            day_map = day_mapping[day_val] if day_val in day_mapping else day_val
            day_str = f'{day_map}, {day_str}'

        return f'{month_str} {day_str}, {year_str}'
    
    processed_sentence = date_pattern2.sub(replace_date, sentence)
    processed_sentence = date_pattern.sub(replace_date, processed_sentence)
    return processed_sentence

def get_postfix(day):
    if 10 <= day % 100 <= 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

def add_date_postfix(date_string):
    date_pattern = re.compile(r'(\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b[.,]? ?)?(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b[.,]? ?)(\d{1,2})(?:st|nd|rd|th)?,? (\d{4})')
    match = date_pattern.match(date_string)
    if match:
        day = int(match.group(3))
        postfix = get_postfix(day)
        formatted_date = f"{match.group(2)} {day}{postfix}, {match.group(4)}"
        return formatted_date
    else:
        return date_string

def process_date_terms(sentence, p = inflect.engine()):
    words = sentence.split()

    processed_words = []
    for word in words:
        fixed = clean_word(word)
        match = re.match(r'(\d+)(st|nd|rd|th)', fixed)
        if match:
            processed_words.append(p.number_to_words(fixed))
        else:
            processed_words.append(word)

    return ' '.join(processed_words)

def check_math_tokens(left_word, right_word):
    pattern = re.compile(r'^\d|\s|\(|\)$')
    return (bool(pattern.match(left_word)) or left_word == '') and (bool(pattern.match(right_word)) or right_word == '')

def convert_numbers_in_sentence(sentence, p = inflect.engine()):
    def convert_word_recursive(word):
        # Find the first occurrence of a math symbol in the word
        math_symbol = next((symbol for symbol in math_symbol_map if symbol in word), None)

        if math_symbol:
            # If a math symbol is found, split the word and convert recursively
            left_word, right_word = word.split(math_symbol, 1)
            print(f"'{left_word}' - '{right_word}'")
            if check_math_tokens(left_word, right_word):
                return convert_word_recursive(left_word) + [math_symbol_map[math_symbol]] + convert_word_recursive(right_word)
            else:
                return [word]
        else:
            # Remove ',' and '.' characters
            cleaned_word = clean_word(word)
            if cleaned_word.isdigit():
                return [p.number_to_words(int(cleaned_word))]
            else:
                return [word]

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


# Some parsing is really only appropriate for the TTS so we do it here
def normalize_transcription(text) -> None:
  text = process_date_sentence(text)
  text = process_date_terms(text)
  return convert_numbers_in_sentence(text)
