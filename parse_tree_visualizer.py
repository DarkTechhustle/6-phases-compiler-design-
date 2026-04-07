# parse_tree_visualizer.py
# Enhanced Syntax Analyzer with Parse Tree Visualization

from ast import BinOp, Num, ASTNode

class ParseTreeVisualizer:
    """Visualizes the parse tree and shows how tokens are consumed"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.indent_level = 0
        self.trace = []

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, token_type):
        """Consume a token and trace it"""
        if self.current_token() and self.current_token().type == token_type:
            consumed = self.tokens[self.pos]
            self.trace.append(f"{'  ' * self.indent_level}→ Consumed: {consumed}")
            self.pos += 1
            return consumed
        else:
            raise ValueError(f'Expected {token_type}, got {self.current_token()}')

    def parse_with_trace(self):
        """Parse and show parsing trace"""
        self.trace.append(f"\n{'='*50}")
        self.trace.append(f"PARSING PROCESS - Token Consumption & Tree Building")
        self.trace.append(f"{'='*50}\n")
        
        result = self.expr()
        
        self.trace.append(f"\n{'='*50}")
        self.trace.append("Parsing Complete!")
        self.trace.append(f"{'='*50}\n")
        
        return result

    def expr(self):
        """expr → term ((PLUS | MINUS) term)*"""
        self.trace.append(f"{'  ' * self.indent_level}[expr] Processing expression")
        self.indent_level += 1
        
        node = self.term()
        
        while self.current_token() and self.current_token().type in ('PLUS', 'MINUS'):
            op_token = self.current_token()
            op = op_token.type
            self.trace.append(f"{'  ' * self.indent_level}[expr] Found {op}, building BinOp node")
            
            if op == 'PLUS':
                self.consume('PLUS')
                right = self.term()
                node = BinOp(node, '+', right)
                self.trace.append(f"{'  ' * self.indent_level}[expr] Created: {node.left} + {node.right}")
            elif op == 'MINUS':
                self.consume('MINUS')
                right = self.term()
                node = BinOp(node, '-', right)
                self.trace.append(f"{'  ' * self.indent_level}[expr] Created: {node.left} - {node.right}")
        
        self.indent_level -= 1
        return node

    def term(self):
        """term → factor ((MULTIPLY | DIVIDE) factor)*"""
        self.trace.append(f"{'  ' * self.indent_level}[term] Processing term")
        self.indent_level += 1
        
        node = self.factor()
        
        while self.current_token() and self.current_token().type in ('MULTIPLY', 'DIVIDE'):
            op_token = self.current_token()
            op = op_token.type
            self.trace.append(f"{'  ' * self.indent_level}[term] Found {op}, building BinOp node")
            
            if op == 'MULTIPLY':
                self.consume('MULTIPLY')
                right = self.factor()
                node = BinOp(node, '*', right)
                self.trace.append(f"{'  ' * self.indent_level}[term] Created: {node.left} * {node.right}")
            elif op == 'DIVIDE':
                self.consume('DIVIDE')
                right = self.factor()
                node = BinOp(node, '/', right)
                self.trace.append(f"{'  ' * self.indent_level}[term] Created: {node.left} / {node.right}")
        
        self.indent_level -= 1
        return node

    def factor(self):
        """factor → NUMBER | LPAREN expr RPAREN"""
        self.trace.append(f"{'  ' * self.indent_level}[factor] Processing factor")
        self.indent_level += 1
        
        token = self.current_token()
        if token and token.type == 'NUMBER':
            self.trace.append(f"{'  ' * self.indent_level}[factor] NUMBER found: {token.value}")
            self.consume('NUMBER')
            node = Num(int(token.value))
            self.trace.append(f"{'  ' * self.indent_level}[factor] Created leaf node: {node}")
            self.indent_level -= 1
            return node
        elif token and token.type == 'LPAREN':
            self.trace.append(f"{'  ' * self.indent_level}[factor] LPAREN found, recursing...")
            self.consume('LPAREN')
            self.indent_level += 1
            node = self.expr()
            self.indent_level -= 1
            self.trace.append(f"{'  ' * self.indent_level}[factor] Returned from expr()")
            self.consume('RPAREN')
            self.trace.append(f"{'  ' * self.indent_level}[factor] RPAREN found, closing parenthesis")
            self.indent_level -= 1
            return node
        else:
            raise ValueError(f'Invalid syntax: {token}')

    def print_trace(self):
        """Print the parsing trace"""
        for line in self.trace:
            print(line)

    def print_tree(self, node, prefix="", is_tail=True):
        """Print AST as a tree structure"""
        if isinstance(node, Num):
            print(prefix + ("└── " if is_tail else "├── ") + f"NUM: {node.value}")
        elif isinstance(node, BinOp):
            print(prefix + ("└── " if is_tail else "├── ") + f"OP: {node.op}")
            extension = "    " if is_tail else "│   "
            self.print_tree(node.left, prefix + extension, False)
            self.print_tree(node.right, prefix + extension, True)


class TreePrinter:
    """Pretty print the parse tree"""
    
    @staticmethod
    def print_ast_tree(node, indent=0, label="root"):
        """Print AST with proper tree formatting"""
        if isinstance(node, Num):
            print("  " * indent + f"├─ {label}: NUM({node.value})")
        elif isinstance(node, BinOp):
            print("  " * indent + f"├─ {label}: OP({node.op})")
            TreePrinter.print_ast_tree(node.left, indent + 1, "left")
            TreePrinter.print_ast_tree(node.right, indent + 1, "right")

    @staticmethod
    def get_tree_structure(node, indent=0):
        """Get tree structure as string"""
        result = []
        if isinstance(node, Num):
            result.append("  " * indent + f"NUM({node.value})")
        elif isinstance(node, BinOp):
            result.append("  " * indent + f"OP({node.op})")
            result.extend(TreePrinter.get_tree_structure(node.left, indent + 1))
            result.extend(TreePrinter.get_tree_structure(node.right, indent + 1))
        return result
