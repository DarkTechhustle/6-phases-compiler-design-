# main.py
# Main program to run the lexical, syntax, and semantic analyzers

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer

def main():
    # Sample input
    input_text = "3 + 5 * (10 + 2)"

    # Phase 1: Lexical Analysis
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(token)

    # Phase 2: Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"\nAST: {ast}")

    # Phase 3: Semantic Analysis
    analyzer = SemanticAnalyzer(ast)
    result = analyzer.analyze()
    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()