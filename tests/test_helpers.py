import pytest
from core.helpers import helpers

# Test cases for the is_code function
@pytest.mark.parametrize("input_text,expected_result", [
    # Code examples
    ("def add(a, b):\n    return a + b", True),
    ("for i in range(10):\n    print(i)", True),
    ("import os\n\nos.makedirs('test_directory')", True),
    ("print('Hello, World!')", True),

    # Natural language examples
    ("This is a sample sentence about programming, but it's not code.", False),
    ("I like to write Python code and create new projects.", False),
    ("The quick brown fox jumps over the lazy dog.", False),
    ("To be or not to be, that is the question.", False),
])
def test_is_code(input_text, expected_result):
    is_code, _ = helpers.is_code_segment(input_text)
    assert is_code == expected_result


test_convert_numbers_in_sentence_data = [
    ("I have 3 apples and 15 oranges.", "I have three apples and fifteen oranges."),
    ("There are 20 cats and 4 dogs.", "There are twenty cats and four dogs."),
    ("In the year 2023, we have 5G technology.", "In the year two thousand and twenty-three, we have five G technology."),
    ("I ate 8 pieces of pizza.", "I ate eight pieces of pizza."),
    ("The 1000 page book is heavy.", "The one thousand page book is heavy.")
]
@pytest.mark.parametrize("input_sentence, expected_output", test_convert_numbers_in_sentence_data)
def test_convert_numbers_in_sentence(input_sentence, expected_output):
    assert helpers.convert_numbers_in_sentence(input_sentence) == expected_output