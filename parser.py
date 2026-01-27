# parser.py
# Syntax Analyzer (Parser) for a simple arithmetic expression language

from ast import BinOp, Num

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, token_type):
        if self.current_token() and self.current_token().type == token_type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise ValueError(f'Expected {token_type}, got {self.current_token()}')

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.current_token() and self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token()
            if op.type == 'PLUS':
                self.consume('PLUS')
                node = BinOp(node, '+', self.term())
            elif op.type == 'MINUS':
                self.consume('MINUS')
                node = BinOp(node, '-', self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token().type in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token()
            if op.type == 'MULTIPLY':
                self.consume('MULTIPLY')
                node = BinOp(node, '*', self.factor())
            elif op.type == 'DIVIDE':
                self.consume('DIVIDE')
                node = BinOp(node, '/', self.factor())
        return node

    def factor(self):
        token = self.current_token()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return Num(int(token.value))
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        else:
            raise ValueError(f'Invalid syntax: {token}')