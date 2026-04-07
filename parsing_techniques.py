"""
Advanced Parsing Techniques for Compiler Design
- FIRST & FOLLOW sets
- Predictive Parsing Table (LL(1))
- Shift-Reduce Parsing
- LR(0) Items
- LEADING & TRAILING sets
"""


class ParsingTechniques:
    """Comprehensive parsing analysis toolkit"""
    
    def __init__(self, grammar):
        """
        Initialize with grammar dict: {lhs: [rhs1, rhs2, ...]}
        """
        self.grammar = grammar
        self.non_terminals = set(grammar.keys())
        self.terminals = self._extract_terminals()
        self.first_sets = {}
        self.follow_sets = {}
        
    def _extract_terminals(self):
        """Extract all terminal symbols from grammar"""
        terminals = set()
        for lhs, productions in self.grammar.items():
            for rhs in productions:
                if rhs == 'ε':
                    continue
                for symbol in rhs.split():
                    if symbol not in self.non_terminals and symbol != 'ε':
                        terminals.add(symbol)
        terminals.discard('(')
        terminals.discard(')')
        return terminals
    
    def compute_first_sets(self, verbose=True):
        """
        Compute FIRST sets for all non-terminals
        FIRST(A) = set of terminals that can start a derivation from A
        """
        if verbose:
            print("\n🔷 Computing FIRST Sets")
            print("-" * 60)
        
        # Initialize FIRST sets
        for nt in self.non_terminals:
            self.first_sets[nt] = set()
        
        # Add terminals as first sets for themselves
        for terminal in self.terminals:
            if terminal not in self.first_sets:
                self.first_sets[terminal] = {terminal}
        self.first_sets['ε'] = {'ε'}
        
        # Iterate until no changes
        changed = True
        iterations = 0
        while changed:
            changed = False
            iterations += 1
            
            for lhs, productions in self.grammar.items():
                for rhs in productions:
                    if rhs == 'ε':
                        if 'ε' not in self.first_sets[lhs]:
                            self.first_sets[lhs].add('ε')
                            changed = True
                    else:
                        symbols = rhs.split()
                        for symbol in symbols:
                            if symbol in self.first_sets:
                                # Add all non-epsilon from FIRST(symbol)
                                for term in self.first_sets[symbol]:
                                    if term != 'ε' and term not in self.first_sets[lhs]:
                                        self.first_sets[lhs].add(term)
                                        changed = True
                                
                                # If epsilon not in FIRST(symbol), stop
                                if 'ε' not in self.first_sets[symbol]:
                                    break
                            else:
                                if symbol not in self.first_sets[lhs]:
                                    self.first_sets[lhs].add(symbol)
                                    changed = True
                                break
                        else:
                            # All symbols can derive epsilon
                            if 'ε' not in self.first_sets[lhs]:
                                self.first_sets[lhs].add('ε')
                                changed = True
        
        if verbose:
            print(f"Computed in {iterations} iterations\n")
            for nt in sorted(self.non_terminals):
                print(f"FIRST({nt}) = {sorted(self.first_sets[nt])}")
        
        return self.first_sets
    
    def compute_follow_sets(self, start_symbol, verbose=True):
        """
        Compute FOLLOW sets for all non-terminals
        FOLLOW(A) = set of terminals that can follow A in a valid derivation
        """
        if verbose:
            print("\n🔷 Computing FOLLOW Sets")
            print("-" * 60)
        
        # Initialize FOLLOW sets
        for nt in self.non_terminals:
            self.follow_sets[nt] = set()
        
        # Start symbol has $ (end of input) in FOLLOW
        self.follow_sets[start_symbol].add('$')
        
        # Iterate until no changes
        changed = True
        iterations = 0
        while changed:
            changed = False
            iterations += 1
            
            for lhs, productions in self.grammar.items():
                for rhs in productions:
                    if rhs == 'ε':
                        continue
                    
                    symbols = rhs.split()
                    for i, symbol in enumerate(symbols):
                        if symbol in self.non_terminals:
                            # Get symbols after current symbol
                            beta = symbols[i+1:] if i+1 < len(symbols) else []
                            
                            if not beta:
                                # Nothing after, add FOLLOW(lhs) to FOLLOW(symbol)
                                for term in self.follow_sets[lhs]:
                                    if term not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(term)
                                        changed = True
                            else:
                                # Add FIRST(beta) - {ε} to FOLLOW(symbol)
                                beta_str = ' '.join(beta)
                                first_beta = self._get_first(beta_str)
                                
                                for term in first_beta:
                                    if term != 'ε' and term not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(term)
                                        changed = True
                                
                                # If epsilon in FIRST(beta), add FOLLOW(lhs)
                                if 'ε' in first_beta:
                                    for term in self.follow_sets[lhs]:
                                        if term not in self.follow_sets[symbol]:
                                            self.follow_sets[symbol].add(term)
                                            changed = True
        
        if verbose:
            print(f"Computed in {iterations} iterations\n")
            for nt in sorted(self.non_terminals):
                print(f"FOLLOW({nt}) = {sorted(self.follow_sets[nt])}")
        
        return self.follow_sets
    
    def _get_first(self, symbols_str):
        """Get FIRST of a sequence of symbols"""
        if not symbols_str or symbols_str == 'ε':
            return {'ε'}
        
        symbols = symbols_str.split()
        first_set = set()
        
        for symbol in symbols:
            if symbol in self.first_sets:
                for term in self.first_sets[symbol]:
                    if term != 'ε':
                        first_set.add(term)
                
                if 'ε' not in self.first_sets[symbol]:
                    return first_set
            else:
                first_set.add(symbol)
                return first_set
        
        first_set.add('ε')
        return first_set
    
    def build_predictive_table(self, verbose=True):
        """
        Build LL(1) predictive parsing table
        M[A, a] = A -> X1 X2 ... Xn if a is in FIRST(X1 X2 ... Xn)
        """
        if verbose:
            print("\n🔶 Building LL(1) Predictive Parsing Table")
            print("-" * 60)
        
        if not self.first_sets:
            self.compute_first_sets(verbose=False)
        if not self.follow_sets:
            # Find start symbol (usually first in grammar)
            start = list(self.grammar.keys())[0]
            self.compute_follow_sets(start, verbose=False)
        
        table = {}
        conflicts = []
        
        for lhs, productions in self.grammar.items():
            for rhs in productions:
                # Get FIRST(rhs)
                first_rhs = self._get_first(rhs)
                
                # For each terminal in FIRST(rhs)
                for terminal in first_rhs:
                    if terminal != 'ε':
                        key = (lhs, terminal)
                        if key in table:
                            conflicts.append({
                                'key': key,
                                'prod1': table[key],
                                'prod2': f"{lhs} → {rhs}"
                            })
                        table[key] = f"{lhs} → {rhs}"
                
                # If epsilon in FIRST(rhs), add FOLLOW(lhs)
                if 'ε' in first_rhs:
                    for terminal in self.follow_sets[lhs]:
                        key = (lhs, terminal)
                        if key in table:
                            conflicts.append({
                                'key': key,
                                'prod1': table[key],
                                'prod2': f"{lhs} → {rhs}"
                            })
                        table[key] = f"{lhs} → {rhs}"
        
        if verbose:
            print(f"\nPredictive Table Entries: {len(table)}")
            if conflicts:
                print(f"⚠️  Conflicts detected: {len(conflicts)}")
                for conf in conflicts[:3]:
                    print(f"  {conf['key']}: {conf['prod1']} vs {conf['prod2']}")
            else:
                print("✓ No conflicts - Grammar is LL(1)")
            
            print("\nPredictive Parsing Table:")
            print(f"{'Non-Term':<10} {'Terminal':<10} {'Production':<30}")
            print("-" * 50)
            for (nt, term), prod in sorted(table.items()):
                print(f"{nt:<10} {term:<10} {prod:<30}")
        
        return table, conflicts
    
    def build_lr0_items(self, verbose=True):
        """
        Build LR(0) items for shift-reduce parsing
        An item is: A → α · β [lookahead]
        The dot indicates how much of the production has been parsed
        """
        if verbose:
            print("\n🟡 Building LR(0) Items")
            print("-" * 60)
        
        items = {}
        item_id = 0
        
        for lhs, productions in self.grammar.items():
            for rhs in productions:
                symbols = rhs.split() if rhs != 'ε' else []
                
                # Item 0: nothing parsed yet
                item = f"{lhs} → · {' '.join(symbols)}"
                items[item_id] = item
                item_id += 1
                
                # Items with dot at different positions
                for i in range(len(symbols)):
                    before_dot = ' '.join(symbols[:i])
                    after_dot = ' '.join(symbols[i:])
                    item = f"{lhs} → {before_dot} · {after_dot}".replace('  ', ' ').strip()
                    items[item_id] = item
                    item_id += 1
                
                # Item at end (completely parsed)
                item = f"{lhs} → {' '.join(symbols)} ·"
                items[item_id] = item
                item_id += 1
        
        if verbose:
            print(f"Total LR(0) Items: {len(items)}\n")
            for item_id, item in sorted(items.items()):
                print(f"  [{item_id}] {item}")
        
        return items
    
    def get_shift_reduce_actions(self, verbose=True):
        """
        Determine shift/reduce/accept actions for parsing
        """
        if verbose:
            print("\n🟢 Shift-Reduce Action Analysis")
            print("-" * 60)
        
        actions = {
            'shift': [],
            'reduce': [],
            'accept': []
        }
        
        # Any item with dot not at end can shift
        lr0_items = self.build_lr0_items(verbose=False)
        
        shift_items = []
        reduce_items = []
        
        for item_id, item in lr0_items.items():
            if '·' in item and item[-1] != '·':
                shift_items.append(item)
                after_dot = item.split('·')[1].strip()
                if after_dot:
                    next_symbol = after_dot.split()[0]
                    actions['shift'].append(f"Shift on '{next_symbol}' (from {item})")
            elif item[-1] == '·':
                reduce_items.append(item)
                production = item.replace('·', '').strip()
                if production:
                    actions['reduce'].append(f"Reduce using: {production}")
        
        # S' → S · is accept action
        actions['accept'].append("Accept when start symbol → complete ·")
        
        if verbose:
            print(f"\n📌 Shift Actions: {len(shift_items)}")
            for action in actions['shift'][:5]:
                print(f"  {action}")
            if len(shift_items) > 5:
                print(f"  ... and {len(shift_items) - 5} more")
            
            print(f"\n📌 Reduce Actions: {len(reduce_items)}")
            for action in actions['reduce'][:5]:
                print(f"  {action}")
            if len(reduce_items) > 5:
                print(f"  ... and {len(reduce_items) - 5} more")
            
            print(f"\n📌 Accept Action:")
            for action in actions['accept']:
                print(f"  {action}")
        
        return actions
    
    def compute_leading_trailing(self, verbose=True):
        """
        LEADING & TRAILING sets for advanced parsing
        LEADING(A) = terminals that can appear at the start of any sentential form derivable from A
        TRAILING(A) = terminals that can follow derivation from A
        """
        if verbose:
            print("\n🔵 Computing LEADING & TRAILING Sets")
            print("-" * 60)
        
        leading = {nt: set() for nt in self.non_terminals}
        trailing = {nt: set() for nt in self.non_terminals}
        
        # LEADING for terminals is themselves
        for terminal in self.terminals:
            leading[terminal] = {terminal}
        
        # Compute LEADING (similar to FIRST)
        changed = True
        iterations = 0
        while changed:
            changed = False
            iterations += 1
            for lhs, productions in self.grammar.items():
                for rhs in productions:
                    if rhs == 'ε':
                        continue
                    first_sym = rhs.split()[0]
                    if first_sym in leading:
                        for term in leading[first_sym]:
                            if term not in leading[lhs]:
                                leading[lhs].add(term)
                                changed = True
        
        # Compute TRAILING (similar to FOLLOW)
        if not self.follow_sets:
            start = list(self.grammar.keys())[0]
            self.compute_follow_sets(start, verbose=False)
        
        trailing = {nt: self.follow_sets[nt].copy() for nt in self.non_terminals}
        
        if verbose:
            print(f"Computed in {iterations} iterations\n")
            print("LEADING Sets:")
            for nt in sorted(self.non_terminals):
                print(f"  LEADING({nt}) = {sorted(leading[nt])}")
            print("\nTRAILING Sets:")
            for nt in sorted(self.non_terminals):
                print(f"  TRAILING({nt}) = {sorted(trailing[nt])}")
        
        return leading, trailing


if __name__ == '__main__':
    # Example grammar
    grammar = {
        'E': ['T E\''],
        'E\'': ['+ T E\'', '- T E\'', 'ε'],
        'T': ['F T\''],
        'T\'': ['* F T\'', '/ F T\'', 'ε'],
        'F': ['( E )', 'id', 'num']
    }
    
    pt = ParsingTechniques(grammar)
    
    print("\n" + "="*60)
    print("PARSING TECHNIQUES DEMO")
    print("="*60)
    
    # Compute FIRST sets
    pt.compute_first_sets()
    
    # Compute FOLLOW sets
    pt.compute_follow_sets('E')
    
    # Build predictive table
    table, conflicts = pt.build_predictive_table()
    
    # Build LR(0) items
    pt.build_lr0_items()
    
    # Shift-reduce analysis
    pt.get_shift_reduce_actions()
    
    # LEADING & TRAILING
    pt.compute_leading_trailing()
