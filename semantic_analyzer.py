# semantic_analyzer.py
# Semantic Analyzer for the arithmetic expression language

from ast import BinOp, Num

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast

    def analyze(self):
        return self.visit(self.ast)

    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, BinOp):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            if node.op == '+':
                return left_val + right_val
            elif node.op == '-':
                return left_val - right_val
            elif node.op == '*':
                return left_val * right_val
            elif node.op == '/':
                if right_val == 0:
                    raise ValueError("Division by zero")
                return left_val / right_val
        else:
            raise ValueError(f"Unknown node type: {type(node)}")