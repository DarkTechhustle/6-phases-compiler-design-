# lexer.py
# Lexical Analyzer for a simple arithmetic expression language

import re

# Token types
TOKEN_TYPES = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('WHITESPACE', r'\s+'),
]

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            match = None
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    if token_type != 'WHITESPACE':  # Skip whitespace
                        tokens.append(Token(token_type, match.group(0)))
                    self.pos = match.end()
                    break
            if not match:
                raise ValueError(f'Invalid character: {self.text[self.pos]}')
        return tokens