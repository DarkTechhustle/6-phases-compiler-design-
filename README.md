# Compiler Design: Lexical, Syntax, and Semantic Analyzers

This project implements the first three phases of a compiler for a simple arithmetic expression language.

## Phases Implemented

1. **Lexical Analysis (Lexer)**: Tokenizes the input string into tokens like numbers, operators, and parentheses.
2. **Syntax Analysis (Parser)**: Parses the tokens into an Abstract Syntax Tree (AST).
3. **Semantic Analysis**: Traverses the AST, performs semantic checks (e.g., division by zero), and evaluates the expression.

## Supported Grammar

- Expressions: `expr -> term ((+ | -) term)*`
- Terms: `term -> factor ((* | /) factor)*`
- Factors: `factor -> NUMBER | ( expr )`

## Files

- `lexer.py`: Contains the Lexer class for tokenizing input.
- `parser.py`: Contains the Parser class for building the AST.
- `ast.py`: Defines AST node classes (BinOp, Num).
- `semantic_analyzer.py`: Contains the SemanticAnalyzer class for traversing the AST and evaluating.
- `main.py`: Main program that demonstrates all three phases.

## Usage

Run the main program:

```bash
python main.py
```

You can modify the `input_text` in `main.py` to test different expressions.

## Example

Input: `"3 + 5 * (10 + 2)"`

Tokens:
- Token(NUMBER, 3)
- Token(PLUS, +)
- Token(NUMBER, 5)
- Token(MULTIPLY, *)
- Token(LPAREN, ()
- Token(NUMBER, 10)
- Token(PLUS, +)
- Token(NUMBER, 2)
- Token(RPAREN, ))

AST: BinOp(Num(3), +, BinOp(Num(5), *, BinOp(Num(10), +, Num(2))))

Result: 63