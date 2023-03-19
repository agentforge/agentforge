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