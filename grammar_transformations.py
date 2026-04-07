"""
Grammar Transformation Techniques for Compiler Design
- Ambiguity Removal
- Left Recursion Elimination
- Left Factoring
"""


class Production:
    """Represents a grammar production rule: A -> body"""
    def __init__(self, lhs, rhs_list):
        self.lhs = lhs
        self.rhs_list = rhs_list  # List of alternative productions

    def __repr__(self):
        rhs_str = " | ".join(self.rhs_list)
        return f"{self.lhs} → {rhs_str}"

    def __str__(self):
        return self.__repr__()


class Grammar:
    """Represents a context-free grammar"""
    def __init__(self, productions, start_symbol):
        self.productions = productions  # dict: {lhs -> Production}
        self.start_symbol = start_symbol

    def __repr__(self):
        result = []
        for non_terminal in sorted(self.productions.keys()):
            result.append(str(self.productions[non_terminal]))
        return "\n".join(result)

    def get_productions(self, lhs):
        """Get all productions for a non-terminal"""
        if lhs in self.productions:
            return self.productions[lhs].rhs_list
        return []

    def add_production(self, lhs, rhs_list):
        """Add or update a production"""
        self.productions[lhs] = Production(lhs, rhs_list)


def detect_ambiguity(grammar):
    """
    Detect ambiguous productions in grammar.
    An ambiguous grammar can generate the same string with multiple parse trees.
    """
    print("\n🔍 AMBIGUITY DETECTION")
    print("-" * 60)
    
    ambiguities = []
    
    for lhs, production in grammar.productions.items():
        rhs_list = production.rhs_list
        
        # Check for duplicate productions
        seen = {}
        for rhs in rhs_list:
            if rhs in seen:
                ambiguities.append({
                    'type': 'Duplicate',
                    'lhs': lhs,
                    'production': rhs,
                    'issue': 'Same production appears multiple times'
                })
            seen[rhs] = True
        
        # Check for productions with overlapping prefixes
        for i, rhs1 in enumerate(rhs_list):
            for j, rhs2 in enumerate(rhs_list):
                if i < j:
                    # Find common prefix
                    tokens1 = rhs1.split()
                    tokens2 = rhs2.split()
                    
                    common_len = 0
                    for t1, t2 in zip(tokens1, tokens2):
                        if t1 == t2:
                            common_len += 1
                        else:
                            break
                    
                    if common_len > 0 and common_len < min(len(tokens1), len(tokens2)):
                        ambiguities.append({
                            'type': 'Overlapping Prefix',
                            'lhs': lhs,
                            'prod1': rhs1,
                            'prod2': rhs2,
                            'issue': f"Common prefix: {' '.join(tokens1[:common_len])}"
                        })
    
    return ambiguities


def remove_ambiguity(grammar, ambiguities):
    """
    Remove ambiguity from grammar by adding precedence/associativity rules
    or restructuring productions
    """
    print("\n✓ AMBIGUITY REMOVAL")
    print("-" * 60)
    
    if not ambiguities:
        print("✓ No ambiguities detected!")
        return grammar
    
    print(f"Found {len(ambiguities)} potential ambiguities:\n")
    
    for i, amb in enumerate(ambiguities, 1):
        if amb['type'] == 'Duplicate':
            print(f"{i}. Duplicate production:")
            print(f"   Rule: {amb['lhs']} → {amb['production']}")
            print(f"   Action: Remove duplicate")
        elif amb['type'] == 'Overlapping Prefix':
            print(f"{i}. Overlapping prefix ambiguity:")
            print(f"   Rule: {amb['lhs']} → {amb['prod1']} | {amb['prod2']}")
            print(f"   Issue: {amb['issue']}")
            print(f"   Action: Apply left factoring")
        print()
    
    # Clean up duplicates
    cleaned_grammar = Grammar({}, grammar.start_symbol)
    for lhs, production in grammar.productions.items():
        unique_rhs = list(dict.fromkeys(production.rhs_list))  # Remove duplicates
        cleaned_grammar.add_production(lhs, unique_rhs)
    
    return cleaned_grammar


def detect_left_recursion(grammar):
    """
    Detect immediate left recursion in grammar.
    A production A → A α is immediately left recursive.
    """
    print("\n🔍 LEFT RECURSION DETECTION")
    print("-" * 60)
    
    left_recursive = {}
    
    for lhs, production in grammar.productions.items():
        recursive_prods = []
        non_recursive_prods = []
        
        for rhs in production.rhs_list:
            tokens = rhs.split()
            if tokens and tokens[0] == lhs:
                recursive_prods.append(rhs)
            else:
                non_recursive_prods.append(rhs)
        
        if recursive_prods:
            left_recursive[lhs] = {
                'recursive': recursive_prods,
                'non_recursive': non_recursive_prods
            }
    
    return left_recursive


def eliminate_left_recursion(grammar):
    """
    Eliminate immediate left recursion using standard transformation.
    
    For A → A α | β, replace with:
    A → β A'
    A' → α A' | ε
    """
    print("\n✓ LEFT RECURSION ELIMINATION")
    print("-" * 60)
    
    left_recursive = detect_left_recursion(grammar)
    
    if not left_recursive:
        print("✓ No left recursion detected!")
        return grammar
    
    new_grammar = Grammar({}, grammar.start_symbol)
    prime_counter = {}
    
    for lhs, production in grammar.productions.items():
        if lhs not in left_recursive:
            # No left recursion, keep as is
            new_grammar.add_production(lhs, production.rhs_list)
        else:
            lr_info = left_recursive[lhs]
            recursive_prods = lr_info['recursive']
            non_recursive_prods = lr_info['non_recursive']
            
            print(f"\nOriginal: {lhs} → {' | '.join(production.rhs_list)}")
            
            # Create new non-terminal A'
            if lhs not in prime_counter:
                prime_counter[lhs] = 0
            prime_counter[lhs] += 1
            new_nt = f"{lhs}'"
            
            # Remove left recursion: A → β A'
            new_a_prods = []
            for beta in non_recursive_prods:
                new_a_prods.append(f"{beta} {new_nt}")
            new_grammar.add_production(lhs, new_a_prods)
            
            # Create A' → α A' | ε
            new_a_prime_prods = []
            for recursive_prod in recursive_prods:
                # Remove leading A
                alpha = ' '.join(recursive_prod.split()[1:])
                if alpha:
                    new_a_prime_prods.append(f"{alpha} {new_nt}")
            new_a_prime_prods.append("ε")  # Add epsilon production
            new_grammar.add_production(new_nt, new_a_prime_prods)
            
            print(f"Transformed:")
            print(f"  {lhs} → {' | '.join(new_a_prods)}")
            print(f"  {new_nt} → {' | '.join(new_a_prime_prods)}")
    
    return new_grammar


def detect_left_factoring_issues(grammar):
    """
    Detect productions that need left factoring.
    Productions with common prefixes need factoring.
    """
    print("\n🔍 LEFT FACTORING DETECTION")
    print("-" * 60)
    
    factoring_needed = {}
    
    for lhs, production in grammar.productions.items():
        rhs_list = production.rhs_list
        groups = {}
        
        for rhs in rhs_list:
            tokens = rhs.split()
            first_token = tokens[0] if tokens else "ε"
            
            if first_token not in groups:
                groups[first_token] = []
            groups[first_token].append(rhs)
        
        # Find tokens with multiple productions
        for first_token, prods in groups.items():
            if len(prods) > 1:
                if lhs not in factoring_needed:
                    factoring_needed[lhs] = []
                factoring_needed[lhs].append({
                    'first_token': first_token,
                    'productions': prods
                })
    
    return factoring_needed


def apply_left_factoring(grammar):
    """
    Apply left factoring transformation.
    For A → α β | α γ, replace with:
    A → α A'
    A' → β | γ
    """
    print("\n✓ LEFT FACTORING")
    print("-" * 60)
    
    factoring_needed = detect_left_factoring_issues(grammar)
    
    if not factoring_needed:
        print("✓ No left factoring needed!")
        return grammar
    
    new_grammar = Grammar({}, grammar.start_symbol)
    prime_counter = {}
    
    for lhs, production in grammar.productions.items():
        if lhs not in factoring_needed:
            # No factoring needed, keep as is
            new_grammar.add_production(lhs, production.rhs_list)
        else:
            factoring_info = factoring_needed[lhs]
            result_prods = []
            processed_prods = set()
            
            print(f"\nOriginal: {lhs} → {' | '.join(production.rhs_list)}")
            
            for rhs in production.rhs_list:
                if rhs in processed_prods:
                    continue
                
                tokens = rhs.split()
                first_token = tokens[0] if tokens else "ε"
                
                # Find all productions with same first token
                prods_with_first = []
                for alt_rhs in production.rhs_list:
                    alt_tokens = alt_rhs.split()
                    alt_first = alt_tokens[0] if alt_tokens else "ε"
                    if alt_first == first_token:
                        prods_with_first.append(alt_rhs)
                
                if len(prods_with_first) > 1:
                    # Need factoring
                    if lhs not in prime_counter:
                        prime_counter[lhs] = 0
                    prime_counter[lhs] += 1
                    new_nt = f"{lhs}'{prime_counter[lhs]}"
                    
                    # A → α A'
                    result_prods.append(f"{first_token} {new_nt}")
                    
                    # A' → β | γ | ...
                    alt_prods = []
                    for prod in prods_with_first:
                        alt_tokens = prod.split()
                        rest = ' '.join(alt_tokens[1:]) if len(alt_tokens) > 1 else "ε"
                        alt_prods.append(rest)
                        processed_prods.add(prod)
                    
                    new_grammar.add_production(new_nt, alt_prods)
                    
                    print(f"  Factored: {lhs} → {first_token} {new_nt}")
                    print(f"  {new_nt} → {' | '.join(alt_prods)}")
                else:
                    # No factoring needed for this production
                    result_prods.append(rhs)
                    processed_prods.add(rhs)
            
            new_grammar.add_production(lhs, result_prods)
    
    return new_grammar


def print_grammar_summary(original, transformed, title):
    """Print before/after comparison"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print("\nOriginal Grammar:")
    print(original)
    print("\nTransformed Grammar:")
    print(transformed)


if __name__ == '__main__':
    # Example: Simple arithmetic expression grammar with ambiguity and left recursion
    productions = {
        'E': Production('E', ['E + T', 'T']),
        'T': Production('T', ['T * F', 'F']),
        'F': Production('F', ['( E )', 'id'])
    }
    
    grammar = Grammar(productions, 'E')
    
    print("\n" + "="*60)
    print("GRAMMAR TRANSFORMATION DEMO")
    print("="*60)
    
    # Test ambiguity removal
    ambiguities = detect_ambiguity(grammar)
    clean_grammar = remove_ambiguity(grammar, ambiguities)
    
    # Test left recursion elimination
    lr_grammar = eliminate_left_recursion(clean_grammar)
    
    # Test left factoring
    factored_grammar = apply_left_factoring(lr_grammar)
    
    print("\n" + "="*60)
    print("FINAL TRANSFORMED GRAMMAR")
    print("="*60)
    print(factored_grammar)
