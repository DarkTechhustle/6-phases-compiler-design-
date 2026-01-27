# ast.py
# Abstract Syntax Tree nodes for the arithmetic expression language

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Num({self.value})'