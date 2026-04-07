# QUICK START GUIDE - 6-Phase Compiler

## 🚀 Quick Start

### Run the Complete Compiler (All 6 Phases):
```bash
python main.py
```

This executes:
1. **Lexical Analysis** - Tokenization
2. **Syntax Analysis** - Parse tree with visualization
3. **Semantic Analysis** - Expression evaluation
4. **Intermediate Code Generation** - Three-address code
5. **Code Optimization** - Constant folding and dead code elimination
6. **Code Generation** - x86-64 assembly

### Output Includes:
✅ Token stream  
✅ Parsing process trace with token consumption  
✅ Parse tree visualization  
✅ Tree structure representation  
✅ Semantic analysis result  
✅ Three-address code (before optimization)  
✅ Optimized code  
✅ Generated assembly code  
✅ Saved assembly file (`output_assembly.asm`)  

---

## 📝 Example Output

For input `(3 + 5) * 2`:

```
PHASE 1: LEXICAL ANALYSIS
Tokens: LPAREN(  NUMBER(3)  PLUS(+)  NUMBER(5)  RPAREN)  MULTIPLY(*)  NUMBER(2)

PHASE 2: SYNTAX ANALYSIS
Parse Tree:
  └── OP: *
      ├── OP: +
      │   ├── NUM: 3
      │   └── NUM: 5
      └── NUM: 2

PHASE 3: SEMANTIC ANALYSIS
Expression evaluates to: 16

PHASE 4: INTERMEDIATE CODE GENERATION
t1 = 3 + 5
t2 = t1 * 2

PHASE 5: CODE OPTIMIZATION
t1 = 8
t2 = t1 * 2

PHASE 6: CODE GENERATION
mov rax, 8
imul rax, 2
mov rbx, rax
mov rax, rbx
ret
```

---

## 🎯 Key Features

### Parse Tree with Tracing
Shows EXACTLY how parser processes tokens:
- Token consumption order
- Function calls (expr → term → factor)
- BinOp node creation
- Precedence handling

### Syntax Analysis Visualization
```
Parse Tree:        
  └── OP: *           ← Root (evaluated last)
      ├── OP: +       ← Left subtree (evaluated first)
      │   ├── NUM: 3
      │   └── NUM: 5
      └── NUM: 2      ← Right leaf
```

### Code Optimization
Applied optimizations:
- **Constant Folding**: `3 + 5 → 8` (computed at compile time)
- **Dead Code Elimination**: Remove unused variables
- **Common Subexpression Elimination**: Reuse computations

---

## 📂 All Files

| File | Purpose |
|------|---------|
| **main.py** | Main compiler runner - runs all 6 phases |
| lexer.py | Lexical analyzer (tokenizer) |
| parser.py | Syntax analyzer basic parser |
| parse_tree_visualizer.py | Enhanced parser with trace & visualization |
| semantic_analyzer.py | Semantic analyzer with evaluation |
| icg.py | Intermediate code generation |
| optimizer.py | Code optimizer |
| codegen.py | Code generator (assembly) |
| ast.py | AST node definitions |
| syntax_analyzer_demo.py | Detailed syntax analysis demo |
| COMPLETE_COMPILER_GUIDE.md | Comprehensive documentation |
| output_assembly.asm | Generated assembly (created after each run) |

---

## 🔧 How to Use

### 1. Run Compiler with Default Expression:
```bash
python main.py
```
Current: `3 + 5 * (10 + 122)`

### 2. Modify Input Expression:
Edit line 18 in `main.py`:
```python
input_text = "YOUR_EXPRESSION_HERE"
```

Examples to try:
- `2 + 3`
- `2 + 3 * 4`
- `(2 + 3) * 4`
- `10 / 2 - 1`
- `((2 + 3) * (4 - 1))`

### 3. Run Syntax Analysis Demo:
```bash
python syntax_analyzer_demo.py
```
Shows 3 detailed examples with explanations.

### 4. View Generated Assembly:
```bash
cat output_assembly.asm
```

---

## 📊 Compilation Flow

```
Input Expression
    ↓
[LEXER] → Token Stream
    ↓
[PARSER] → Parse Tree
    ↓
[SEMANTIC ANALYZER] → Validated & Evaluated
    ↓
[ICG] → Three-Address Code
    ↓
[OPTIMIZER] → Optimized Code
    ↓
[CODEGEN] → Assembly Code
    ↓
output_assembly.asm
```

---

## 💡 Understanding Parse Trees

### Why Operator at Root?
```
Expression: 3 + 5 * 2

Parse Tree:       +          ← Added LAST (root)
                 / \
                3   *        ← Multiplied FIRST (right child)
                   / \
                  5   2

Reason: * has higher precedence
Evaluation: (5*2=10) then (3+10=13)
```

### Why Parentheses Matter?
```
Expression: (3 + 5) * 2

Parse Tree:       *          ← Multiply LAST (root)
                 / \
                +   2        ← Add FIRST (left child)
               / \
              3   5

Evaluation: (3+5=8) then (8*2=16)
```

---

## ⚙️ Optimization Example

### Constant Folding:
```
Before: t1 = 10 + 122
After:  t1 = 132
(Computed at compile time, not runtime)
```

### Assembly Impact:
```
Before: MOV rax, 10
        MOV rbx, 122
        ADD rax, rbx        ← Runtime computation

After:  MOV rax, 132        ← Direct value (optimized)
(Much faster!)
```

---

## 🐛 Troubleshooting

### ERROR: Module not found
```bash
# Ensure you're in the right directory
cd /workspaces/codespaces-blank
python main.py
```

### Invalid syntax error
```
# Check your expression only uses: numbers, +, -, *, /, ()
# Valid: 3 + 5 * (2 - 1)
# Invalid: 3 + a * 2  (no variables yet)
```

### Assembly file not created
Assembly is saved after successful compilation. Check console output for errors.

---

## 📚 Learn More

Read the detailed guides:
- `COMPLETE_COMPILER_GUIDE.md` - Full explanation of all 6 phases
- `SYNTAX_ANALYZER_GUIDE.md` - Deep dive into parsing and parse trees

---

## 🎓 Key Concepts

| Phase | Input | Output | Purpose |
|-------|-------|--------|---------|
| 1. Lexical | Source code | Tokens | Break into units |
| 2. Syntax | Tokens | AST + Parse Tree | Verify grammar |
| 3. Semantic | AST | Result + Validation | Type checking |
| 4. ICG | AST | Three-Address Code | Intermediate form |
| 5. Optimization | TAC | Optimized TAC | Improve code |
| 6. CodeGen | Optimized TAC | Assembly | Machine code |

---

## ✨ Summary

Your complete 6-phase compiler is ready!

**Run:** `python main.py`

**See:** All phases execute with detailed output, parse tree visualization, and assembly generation.

**Learn:** Read COMPLETE_COMPILER_GUIDE.md for deep explanations.
