# syntax_analyzer_demo.py
# Demonstration of Syntax Analyzer with Parse Tree Visualization

from lexer import Lexer
from parse_tree_visualizer import ParseTreeVisualizer, TreePrinter
from ast import BinOp, Num

def demonstrate_syntax_analysis(expression):
    """Demonstrate syntax analysis for a given expression"""
    
    print("\n" + "="*70)
    print(f"SYNTAX ANALYSIS DEMONSTRATION")
    print("="*70)
    print(f"\nInput Expression: {expression}\n")
    
    # Step 1: Lexical Analysis
    print("-" * 70)
    print("STEP 1: LEXICAL ANALYSIS (Tokenization)")
    print("-" * 70)
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    print(f"\nTokens produced:")
    for i, token in enumerate(tokens, 1):
        print(f"  {i}. {token}")
    
    print(f"\nToken stream: ", end="")
    print(" → ".join([f"{t.type}({t.value})" for t in tokens]))
    
    # Step 2: Syntax Analysis with Trace
    print("\n" + "-" * 70)
    print("STEP 2: SYNTAX ANALYSIS (Parsing with Trace)")
    print("-" * 70)
    print("\nParsing process with token consumption trace:\n")
    
    visualizer = ParseTreeVisualizer(tokens)
    ast = visualizer.parse_with_trace()
    visualizer.print_trace()
    
    # Step 3: Parse Tree Visualization
    print("\n" + "-" * 70)
    print("STEP 3: PARSE TREE / AST VISUALIZATION")
    print("-" * 70)
    print("\nAbstract Syntax Tree (AST):\n")
    visualizer.print_tree(ast)
    
    print("\n\nTree Structure Representation:\n")
    for line in TreePrinter.get_tree_structure(ast):
        print(line)
    
    # Step 4: Grammar Rules Explanation
    print("\n" + "-" * 70)
    print("GRAMMAR RULES USED")
    print("-" * 70)
    print("""
The parser follows these grammar rules (precedence):

expr   → term ((PLUS | MINUS) term)*
term   → factor ((MULTIPLY | DIVIDE) factor)*
factor → NUMBER | LPAREN expr RPAREN

Precedence: MULTIPLY/DIVIDE > PLUS/MINUS > LPAREN
Associativity: Left-to-right
    """)
    
    return ast

def explain_parse_tree(ast, expression):
    """Explain the structure of the parse tree"""
    
    def get_tree_info(node, side=""):
        info = []
        if isinstance(node, Num):
            info.append(f"{side} Leaf node with value: {node.value}")
        elif isinstance(node, BinOp):
            info.append(f"{side} Binary operation node: {node.op}")
            info.append(f"  └─ Left operand:")
            info.extend(["      " + line for line in get_tree_info(node.left, "")])
            info.append(f"  └─ Right operand:")
            info.extend(["      " + line for line in get_tree_info(node.right, "")])
        return info
    
    print("\n" + "="*70)
    print("PARSE TREE EXPLANATION")
    print("="*70)
    print(f"\nFor expression: {expression}\n")
    for line in get_tree_info(ast):
        print(line)


if __name__ == "__main__":
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  SYNTAX ANALYZER - PARSE TREE DEMONSTRATION".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Example 1: Simple addition
    expr1 = "3 + 5"
    ast1 = demonstrate_syntax_analysis(expr1)
    explain_parse_tree(ast1, expr1)
    
    # Example 2: Parenthesized expression - (3 + 5) * 2
    print("\n\n" + "█"*70)
    expr2 = "(3 + 5) * 2"
    ast2 = demonstrate_syntax_analysis(expr2)
    explain_parse_tree(ast2, expr2)
    
    # Example 3: Complex expression - 3 + 5 * (10 + 2)
    print("\n\n" + "█"*70)
    expr3 = "3 + 5 * (10 + 2)"
    ast3 = demonstrate_syntax_analysis(expr3)
    explain_parse_tree(ast3, expr3)
    
    print("\n\n" + "="*70)
    print("="*70)
    