from collections import deque


class NFAState:
    _id_counter = 0

    def __init__(self):
        self.id = NFAState._id_counter
        NFAState._id_counter += 1
        self.transitions = {}  # symbol -> set of NFAState
        self.epsilon = set()   # epsilon transitions

    def add_transition(self, symbol, state):
        if symbol is None:
            self.epsilon.add(state)
        else:
            self.transitions.setdefault(symbol, set()).add(state)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, NFAState) and self.id == other.id

    def __repr__(self):
        return f"NFAState({self.id})"


class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept
        self.states = self._collect_states(start)

    @staticmethod
    def _collect_states(start_state):
        states = set()
        stack = [start_state]
        while stack:
            state = stack.pop()
            if state in states:
                continue
            states.add(state)
            stack.extend(state.epsilon)
            for targets in state.transitions.values():
                stack.extend(targets)
        return states

    def alphabet(self):
        return sorted({symbol for state in self.states for symbol in state.transitions.keys()})

    def __repr__(self):
        return f"NFA(start={self.start}, accept={self.accept}, states={len(self.states)})"


class DFAState:
    _id_counter = 0

    def __init__(self, nfa_states):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.nfa_states = frozenset(nfa_states)
        self.transitions = {}

    def __hash__(self):
        return hash(self.nfa_states)

    def __eq__(self, other):
        return isinstance(other, DFAState) and self.nfa_states == other.nfa_states

    def __repr__(self):
        state_ids = sorted(state.id for state in self.nfa_states)
        return f"DFAState({self.id}, nfa={state_ids})"


class DFA:
    def __init__(self, start_state, states, accept_states):
        self.start = start_state
        self.states = states
        self.accept_states = accept_states

    def alphabet(self):
        return sorted({symbol for state in self.states for symbol in state.transitions.keys()})

    def matches(self, text):
        current = self.start
        for char in text:
            current = current.transitions.get(char)
            if current is None:
                return False
        return current in self.accept_states

    def __repr__(self):
        return f"DFA(start={self.start}, states={len(self.states)}, accept={len(self.accept_states)})"


def _insert_concat_symbols(regex):
    result = []
    for i, char in enumerate(regex):
        result.append(char)
        if i + 1 < len(regex):
            next_char = regex[i + 1]
            if char not in '(|' and next_char not in '|)*':
                result.append('.')
    return ''.join(result)


def _to_postfix(regex):
    precedence = {'*': 3, '.': 2, '|': 1}
    output = []
    operators = []

    for token in regex:
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError('Unmatched parenthesis in regular expression')
            operators.pop()
        elif token in precedence:
            while operators and operators[-1] != '(' and precedence[operators[-1]] >= precedence[token]:
                output.append(operators.pop())
            operators.append(token)
        else:
            output.append(token)

    while operators:
        op = operators.pop()
        if op in '()':
            raise ValueError('Unmatched parenthesis in regular expression')
        output.append(op)

    return ''.join(output)


def _symbol_nfa(symbol):
    start = NFAState()
    accept = NFAState()
    start.add_transition(symbol, accept)
    return NFA(start, accept)


def _concat_nfa(left, right):
    left.accept.add_transition(None, right.start)
    return NFA(left.start, right.accept)


def _union_nfa(left, right):
    start = NFAState()
    accept = NFAState()
    start.add_transition(None, left.start)
    start.add_transition(None, right.start)
    left.accept.add_transition(None, accept)
    right.accept.add_transition(None, accept)
    return NFA(start, accept)


def _star_nfa(nfa):
    start = NFAState()
    accept = NFAState()
    start.add_transition(None, nfa.start)
    start.add_transition(None, accept)
    nfa.accept.add_transition(None, nfa.start)
    nfa.accept.add_transition(None, accept)
    return NFA(start, accept)


def regex_to_nfa(regex):
    if regex is None:
        raise ValueError('Regular expression cannot be None')
    regex = regex.strip()
    if regex == '':
        raise ValueError('Regular expression cannot be empty')

    regex = _insert_concat_symbols(regex)
    postfix = _to_postfix(regex)
    stack = []

    for token in postfix:
        if token == '.':
            if len(stack) < 2:
                raise ValueError('Invalid regular expression for concatenation')
            right = stack.pop()
            left = stack.pop()
            stack.append(_concat_nfa(left, right))
        elif token == '|':
            if len(stack) < 2:
                raise ValueError('Invalid regular expression for alternation')
            right = stack.pop()
            left = stack.pop()
            stack.append(_union_nfa(left, right))
        elif token == '*':
            if not stack:
                raise ValueError('Invalid regular expression for Kleene star')
            nfa = stack.pop()
            stack.append(_star_nfa(nfa))
        else:
            stack.append(_symbol_nfa(token))

    if len(stack) != 1:
        raise ValueError('Invalid regular expression: could not build NFA')

    return stack[0]


def _epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state in state.epsilon:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure


def _move(states, symbol):
    targets = set()
    for state in states:
        targets.update(state.transitions.get(symbol, set()))
    return targets


def nfa_to_dfa(nfa):
    start_closure = _epsilon_closure({nfa.start})
    start_state = DFAState(start_closure)
    states_by_closure = {start_state.nfa_states: start_state}
    queue = deque([start_state])
    alphabet = nfa.alphabet()

    while queue:
        current = queue.popleft()
        for symbol in alphabet:
            target_states = _epsilon_closure(_move(current.nfa_states, symbol))
            if not target_states:
                continue
            if frozenset(target_states) not in states_by_closure:
                new_state = DFAState(target_states)
                states_by_closure[new_state.nfa_states] = new_state
                queue.append(new_state)
            current.transitions[symbol] = states_by_closure[frozenset(target_states)]

    accept_states = {state for state in states_by_closure.values() if nfa.accept in state.nfa_states}
    return DFA(start_state, set(states_by_closure.values()), accept_states)


def visualize_nfa(nfa, title="NFA"):
    """Pretty print NFA structure"""
    print(f"\n{'='*60}")
    print(f"🔷 {title}")
    print(f"{'='*60}")
    print(f"Total States: {len(nfa.states)}")
    print(f"Start State: {nfa.start}")
    print(f"Accept State: {nfa.accept}")
    print(f"Alphabet: {sorted(nfa.alphabet())}")
    print(f"\nStates and Transitions:")
    
    for state in sorted(nfa.states, key=lambda s: s.id):
        transitions = []
        for symbol, targets in sorted(state.transitions.items()):
            for target in sorted(targets, key=lambda s: s.id):
                transitions.append(f"{symbol}->{target.id}")
        
        for target in sorted(state.epsilon, key=lambda s: s.id):
            transitions.append(f"ε->{target.id}")
        
        markers = []
        if state == nfa.start:
            markers.append("START")
        if state == nfa.accept:
            markers.append("ACCEPT")
        
        marker_str = f" [{', '.join(markers)}]" if markers else ""
        print(f"  State {state.id}{marker_str}")
        if transitions:
            for trans in transitions:
                print(f"    → {trans}")


def visualize_dfa(dfa, title="DFA"):
    """Pretty print DFA structure"""
    print(f"\n{'='*60}")
    print(f"🔶 {title}")
    print(f"{'='*60}")
    print(f"Total States: {len(dfa.states)}")
    print(f"Start State: {dfa.start}")
    print(f"Accept States: {len(dfa.accept_states)}")
    print(f"Alphabet: {sorted(dfa.alphabet())}")
    print(f"\nStates and Transitions:")
    
    for state in sorted(dfa.states, key=lambda s: s.id):
        markers = []
        if state == dfa.start:
            markers.append("START")
        if state in dfa.accept_states:
            markers.append("ACCEPT")
        
        marker_str = f" [{', '.join(markers)}]" if markers else ""
        nfa_set = sorted({s.id for s in state.nfa_states})
        print(f"  State {state.id} (from NFA states: {nfa_set}){marker_str}")
        
        if state.transitions:
            for symbol in sorted(state.transitions.keys()):
                target = state.transitions[symbol]
                target_nfa = sorted({s.id for s in target.nfa_states})
                print(f"    {symbol} → State {target.id} (NFA: {target_nfa})")


if __name__ == '__main__':
    regex = 'a(b|c)*'
    nfa = regex_to_nfa(regex)
    dfa = nfa_to_dfa(nfa)

    print('Regular expression:', regex)
    print('NFA:', nfa)
    for state in sorted(nfa.states, key=lambda s: s.id):
        transitions = [f"{symbol or 'ε'}->{sorted({t.id for t in targets})}" for symbol, targets in state.transitions.items()]
        epsilon = sorted({t.id for t in state.epsilon})
        print(f"  {state}: transitions={transitions} epsilon={epsilon}")

    print('\nDFA:', dfa)
    for state in sorted(dfa.states, key=lambda s: s.id):
        print(f"  {state}: {{ {', '.join(f'{sym}->{dst.id}' for sym, dst in state.transitions.items())} }}")

    for sample in ['a', 'ab', 'abc', 'abcb', 'ac', 'b', '']:
        print(f"{sample!r}: {dfa.matches(sample)}")
