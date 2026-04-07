# main.py
# Complete Compiler with 6 Phases:
# 1. Lexical Analysis
# 2. Syntax Analysis
# 3. Semantic Analysis
# 4. Intermediate Code Generation
# 5. Code Optimization
# 6. Code Generation

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from icg import IntermediateCodeGenerator, ThreeAddressCode
from optimizer import CodeOptimizer, OptimizedCode
from codegen import CodeGenerator, AssemblyCode
from parse_tree_visualizer import ParseTreeVisualizer, TreePrinter
from automata import nfa_to_dfa, regex_to_nfa, visualize_nfa, visualize_dfa
from grammar_transformations import Grammar, Production, detect_ambiguity, remove_ambiguity, eliminate_left_recursion, apply_left_factoring
from parsing_techniques import ParsingTechniques
from advanced_optimization import (NotationConverter, IntermediateCodeFormats, 
                                    DAGOptimizer, DataFlowAnalyzer, StorageAllocator)

def main():
    # Sample input
    input_text = "3 + 6 * (10 + 122)"
    
    print("="*60)
    print("COMPLETE COMPILER - 6 PHASES")
    print("="*60)
    print(f"Input Expression: {input_text}\n")

    # Phase 1: Lexical Analysis
    print("\n" + "="*60)
    print("PHASE 1: LEXICAL ANALYSIS")
    print("="*60)
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    print("Tokens generated:")
    for i, token in enumerate(tokens, 1):
        print(f"  {i}. {token}")

    # Phase 2: Syntax Analysis
    print("\n" + "="*60)
    print("PHASE 2: SYNTAX ANALYSIS (Parser with Parse Tree)")
    print("="*60)
    
    # Parse with visualization
    visualizer = ParseTreeVisualizer(tokens)
    ast = visualizer.parse_with_trace()
    
    print(f"\nAST created: {ast}")
    
    print("\n" + "-"*60)
    print("Parsing Process Trace:")
    print("-"*60)
    visualizer.print_trace()
    
    print("\n" + "-"*60)
    print("Parse Tree Visualization:")
    print("-"*60)
    print()
    visualizer.print_tree(ast)
    
    print("\n" + "-"*60)
    print("Tree Structure Representation:")
    print("-"*60)
    print()
    for line in TreePrinter.get_tree_structure(ast):
        print(line)

    # Phase 3: Semantic Analysis
    print("\n" + "="*60)
    print("PHASE 3: SEMANTIC ANALYSIS")
    print("="*60)
    analyzer = SemanticAnalyzer(ast)
    result = analyzer.analyze()
    print(f"Expression evaluates to: {result}")

    # Phase 4: Intermediate Code Generation
    print("\n" + "="*60)
    print("PHASE 4: INTERMEDIATE CODE GENERATION")
    print("="*60)
    icg = IntermediateCodeGenerator(ast)
    icg_code = icg.generate()
    tac = ThreeAddressCode(icg_code)
    print(tac)

    # Phase 5: Code Optimization
    print("\n" + "="*60)
    print("PHASE 5: CODE OPTIMIZATION")
    print("="*60)
    optimizer = CodeOptimizer(tac)
    optimized = optimizer.optimize()
    opt_code = OptimizedCode(optimized)
    print(opt_code)

    # Phase 6: Code Generation
    print("\n" + "="*60)
    print("PHASE 6: CODE GENERATION (Assembly)")
    print("="*60)
    codegen = CodeGenerator(opt_code)
    assembly = codegen.generate()
    asm_code = AssemblyCode(assembly)
    print(asm_code)
    
    # Save assembly to file
    asm_code.save_to_file("output_assembly.asm")
    
    print("\n" + "="*60)
    print("PHASE 7: GRAMMAR TRANSFORMATIONS")
    print("="*60)
    
    # Create example grammar with issues
    productions = {
        'E': Production('E', ['E + T', 'E - T', 'T']),
        'T': Production('T', ['T * F', 'T / F', 'F']),
        'F': Production('F', ['( E )', 'id', 'num'])
    }
    
    original_grammar = Grammar(productions, 'E')
    
    print("\n📋 Original Grammar (with ambiguity and left recursion):")
    print("-"*60)
    print(original_grammar)
    
    # Step 1: Ambiguity Detection and Removal
    print("\n" + "="*60)
    print("STEP 1: Ambiguity Analysis")
    print("="*60)
    ambiguities = detect_ambiguity(original_grammar)
    clean_grammar = remove_ambiguity(original_grammar, ambiguities)
    
    print("\n✓ Ambiguity Removal Complete")
    print("-"*60)
    print("Cleaned Grammar:")
    print(clean_grammar)
    
    # Step 2: Left Recursion Elimination
    print("\n" + "="*60)
    print("STEP 2: Left Recursion Elimination")
    print("="*60)
    lr_free_grammar = eliminate_left_recursion(clean_grammar)
    
    print("\n✓ Left Recursion Elimination Complete")
    print("-"*60)
    print("Left-Recursion-Free Grammar:")
    print(lr_free_grammar)
    
    # Step 3: Left Factoring
    print("\n" + "="*60)
    print("STEP 3: Left Factoring")
    print("="*60)
    factored_grammar = apply_left_factoring(lr_free_grammar)
    
    print("\n✓ Left Factoring Complete")
    print("-"*60)
    print("Fully Transformed Grammar (LL(1) Compatible):")
    print(factored_grammar)
    
    print("\n" + "="*60)
    print("TRANSFORMATION SUMMARY")
    print("="*60)
    print(f"Original productions: {sum(len(p.rhs_list) for p in original_grammar.productions.values())}")
    print(f"Final productions: {sum(len(p.rhs_list) for p in factored_grammar.productions.values())}")
    print("\n✓ Grammar is now suitable for LL(1) parsing")
    print("="*60)
    
    # Phase 8: Automata Conversion
    print("\n" + "="*60)
    print("PHASE 8: REGULAR EXPRESSION → NFA → DFA")
    print("="*60)
    regex = "a(b|c)*"
    
    print(f"\n📝 Converting Regular Expression: '{regex}'")

    print(f"{'='*60}")
    
    # Step 1: RE to NFA using Thompson's Construction
    print("\nSTEP 1: Thompson's Construction (RE → NFA)")
    print("-"*60)
    nfa = regex_to_nfa(regex)
    print(f"✓ NFA created with {len(nfa.states)} states")
    print(f"  Start: {nfa.start}, Accept: {nfa.accept}")
    visualize_nfa(nfa, "Thompson's NFA")
    
    # Step 2: NFA to DFA using Subset Construction
    print("\nSTEP 2: Subset Construction (NFA → DFA)")
    print("-"*60)
    dfa = nfa_to_dfa(nfa)
    print(f"✓ DFA created with {len(dfa.states)} states")
    print(f"  Start: {dfa.start}, Accept states: {len(dfa.accept_states)}")
    visualize_dfa(dfa, "Subset Construction DFA")
    
    # Step 3: Pattern matching
    print(f"\n{'='*60}")
    print("STEP 3: Pattern Matching with DFA")
    print(f"{'='*60}")
    test_strings = ["a", "ab", "abc", "abcb", "ac", "abb", "b", "", "aa"]
    print(f"\nTesting regex '{regex}' against input strings:\n")
    for sample in test_strings:
        result = dfa.matches(sample)
        status = "✓ MATCH" if result else "✗ NO MATCH"
        print(f"  Input: {sample!r:8} → {status}")
    
    # Phase 9: Advanced Parsing Techniques
    print("\n" + "="*60)
    print("PHASE 9: ADVANCED PARSING TECHNIQUES")
    print("="*60)
    
    # Grammar for parsing analysis
    grammar_dict = {
        'E': ['T E\''],
        'E\'': ['+ T E\'', '- T E\'', 'ε'],
        'T': ['F T\''],
        'T\'': ['* F T\'', '/ F T\'', 'ε'],
        'F': ['( E )', 'id', 'num']
    }
    
    pt = ParsingTechniques(grammar_dict)
    
    print("\n📋 Grammar for Analysis:")
    print("-"*60)
    for lhs, productions in grammar_dict.items():
        rhs_str = " | ".join(productions)
        print(f"  {lhs} → {rhs_str}")
    
    # 1. FIRST sets
    print("\n" + "="*60)
    print("TECHNIQUE 1: FIRST SETS")
    print("="*60)
    first_sets = pt.compute_first_sets()
    
    # 2. FOLLOW sets
    print("\n" + "="*60)
    print("TECHNIQUE 2: FOLLOW SETS")
    print("="*60)
    follow_sets = pt.compute_follow_sets('E')
    
    # 3. LL(1) Predictive Parsing Table
    print("\n" + "="*60)
    print("TECHNIQUE 3: LL(1) PREDICTIVE PARSING TABLE")
    print("="*60)
    table, conflicts = pt.build_predictive_table()
    
    # 4. LR(0) Items
    print("\n" + "="*60)
    print("TECHNIQUE 4: LR(0) ITEMS (Shift-Reduce)")
    print("="*60)
    lr0_items = pt.build_lr0_items()
    
    # 5. Shift-Reduce Actions
    print("\n" + "="*60)
    print("TECHNIQUE 5: SHIFT-REDUCE PARSING ACTIONS")
    print("="*60)
    actions = pt.get_shift_reduce_actions()
    
    # 6. LEADING & TRAILING
    print("\n" + "="*60)
    print("TECHNIQUE 6: LEADING & TRAILING SETS")
    print("="*60)
    leading, trailing = pt.compute_leading_trailing()

    # Phase 10: Advanced Optimization & Backend
    print("\n" + "="*60)
    print("PHASE 10: ADVANCED OPTIMIZATION & BACKEND")
    print("="*60)
    
    # 1. Notation Conversion
    print("\n" + "-"*60)
    print("TECHNIQUE 1: NOTATION CONVERSION")
    print("-"*60)
    
    infix = "a + b * c"
    print(f"\n📝 Expression: {infix}")
    postfix = NotationConverter.infix_to_postfix(infix)
    prefix = NotationConverter.infix_to_prefix(infix)
    print(f"  Postfix (RPN): {postfix}")
    print(f"  Prefix (Polish): {prefix}")
    
    # Reverse conversion
    back_to_infix = NotationConverter.postfix_to_infix(postfix)
    print(f"  Back to Infix: {back_to_infix}")
    
    # 2. Intermediate Code Representations
    print("\n" + "-"*60)
    print("TECHNIQUE 2: INTERMEDIATE CODE REPRESENTATIONS")
    print("-"*60)
    
    icf = IntermediateCodeFormats()
    postfix_expr = "a b + c *"
    print(f"\nExpression (postfix): {postfix_expr}")
    icf.generate_quadruple(postfix_expr)
    icf.generate_triple(postfix_expr)
    icf.generate_indirect_triple(postfix_expr)
    
    # 3. DAG-Based Optimization
    print("\n" + "-"*60)
    print("TECHNIQUE 3: DAG-BASED OPTIMIZATION")
    print("-"*60)
    
    dag_opt = DAGOptimizer()
    expr = "a + b * c"
    print(f"\nExpression: {expr}")
    root = dag_opt.build_dag_from_expression(expr)
    dag_opt.dag_to_code(root)
    
    # 4. Global Data Flow Analysis
    print("\n" + "-"*60)
    print("TECHNIQUE 4: GLOBAL DATA FLOW ANALYSIS")
    print("-"*60)
    
    instructions = [
        "a = 5",
        "b = a + 2",
        "c = b * 3",
        "d = c + a"
    ]
    dfa = DataFlowAnalyzer(instructions)
    gen_sets, kill_sets = dfa.analyze_definitions()
    
    # 5. Storage Allocation
    print("\n" + "-"*60)
    print("TECHNIQUE 5: STORAGE ALLOCATION")
    print("-"*60)
    
    variables = ['a', 'b', 'c', 'd', 'e']
    
    print("\n📊 Storage Allocation Strategies:")
    
    sa_stack = StorageAllocator()
    sa_stack.allocate_storage(variables, "stack")
    
    sa_mixed = StorageAllocator()
    sa_mixed.allocate_storage(variables, "mixed")
    
    sa_static = StorageAllocator()
    sa_static.allocate_storage(variables, "static")

    print("\n" + "="*60)
    print("COMPILATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()