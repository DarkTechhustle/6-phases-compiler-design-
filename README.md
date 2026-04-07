# 🎓 Complete 6-Phase Compiler Implementation

A fully functional compiler that demonstrates all 6 phases of compilation with detailed visualization of the parse tree and optimization process.

## ✨ What You Have

A complete, working compiler that transforms source code through 6 compilation phases:

```
Source Code 
    ↓
📝 Phase 1: Lexical Analysis (Tokenization)
    ↓
🌳 Phase 2: Syntax Analysis (Parsing & Parse Tree)
    ↓
✓ Phase 3: Semantic Analysis (Validation & Evaluation)
    ↓
⚙️  Phase 4: Intermediate Code Generation (Three-Address Code)
    ↓
🚀 Phase 5: Code Optimization (Constant Folding, Dead Code Elimination)
    ↓
🔧 Phase 6: Code Generation (x86-64 Assembly)
    ↓
Machine-Executable Code
```

## 🚀 Quick Start

### Run the Complete Compiler:
```bash
python main.py
```

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| **QUICK_START.md** | Start here! Quick reference guide |
| **COMPLETE_COMPILER_GUIDE.md** | Detailed explanation of all 6 phases |
| **SYNTAX_ANALYZER_GUIDE.md** | Deep dive into parsing and parse trees |

---

## 🔧 Compiler Files

### Core Compiler Phases:
| File | Phase | Purpose |
|------|-------|---------|
| `lexer.py` | 1 | Tokenization - breaks input into tokens |
| `parser.py` | 2 | Basic syntax analysis |
| `parse_tree_visualizer.py` | 2 | Enhanced parser with visualization |
| `semantic_analyzer.py` | 3 | Semantic analysis & evaluation |
| `icg.py` | 4 | Intermediate code generation |
| `optimizer.py` | 5 | Code optimization |
| `codegen.py` | 6 | Assembly code generation |

### Support Files:
| File | Purpose |
|------|---------|
| `ast.py` | AST node definitions (Num, BinOp) |
| `main.py` | Main compiler runner - **RUN THIS!** |
| `syntax_analyzer_demo.py` | Interactive syntax analysis demo |

---

## 📖 Understanding the Compiler

### Phase 1: Lexical Analysis
```
Input:  "3 + 5 * (10 + 2)"
Output: NUMBER(3) PLUS(+) NUMBER(5) MULTIPLY(*) LPAREN(() NUMBER(10) PLUS(+) NUMBER(2) RPAREN())
```

### Phase 2: Syntax Analysis with Parse Tree
```
Parse Tree:        *           [Multiplication at root = evaluated last]
                  / \
                 +   2        [Addition subtree = evaluated first]
                / \
               3   5          [Numbers as leaves]

Key: Tree structure shows evaluation order due to operator precedence!
```

### Phase 3: Semantic Analysis
```
AST Evaluation: 3 + 5 * (10 + 2)
├─ (10 + 2) = 12
├─ 5 * 12 = 60
└─ 3 + 60 = 63 ✓
```

### Phase 4: Intermediate Code Generation
```
t1 = 10 + 2
t2 = 5 * t1
t3 = 3 + t2
```

### Phase 5: Code Optimization
```
t1 = 12          [Constant folding: 10 + 2 = 12]
t2 = 5 * t1
t3 = 3 + t2
```

### Phase 6: Code Generation
```
mov rax, 12
imul rax, 5
mov rbx, rax
mov rax, 3
add rax, rbx
mov rcx, rax
```

---

## 💡 Parse Trees & Operator Precedence

### Why `3 + 5 * 2 = 13` (not 16)?
```
Parse Tree:       +           [Addition at root = evaluated LAST]
                 / \
                3   *         [Multiplication as child = evaluated FIRST]
                   / \
                  5   2

Evaluation: (5 * 2 = 10), then (3 + 10 = 13) ✓
```

### With Parentheses `(3 + 5) * 2 = 16`:
```
Parse Tree:       *           [Multiplication at root]
                 / \
                +   2         [Addition as child]
               / \
              3   5

Evaluation: (3 + 5 = 8), then (8 * 2 = 16) ✓
```

---

## 🎯 Try These Examples

### Simple Addition:
```python
input_text = "2 + 3"
# Result: 5
```

### With Precedence:
```python
input_text = "2 + 3 * 4"
# Result: 14 (not 20, because * has higher precedence)
```

### With Parentheses:
```python
input_text = "(2 + 3) * 4"
# Result: 20 (parentheses override precedence)
```

### Complex Expression:
```python
input_text = "10 * 2 + 3 / 6 * 2"
# Result: 21 (left to right evaluation)
```

---

## ⚙️ Grammar Rules

```
expr   → term ((PLUS | MINUS) term)*
term   → factor ((MULTIPLY | DIVIDE) factor)*
factor → NUMBER | LPAREN expr RPAREN

Precedence (highest to lowest):
1. Parentheses ( )
2. Multiply/Divide * /
3. Plus/Minus + -
```

---

## 📝 Supported Operations

**Operators:** `+`, `-`, `*`, `/`  
**Grouping:** `(` `)`  
**Literals:** Integer numbers  

Valid expressions:
- `3 + 5`
- `2 * 3 + 4`
- `(3 + 5) * 2`
- `10 / 2 - 3`
- `((2 + 3) * (4 - 1))`

---

## 🚀 Usage

### 1. Run Compiler with Default Expression:
```bash
python main.py
```

### 2. Modify Input Expression:
Edit line 18 in `main.py`:
```python
input_text = "YOUR_EXPRESSION_HERE"
```

### 3. Run Syntax Analysis Demo:
```bash
python syntax_analyzer_demo.py
```

### 4. View Generated Assembly:
```bash
cat output_assembly.asm
```

---

## ✨ Features

✅ **Complete 6-Phase Pipeline**: All compiler phases  
✅ **Parse Tree Visualization**: See operator hierarchy  
✅ **Parsing Trace**: Watch token consumption  
✅ **Code Optimization**: Multiple optimization techniques  
✅ **Assembly Generation**: x86-64 executable code  
✅ **Comprehensive Guides**: Learn how it all works  
✅ **Interactive Demos**: Try different expressions  

---

## 📊 Project Structure

```
/workspaces/codespaces-blank/
├── 📚 Guides
│   ├── README.md                     (Overview)
│   ├── QUICK_START.md               (Quick reference)
│   ├── COMPLETE_COMPILER_GUIDE.md   (All 6 phases)
│   └── SYNTAX_ANALYZER_GUIDE.md     (Parse trees)
│
├── 🔧 Compiler Phases (1-6)
│   ├── lexer.py                     (Phase 1)
│   ├── parser.py                    (Phase 2 - basic)
│   ├── parse_tree_visualizer.py     (Phase 2 - enhanced)
│   ├── semantic_analyzer.py         (Phase 3)
│   ├── icg.py                       (Phase 4)
│   ├── optimizer.py                 (Phase 5)
│   └── codegen.py                   (Phase 6)
│
├── 🆘 Support
│   ├── ast.py                       (AST definitions)
│   ├── main.py                      (Main runner ← RUN THIS)
│   ├── syntax_analyzer_demo.py      (Interactive demo)
│   └── output_assembly.asm          (Generated output)
```

---

## 📞 Help & Resources

- **Start here?** → `QUICK_START.md`
- **All phases explained?** → `COMPLETE_COMPILER_GUIDE.md`
- **Parse tree guide?** → `SYNTAX_ANALYZER_GUIDE.md`
- **Run demo?** → `python syntax_analyzer_demo.py`
- **See result?** → `cat output_assembly.asm`

---

## 🎓 What You Learn

Understanding this compiler teaches:

1. **Lexical Analysis**: Tokenization patterns
2. **Syntax Analysis**: Recursive descent parsing, operator precedence, parse trees
3. **Semantic Analysis**: AST traversal, expression evaluation
4. **Intermediate Code**: Three-address code representation
5. **Optimization**: Code improvement techniques
6. **Code Generation**: Assembly instruction generation

---

## 🎉 Summary

**You now have a complete 6-phase compiler!**

- Phase 1: Lexical Analysis ✓
- Phase 2: Syntax Analysis with Parse Tree ✓
- Phase 3: Semantic Analysis ✓
- Phase 4: Intermediate Code Generation ✓
- Phase 5: Code Optimization ✓
- Phase 6: Code Generation ✓

**Run it:** `python main.py`

**Learn more:** Read the guide files

---

**Status:** Fully Functional ✓  
**Type:** Educational Compiler  
**License:** Open Source

Result: 63