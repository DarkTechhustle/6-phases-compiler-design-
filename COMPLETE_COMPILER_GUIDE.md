# COMPLETE 6-PHASE COMPILER GUIDE

## Overview

Your compiler now implements all 6 phases of compilation. When you run `python main.py`, you get complete output showing how source code transforms through the entire compilation pipeline.

## The 6 Phases of Compilation

### Phase 1: Lexical Analysis
**Input:** Source code string  
**Output:** Token stream  
**Purpose:** Break source code into meaningful units (tokens)

```
Input:  "(3 + 5) * 2"
Output: LPAREN(  NUMBER(3)  PLUS(+)  NUMBER(5)  RPAREN)  MULTIPLY(*)  NUMBER(2)
```

**Key Points:**
- Identifies token types: NUMBER, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN
- Skips whitespace
- Validates characters

---

### Phase 2: Syntax Analysis (Parsing) with Parse Tree
**Input:** Token stream  
**Output:** Abstract Syntax Tree (AST) with tree visualization  
**Purpose:** Verify tokens follow grammar rules and build hierarchical structure

```
Tokens: LPAREN NUMBER(3) PLUS NUMBER(5) RPAREN MULTIPLY NUMBER(2)

Parse Tree:        *
                  / \
                 +   2
                / \
               3   5

AST Structure:
BinOp(BinOp(Num(3), +, Num(5)), *, Num(2))
```

**Key Points:**
- Respects operator precedence: `*` and `/` before `+` and `-`
- Handles parentheses for grouping
- Shows token consumption trace
- Visualizes tree structure
- Tree root shows operation evaluated last

**Grammar Rules:**
```
expr   → term ((PLUS | MINUS) term)*
term   → factor ((MULTIPLY | DIVIDE) factor)*
factor → NUMBER | LPAREN expr RPAREN
```

---

### Phase 3: Semantic Analysis
**Input:** AST from parser  
**Output:** Semantic validation + expression evaluation  
**Purpose:** Check type correctness and validate semantics

```
AST: BinOp(BinOp(Num(3), +, Num(5)), *, Num(2))

Evaluation:
├─ Evaluate left: 3 + 5 = 8
├─ Evaluate right: 2
└─ Combine: 8 * 2 = 16

Result: 16
```

**Key Points:**
- Validates operations are valid
- Evaluates expression to verify correctness
- Detects semantic errors (e.g., type mismatches)
- For arithmetic expressions, produces the final result

---

### Phase 4: Intermediate Code Generation (ICG)
**Input:** AST  
**Output:** Three-Address Code (TAC)  
**Purpose:** Convert AST to intermediate representation

```
AST: BinOp(BinOp(Num(3), +, Num(5)), *, Num(2))

Generated Three-Address Code:
t1 = 3 + 5        (temporary variable t1 holds first operation)
t2 = t1 * 2       (temporary variable t2 holds final result)
```

**Key Points:**
- Each instruction has max 3 operands: `var = operand1 OP operand2`
- Creates temporary variables (t1, t2, t3, ...)
- Shows evaluation order explicitly
- Easier to optimize than AST
- Close to machine code but still high-level

---

### Phase 5: Code Optimization
**Input:** Three-Address Code  
**Output:** Optimized Three-Address Code  
**Purpose:** Reduce code size and execution time

**Optimization Techniques Applied:**

#### 1. Constant Folding
```
Before: t1 = 3 + 5
After:  t1 = 8        (computed at compile time)
```

#### 2. Dead Code Elimination
```
Before: t1 = something
        t2 = t1 * value
        (t1 never used again)
After:  Just keep t2 assignment
```

#### 3. Common Subexpression Elimination
```
Before: t1 = a + b
        t2 = a + b    (same calculation)
        t3 = t1 + t2
After:  t1 = a + b
        t2 = t1       (reuse result)
        t3 = t1 + t2
```

**Example Output:**
```
Input:   t1 = 3 + 5
         t2 = t1 * 2

Output:  t1 = 8          (constant folding applied)
         t2 = t1 * 2
```

---

### Phase 6: Code Generation
**Input:** Optimized Three-Address Code  
**Output:** Assembly Code (x86-64)  
**Purpose:** Generate actual machine-executable code

```
Three-Address Code:
t1 = 8
t2 = t1 * 2

Generated Assembly:
mov rax, 8        (load 8 into register RAX)
imul rax, 2       (multiply RAX by 2)
mov rbx, rax      (store result in RBX)
mov rax, rbx      (move result to return register)
ret               (return from function)
```

**Key Points:**
- Allocates registers for temporary variables
- Generates appropriate CPU instructions
- Includes function prologue/epilogue (push/pop rbp)
- Handles different operations: ADD, SUB, IMUL, IDIV

---

## Complete Example: `(3 + 5) * 2`

```
PHASE 1: LEXICAL ANALYSIS
Input:  "(3 + 5) * 2"
Output: LPAREN  NUMBER(3)  PLUS  NUMBER(5)  RPAREN  MULTIPLY  NUMBER(2)

PHASE 2: SYNTAX ANALYSIS
Parse Tree:
        *           [Multiplication at root]
       / \
      +   2         [Addition subtree]
     / \
    3   5           [Numbers as leaves]

Why * is root? → Multiply has higher precedence than add

PHASE 3: SEMANTIC ANALYSIS
Evaluate:
├─ (3 + 5) = 8    [parentheses evaluated first]
├─ 8 * 2 = 16     [multiplication second]
Result: 16 ✓

PHASE 4: INTERMEDIATE CODE GENERATION
t1 = 3 + 5
t2 = t1 * 2

PHASE 5: CODE OPTIMIZATION
Constant Folding: 3 + 5 = 8
t1 = 8            [computed at compile time]
t2 = t1 * 2

PHASE 6: CODE GENERATION
mov rax, 8
imul rax, 2
mov rbx, rax
mov rax, rbx
ret
```

---

## How to Use

### Run Complete Compilation:
```bash
cd /workspaces/codespaces-blank
python main.py
```

Output shows all 6 phases with:
- Token list
- Parsing trace
- Parse tree visualization
- Semantic analysis result
- Three-address code (before/after optimization)
- Final assembly code
- Saves assembly to `output_assembly.asm`

### Change Input Expression:
Edit line 18 in [main.py](main.py):
```python
input_text = "3 + 5 * (10 + 122)"  # Change this
```

### Run Syntax Analysis Demo Only:
```bash
python syntax_analyzer_demo.py
```
Shows 3 detailed examples with parse tree visualization and explanations.

---

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | **Complete compiler runner** - runs all 6 phases |
| `lexer.py` | Phase 1: Tokenization |
| `parser.py` | Phase 2: Syntax analysis |
| `parse_tree_visualizer.py` | Enhanced parser with trace and tree visualization |
| `semantic_analyzer.py` | Phase 3: Semantic analysis & evaluation |
| `icg.py` | Phase 4: Intermediate code generation |
| `optimizer.py` | Phase 5: Code optimization |
| `codegen.py` | Phase 6: Code generation (assembly) |
| `ast.py` | AST node definitions (Num, BinOp) |
| `syntax_analyzer_demo.py` | Interactive syntax analysis demonstration |
| `output_assembly.asm` | Generated assembly code (created after each run) |

---

## Key Concepts

### Parse Tree vs AST
- **Parse Tree**: Detailed tree showing all grammar rules applied
- **AST**: Simplified tree with only semantic information
- In this compiler, we build the AST during parsing

### Three-Address Code
- Intermediate representation between AST and assembly
- Each instruction: `variable = operand1 operator operand2`
- Makes optimization easier
- Platform-independent

### Operator Precedence
How compiler evaluates `3 + 5 * 2`:
1. Parse sees * in term() function (higher precedence level)
2. Parse sees + in expr() function (lower precedence level)
3. Creates tree with + at root, * as child
4. This forces: 5*2 first (12), then 3+12 (15)
5. NOT: 3+5 first (8), then 8*2 (16)

### Register Allocation
In code generation:
- `rax`: General purpose register (usually return value)
- `rbx`, `rcx`, `rdx`: Additional general purpose
- `r8-r11`: Additional registers for x86-64

---

## Data Flow Through Compiler

```
Source Code String
    ↓
LEXER ──────────────→ Tokens
    ↓
PARSER ─────────────→ AST + Parse Tree
    ↓
SEMANTIC ANALYZER ──→ Validated + Evaluated Result
    ↓
ICG ────────────────→ Three-Address Code
    ↓
OPTIMIZER ─────────→ Optimized Code
    ↓
CODEGEN ────────────→ Assembly Code
    ↓
output_assembly.asm
```

---

## Example Expressions to Try

1. **Simple**: `2 + 3`
   - Result: 5
   - Tree: `+ node with 2 and 3 as children`

2. **With Precedence**: `2 + 3 * 4`
   - Result: 14 (not 20)
   - Tree: `+ at root, * as right child`

3. **With Parentheses**: `(2 + 3) * 4`
   - Result: 20 (not 14)
   - Tree: `* at root, + as left child`

4. **Complex**: `10 * 2 + 3 / 6 * 2`
   - Left-to-right: `(10*2) + ((3/6)*2) = 20 + 1 = 21`
   - Tree shows correct evaluation order

5. **Nested**: `((5 + 3) * (2 * 4))`
   - Innermost parentheses evaluated first
   - Tree structure shows this clearly

---

## Summary

Your compiler is now complete with all 6 compilation phases:

✅ **Lexical Analysis** - Tokenization  
✅ **Syntax Analysis** - Parse tree with visualization  
✅ **Semantic Analysis** - Validation & evaluation  
✅ **Intermediate Code Generation** - Three-address code  
✅ **Optimization** - Code improvements  
✅ **Code Generation** - Assembly output  

Run `python main.py` to see the complete compilation process!
