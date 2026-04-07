# icg.py
# Intermediate Code Generation (Three-Address Code)

from ast import BinOp, Num

class IntermediateCodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.temp_counter = 0
        self.code = []

    def generate(self):
        self.visit(self.ast)
        return self.code

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def visit(self, node):
        if isinstance(node, Num):
            return str(node.value)
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.op} {right}")
            return temp
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

class ThreeAddressCode:
    def __init__(self, code_list):
        self.instructions = code_list

    def __repr__(self):
        result = "Three-Address Code:\n"
        for i, instr in enumerate(self.instructions, 1):
            result += f"{i}: {instr}\n"
        return result

    def __str__(self):
        return "\n".join(self.instructions)
