from transformers.generation.streamers import BaseStreamer
from transformers import AutoTokenizer
from flask_sse import sse

class TextStreamer(BaseStreamer):
    """
    Simple text streamer that prints the token(s) to stdout as soon as entire words are formed.
    Parameters:
        tokenizer (`AutoTokenizer`):
            The tokenized used to decode the tokens.
    Examples:
        ```python
        >>> from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
        >>> tok = AutoTokenizer.from_pretrained("gpt2")
        >>> model = AutoModelForCausalLM.from_pretrained("gpt2")
        >>> inputs = tok(["An increasing sequence: one,"], return_tensors="pt")
        >>> streamer = TextStreamer(tok)
        >>> # Despite returning the usual output, the streamer will also print the generated text to stdout.
        >>> _ = model.generate(**inputs, streamer=streamer, max_new_tokens=20)
        An increasing sequence: one, two, three, four, five, six, seven, eight, nine, ten, eleven,
        ```
    """

    def __init__(self, tokenizer: "AutoTokenizer"):
        self.tokenizer = tokenizer
        self.token_cache = []
        self.print_len = 0

    def put(self, value):
        """
        Recives tokens, decodes them, and prints them to stdout as soon as they form entire words.
        """
        if len(value.shape) > 1 and value.shape[0] > 1:
            raise ValueError("TextStreamer only supports batch size 1")
        elif len(value.shape) > 1:
            value = value[0]

        # Add the new token to the cache and decodes the entire thing.
        self.token_cache.extend(value.tolist())
        text = self.tokenizer.decode(self.token_cache)

        # After symbol for a new line, we flush the cache.
        if text.endswith("\n"):
            printable_text = text[self.print_len :]
            self.token_cache = []
            self.print_len = 0
        # Otherwise, prints until the last space char (simple heuristic to avoid printing incomplete words,
        # which may change with the subsequent token -- there are probably smarter ways to do this!)
        else:
            printable_text = text[self.print_len : text.rfind(" ") + 1]
            self.print_len += len(printable_text)

        # print(printable_text, flush=True, end="")
        sse.publish({"message": printable_text}, type='stream_completion')

    def end(self):
        """Flushes any remaining cache and prints a newline to stdout."""
        # Flush the cache, if it exists
        if len(self.token_cache) > 0:
            text = self.tokenizer.decode(self.token_cache)
            printable_text = text[self.print_len :]
            self.token_cache = []
            self.print_len = 0
        else:
            printable_text = ""

        # Print a newline (and the remaining text, if any)
        # print(printable_text, flush=True)
        sse.publish({"message": printable_text}, type='stream_completion')