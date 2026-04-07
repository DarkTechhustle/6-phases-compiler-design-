# SYNTAX ANALYZER - DETAILED EXPLANATION

## What is Syntax Analysis?

**Syntax Analysis** (also called parsing) is the second phase of a compiler that:
1. **Takes**: Token stream from Lexical Analysis
2. **Verifies**: Tokens follow the grammar rules
3. **Produces**: Parse Tree (Abstract Syntax Tree - AST)

## How It Works

### Example: `(3 + 5) * 2`

#### Stage 1: Lexical Analysis (Input)
```
Token Stream: LPAREN(  NUMBER(3)  PLUS(+)  NUMBER(5)  RPAREN)  MULTIPLY(*)  NUMBER(2)
                |        |          |         |         |         |         |
                (        3          +         5         )         *         2
```

#### Stage 2: Parsing / Syntax Analysis (Process)

The parser follows grammar rules with **operator precedence**:

```
expr   → term ((PLUS | MINUS) term)*
term   → factor ((MULTIPLY | DIVIDE) factor)*
factor → NUMBER | LPAREN expr RPAREN

Precedence (highest to lowest):
1. Parentheses  ( )
2. Multiply/Divide: * /
3. Plus/Minus: + -
```

**Parsing Steps:**
```
1. [expr] starts
   └─ [term] starts
      └─ [factor] sees LPAREN
         └─ Recursively calls [expr] for (3 + 5)
            ├─ [term] → [factor] → 3 (NUMBER)
            ├─ Sees PLUS, creates BinOp: 3 + 5
         └─ Returns BinOp(3, +, 5)
   └─ [term] sees MULTIPLY
      └─ [factor] → 2 (NUMBER)
      └─ Creates: BinOp(BinOp(3,+,5), *, 2)

2. Token consumption order:
   ( → 3 → + → 5 → ) → * → 2 ✓
   All tokens valid according to grammar
```

#### Stage 3: Parse Tree Output

```
         *                          MULTIPLY (root)
        / \                        /          \
       +   2    ==>             +              2
      / \                      / \
     3   5                    3   5
     
    
     OP(*)
       ├── OP(+)
       │    ├── NUM(3)
       │    └── NUM(5)
       └── NUM(2)
```

## Key Points

### **Leaf Nodes** (Operands)
- Numbers, variables, constants
- `Num(3)`, `Num(5)`, `Num(2)`

### **Internal Nodes** (Operators)
- Binary operations: `+`, `-`, `*`, `/`
- `BinOp(left, op, right)`
- Root operation is the last to be evaluated

### **Tree Structure Shows Evaluation Order**
```
Expression: 3 + 5 * (10 + 2)

Parse Tree:        +
                  / \
                 3   *
                    / \
                   5  +
                     / \
                   10   2

Evaluation Order:
1. First: (10 + 2) = 12  [innermost parentheses]
2. Then: 5 * 12 = 60     [multiplication has higher precedence]
3. Finally: 3 + 60 = 63  [addition last]

Result = 63 ✓
```

## Examples from Demo

### Example 1: `3 + 5`
```
Tokens: NUMBER(3) → PLUS(+) → NUMBER(5)

Tree:      +
          / \
         3   5

Parser process:
- expr() → term() → factor() → consume NUMBER(3) → Num(3)
- Sees PLUS → consume PLUS
- term() → factor() → consume NUMBER(5) → Num(5)
- Creates: BinOp(Num(3), '+', Num(5))
```

### Example 2: `(3 + 5) * 2`
```
Tokens: LPAREN → NUMBER(3) → PLUS → NUMBER(5) → RPAREN → MULTIPLY → NUMBER(2)

Tree:        *           [Multiplication is root = higher precedence in term()]
           /   \
          +     2       [Addition evaluated first in parentheses]
         / \
        3   5

Why * is at root:
- term() handles MULTIPLY/DIVIDE (higher precedence)
- expr() handles PLUS/MINUS (lower precedence)
- Parentheses are lowest level (factor) - handled first
- Result: (3+5)*2 = 8*2 = 16 (not 3+5*2 = 13)
```

### Example 3: `3 + 5 * (10 + 2)`
```
Tokens: NUMBER(3) → PLUS → NUMBER(5) → MULTIPLY → LPAREN → NUMBER(10) → PLUS → NUMBER(2) → RPAREN

Tree:           +              [expr level]
              /   \
             3     *            [term level - higher precedence]
                 /   \
                5    +          [factor recursion - parentheses]
                    / \
                   10  2

Precedence respected:
1. (10 + 2) = 12   [parentheses first]
2. 5 * 12 = 60     [multiplication before addition]
3. 3 + 60 = 63     [addition last]
```

## Syntax vs Semantics

### Syntax Analysis:
- ✓ Checks if tokens follow grammar rules
- ✓ Builds tree structure
- ✓ Verifies parentheses match
- ✓ Respects operator precedence
- ✗ Does NOT check type correctness
- ✗ Does NOT evaluate expressions

### Semantic Analysis (Next Phase):
- ✓ Checks type compatibility
- ✓ Validates variable declarations
- ✓ Evaluates expressions: 3 + 5 = 8
- ✓ Detects semantic errors: 5 + "hello" ✗

## Common Parsing Problems & Solutions

### Problem 1: Operator Precedence
```
Expression: 2 + 3 * 4
Wrong:       + (if no precedence)
            / \
           2   *
              / \
             3   4
        = (2+3)*4 = 20 ✗

Correct:     +
            / \
           2   *
              / \
             3   4
        = 2+(3*4) = 14 ✓
```

### Problem 2: Parentheses
```
Expression: (2 + 3) * 4
Tree:        *
           /   \
          +     4
         / \
        2   3
     = (2+3)*4 = 20 ✓
```

### Problem 3: Left Associativity
```
Expression: 10 - 5 - 2
Tree:         -
            /   \
           -     2
          / \
        10   5
     = (10-5)-2 = 3 ✓  (not 10-(5-2) = 7)
```

## From Syntax Analysis to Next Phases

```
Source Code
    ↓
[LEXER] → Tokens
    ↓
[PARSER] → Parse Tree / AST  ← You are here
    ↓
[SEMANTIC ANALYZER] → Type checking, symbol table
    ↓
[ICG] → Three-address code
    ↓
[OPTIMIZER] → Optimized code
    ↓
[CODEGEN] → Assembly/Machine code
```

## Grammar Specification (BNF - Backus-Naur Form)

```
<expr>   ::= <term> (('+'|'-') <term>)*
<term>   ::= <factor> (('*'|'/') <factor>)*
<factor> ::= <number> | '(' <expr> ')'
<number> ::= [0-9]+
```

In words:
- An expression is one or more terms, separated by + or -
- A term is one or more factors, separated by * or /
- A factor is either a number or an expression in parentheses
- This automatically gives * and / higher precedence than + and -

## Summary

| Aspect | Details |
|--------|---------|
| **Input** | Token stream from Lexer |
| **Process** | Recursive descent parsing following grammar |
| **Output** | Abstract Syntax Tree (AST) |
| **Verifies** | Grammar rules, bracket matching, operator precedence |
| **Does NOT** | Type checking, evaluation, semantic validation |
| **Key Structure** | Tree with operators as internal nodes, numbers as leaves |
| **Importance** | Ensures syntactically correct programs before semantic analysis |
