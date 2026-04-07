"""
Advanced Compilation Techniques: Optimization & Backend
- Prefix/Postfix Notation Conversion
- Intermediate Code Formats (Quadruple, Triple, Indirect Triple)
- DAG (Directed Acyclic Graph) Construction
- Global Data Flow Analysis
- Storage Allocation (Heap, Stack, Static)
"""

from collections import defaultdict, deque


class NotationConverter:
    """Convert between infix, prefix, and postfix notations"""
    
    @staticmethod
    def infix_to_postfix(expression):
        """Convert infix to postfix (Reverse Polish Notation)"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output = []
        operator_stack = []
        
        tokens = expression.split()
        for token in tokens:
            if token not in precedence and token not in '()':
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()
            else:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        while operator_stack:
            output.append(operator_stack.pop())
        
        return ' '.join(output)
    
    @staticmethod
    def infix_to_prefix(expression):
        """Convert infix to prefix (Polish Notation)"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output = []
        operator_stack = []
        
        tokens = expression.split()[::-1]  # Reverse tokens
        
        for token in tokens:
            if token not in precedence and token not in '()':
                output.append(token)
            elif token == ')':
                operator_stack.append(token)
            elif token == '(':
                while operator_stack and operator_stack[-1] != ')':
                    output.append(operator_stack.pop())
                operator_stack.pop()
            else:
                while (operator_stack and 
                       operator_stack[-1] != ')' and
                       operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] > precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        while operator_stack:
            output.append(operator_stack.pop())
        
        return ' '.join(output[::-1])
    
    @staticmethod
    def postfix_to_infix(postfix):
        """Convert postfix to infix"""
        stack = []
        operators = {'+', '-', '*', '/', '^'}
        
        tokens = postfix.split()
        for token in tokens:
            if token in operators:
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(f"( {a} {token} {b} )")
            else:
                stack.append(token)
        
        return stack[0] if stack else ""


class IntermediateCodeFormats:
    """Generate different intermediate code formats"""
    
    def __init__(self):
        self.quad_counter = 0
        self.temp_counter = 0
    
    def generate_quadruple(self, expression):
        """
        Generate quadruple representation (op, arg1, arg2, result)
        """
        print("🟩 QUADRUPLE Format (4-tuple: op, arg1, arg2, result)")
        print("-" * 60)
        
        quads = []
        tokens = expression.split()
        temp_stack = []
        
        for token in tokens:
            if token in ['+', '-', '*', '/']:
                if len(temp_stack) >= 2:
                    arg2 = temp_stack.pop()
                    arg1 = temp_stack.pop()
                    result = f"t{self.temp_counter}"
                    self.temp_counter += 1
                    quad = (token, arg1, arg2, result)
                    quads.append(quad)
                    temp_stack.append(result)
                    print(f"  ({token}, {arg1}, {arg2}, {result})")
            else:
                temp_stack.append(token)
        
        return quads
    
    def generate_triple(self, expression):
        """
        Generate triple representation (op, arg1, arg2)
        Result is implicit (position in array)
        """
        print("\n🟦 TRIPLE Format (3-tuple: op, arg1, arg2)")
        print("-" * 60)
        
        triples = []
        tokens = expression.split()
        temp_stack = []
        position_map = {}
        
        position = 0
        for token in tokens:
            if token in ['+', '-', '*', '/']:
                if len(temp_stack) >= 2:
                    arg2_ref = temp_stack.pop()
                    arg1_ref = temp_stack.pop()
                    triple = (token, arg1_ref, arg2_ref)
                    triples.append(triple)
                    position_map[position] = triple
                    print(f"  [{position}] ({token}, {arg1_ref}, {arg2_ref})")
                    temp_stack.append(f"({position})")
                    position += 1
            else:
                temp_stack.append(token)
        
        return triples
    
    def generate_indirect_triple(self, expression):
        """
        Generate indirect triple representation
        Adds level of indirection via operation sequence table
        """
        print("\n🟨 INDIRECT TRIPLE Format (with operation sequence)")
        print("-" * 60)
        
        triples = []
        tokens = expression.split()
        temp_stack = []
        
        position = 0
        op_sequence = []
        
        for token in tokens:
            if token in ['+', '-', '*', '/']:
                if len(temp_stack) >= 2:
                    arg2_ref = temp_stack.pop()
                    arg1_ref = temp_stack.pop()
                    triple = (token, arg1_ref, arg2_ref)
                    triples.append(triple)
                    op_sequence.append(position)
                    print(f"  Triple[{position}]: ({token}, {arg1_ref}, {arg2_ref})")
                    temp_stack.append(f"T{position}")
                    position += 1
            else:
                temp_stack.append(token)
        
        print(f"\n  Operation Sequence: {op_sequence}")
        return triples, op_sequence


class DAGNode:
    """Node in Directed Acyclic Graph"""
    _id_counter = 0
    
    def __init__(self, op, left=None, right=None, value=None):
        self.id = DAGNode._id_counter
        DAGNode._id_counter += 1
        self.op = op
        self.left = left
        self.right = right
        self.value = value
        self.labels = []
    
    def __repr__(self):
        return f"N{self.id}({self.op})"


class DAGOptimizer:
    """Construct and optimize code using DAG"""
    
    def __init__(self):
        self.nodes = {}
        self.node_counter = {}
    
    def build_dag_from_expression(self, expression):
        """Build DAG from arithmetic expression"""
        print("\n🟫 DAG (Directed Acyclic Graph) Construction")
        print("-" * 60)
        
        def build_tree(tokens, index=0):
            if index >= len(tokens):
                return None
            
            token = tokens[index]
            
            if token == '(':
                expr, next_idx = build_expr(tokens, index + 1)
                return expr, next_idx + 1
            else:
                # Leaf node
                node_key = f"({token})"
                if node_key not in self.nodes:
                    self.nodes[node_key] = DAGNode('leaf', value=token)
                return self.nodes[node_key], index + 1
        
        def build_expr(tokens, index):
            left, index = build_tree(tokens, index)
            
            while index < len(tokens) and tokens[index] in ['+', '-', '*', '/']:
                op = tokens[index]
                right, index = build_tree(tokens, index + 1)
                
                node_key = f"({left.id} {op} {right.id})"
                if node_key not in self.nodes:
                    node = DAGNode(op, left, right)
                    self.nodes[node_key] = node
                else:
                    node = self.nodes[node_key]
                
                left = node
            
            return left, index
        
        tokens = expression.split()
        root, _ = build_expr(tokens, 0)
        
        print(f"DAG Nodes: {len(self.nodes)}")
        for key, node in self.nodes.items():
            if node.value:
                print(f"  {node}: value={node.value}")
            else:
                print(f"  {node}: op={node.op}, left={node.left}, right={node.right}")
        
        return root
    
    def dag_to_code(self, root):
        """Convert DAG to optimized sequence of instructions"""
        print("\n  Optimized Code from DAG:")
        code = []
        counter = 0
        
        def traverse(node):
            nonlocal counter
            if not node:
                return f"empty"
            
            if node.value:
                return node.value
            
            left_val = traverse(node.left)
            right_val = traverse(node.right)
            
            result = f"t{counter}"
            counter += 1
            code.append(f"    {result} = {left_val} {node.op} {right_val}")
            return result
        
        traverse(root)
        for instr in code:
            print(instr)
        
        return code


class DataFlowAnalyzer:
    """Global data flow analysis"""
    
    def __init__(self, instructions):
        self.instructions = instructions
        self.gen = defaultdict(set)
        self.kill = defaultdict(set)
        self.in_set = defaultdict(set)
        self.out_set = defaultdict(set)
    
    def analyze_definitions(self):
        """Analyze variable definitions and uses"""
        print("\n🔵 Global Data Flow Analysis")
        print("-" * 60)
        
        print(f"\nInstructions: {len(self.instructions)}")
        for i, instr in enumerate(self.instructions):
            print(f"  [{i}] {instr}")
        
        # Extract definitions and uses
        for i, instr in enumerate(self.instructions):
            parts = instr.split('=')
            if len(parts) == 2:
                var = parts[0].strip()
                expr = parts[1].strip()
                self.gen[i].add(var)
                
                for char in expr:
                    if char.isalpha() or char.isdigit():
                        self.kill[i].add(char)
        
        print("\nGEN/KILL Analysis:")
        for i in range(len(self.instructions)):
            print(f"  Block[{i}]:")
            print(f"    GEN(defined): {self.gen[i]}")
            print(f"    KILL(used): {self.kill[i]}")
        
        self._compute_reaching_definitions()
        return self.gen, self.kill
    
    def _compute_reaching_definitions(self):
        """Compute reaching definitions iteratively"""
        changed = True
        iterations = 0
        
        while changed:
            changed = False
            iterations += 1
            
            for i in range(len(self.instructions)):
                new_in = set().union(*[self.out_set[j] for j in range(i)])
                new_out = self.gen[i].union(new_in - self.kill[i])
                
                if new_in != self.in_set[i] or new_out != self.out_set[i]:
                    changed = True
                    self.in_set[i] = new_in
                    self.out_set[i] = new_out
        
        print(f"\nReaching Definitions (computed in {iterations} iterations):")
        for i in range(len(self.instructions)):
            print(f"  Block[{i}]: IN={self.in_set[i]}, OUT={self.out_set[i]}")


class StorageAllocator:
    """Allocate storage for variables (heap, stack, static)"""
    
    def __init__(self):
        self.stack_offset = 0
        self.heap_vars = {}
        self.static_vars = {}
        self.stack_vars = {}
    
    def allocate_storage(self, variables, allocation_strategy):
        """Allocate storage based on strategy"""
        print(f"\n📦 Storage Allocation ({allocation_strategy})")
        print("-" * 60)
        
        print(f"\nVariables to allocate: {variables}")
        
        if allocation_strategy == "stack":
            return self._allocate_stack(variables)
        elif allocation_strategy == "heap":
            return self._allocate_heap(variables)
        elif allocation_strategy == "static":
            return self._allocate_static(variables)
        elif allocation_strategy == "mixed":
            return self._allocate_mixed(variables)
    
    def _allocate_stack(self, variables):
        """Allocate all variables on stack"""
        print("\n📍 Stack Allocation Strategy:")
        stack_map = {}
        offset = 0
        
        for var in variables:
            size = 8  # 64-bit
            self.stack_vars[var] = {'offset': offset, 'size': size}
            stack_map[var] = f"[rbp - {offset}]"
            offset += size
            print(f"  {var}: offset={offset}, address=[rbp - {offset}]")
        
        return stack_map
    
    def _allocate_heap(self, variables):
        """Allocate all variables on heap"""
        print("\n📍 Heap Allocation Strategy:")
        heap_map = {}
        address = 0x1000  # Base heap address
        
        for var in variables:
            size = 8
            self.heap_vars[var] = {'address': address, 'size': size}
            heap_map[var] = f"0x{address:04x}"
            print(f"  {var}: address=0x{address:04x}")
            address += size
        
        return heap_map
    
    def _allocate_static(self, variables):
        """Allocate all variables in static data section"""
        print("\n📍 Static Allocation Strategy:")
        static_map = {}
        
        for var in variables:
            size = 8
            self.static_vars[var] = {'size': size}
            static_map[var] = f".data_{var}"
            print(f"  {var}: stored in data segment")
        
        return static_map
    
    def _allocate_mixed(self, variables):
        """Mixed allocation: locals on stack, globals in static"""
        print("\n📍 Mixed Allocation Strategy (stack + static):")
        mixed_map = {}
        
        local_vars = variables[:len(variables)//2]
        global_vars = variables[len(variables)//2:]
        
        # Locals on stack
        offset = 0
        for var in local_vars:
            self.stack_vars[var] = {'offset': offset, 'size': 8}
            mixed_map[var] = f"[rbp - {offset}]"
            print(f"  {var} (local): [rbp - {offset}]")
            offset += 8
        
        # Globals in static
        for var in global_vars:
            self.static_vars[var] = {'size': 8}
            mixed_map[var] = f".data_{var}"
            print(f"  {var} (global): .data_{var}")
        
        return mixed_map
    
    def generate_storage_map(self):
        """Generate complete storage allocation report"""
        print(f"\n📊 Storage Allocation Summary:")
        print(f"  Stack variables: {len(self.stack_vars)}")
        for var, info in self.stack_vars.items():
            print(f"    {var}: offset={info['offset']}")
        
        print(f"  Heap variables: {len(self.heap_vars)}")
        for var, info in self.heap_vars.items():
            print(f"    {var}: address=0x{info['address']:04x}")
        
        print(f"  Static variables: {len(self.static_vars)}")
        for var in self.static_vars:
            print(f"    {var}: static")


def demonstrate_all_techniques():
    """Demonstrate all advanced optimization techniques"""
    
    print("\n" + "="*60)
    print("ADVANCED COMPILATION TECHNIQUES")
    print("="*60)
    
    # 1. Notation Conversion
    print("\n" + "="*60)
    print("1. NOTATION CONVERSION")
    print("="*60)
    
    infix = "a + b * c"
    print(f"\nInfix: {infix}")
    postfix = NotationConverter.infix_to_postfix(infix)
    prefix = NotationConverter.infix_to_prefix(infix)
    print(f"Postfix (RPN): {postfix}")
    print(f"Prefix (Polish): {prefix}")
    
    # 2. Intermediate Code Formats
    print("\n" + "="*60)
    print("2. INTERMEDIATE CODE REPRESENTATIONS")
    print("="*60)
    
    icf = IntermediateCodeFormats()
    postfix_expr = "a b + c *"
    icf.generate_quadruple(postfix_expr)
    icf.generate_triple(postfix_expr)
    icf.generate_indirect_triple(postfix_expr)
    
    # 3. DAG Optimization
    print("\n" + "="*60)
    print("3. DAG-BASED OPTIMIZATION")
    print("="*60)
    
    dag_opt = DAGOptimizer()
    expr = "a + b * c"
    root = dag_opt.build_dag_from_expression(expr)
    dag_opt.dag_to_code(root)
    
    # 4. Data Flow Analysis
    print("\n" + "="*60)
    print("4. DATA FLOW ANALYSIS")
    print("="*60)
    
    instructions = [
        "a = 5",
        "b = a + 2",
        "c = b * 3",
        "d = c + a"
    ]
    dfa = DataFlowAnalyzer(instructions)
    dfa.analyze_definitions()
    
    # 5. Storage Allocation
    print("\n" + "="*60)
    print("5. STORAGE ALLOCATION")
    print("="*60)
    
    variables = ['a', 'b', 'c', 'd', 'e']
    
    sa = StorageAllocator()
    sa.allocate_storage(variables, "stack")
    
    sa2 = StorageAllocator()
    sa2.allocate_storage(variables, "mixed")
    
    sa3 = StorageAllocator()
    sa3.allocate_storage(variables, "static")


if __name__ == '__main__':
    demonstrate_all_techniques()
