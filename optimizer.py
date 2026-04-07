# optimizer.py
# Code Optimization Phase

class CodeOptimizer:
    def __init__(self, three_address_code):
        self.code = three_address_code.instructions
        self.optimized_code = []

    def optimize(self):
        # Apply multiple optimization techniques
        self.code = self.constant_folding(self.code)
        self.code = self.dead_code_elimination(self.code)
        self.code = self.common_subexpression_elimination(self.code)
        self.optimized_code = self.code
        return self.optimized_code

    def constant_folding(self, code):
        """Replace constant expressions with their computed values"""
        optimized = []
        for instr in code:
            if '=' in instr:
                parts = instr.split('=')
                var = parts[0].strip()
                expr = parts[1].strip()
                
                # Check if expression contains only constants
                try:
                    if all(self.is_constant(token) for token in expr.split()):
                        result = self.evaluate_expr(expr)
                        optimized.append(f"{var} = {result}")
                    else:
                        optimized.append(instr)
                except:
                    optimized.append(instr)
            else:
                optimized.append(instr)
        return optimized

    def is_constant(self, token):
        """Check if token is a number or operator"""
        try:
            float(token)
            return True
        except:
            return token in ['+', '-', '*', '/', '=']

    def evaluate_expr(self, expr):
        """Safely evaluate a mathematical expression"""
        try:
            return eval(expr)
        except:
            return expr

    def dead_code_elimination(self, code):
        """Remove unused variable assignments"""
        # Track which variables are actually used
        used_vars = set()
        
        # Last assignment to each variable
        last_assignment = {}
        
        # Scan forward to find used variables
        for instr in code:
            if '=' in instr:
                parts = instr.split('=')
                expr = parts[1].strip()
                tokens = expr.split()
                for token in tokens:
                    if token not in ['+', '-', '*', '/']:
                        try:
                            float(token)
                        except:
                            if token != '=' and token.startswith('t'):
                                used_vars.add(token)

        optimized = []
        for instr in code:
            if '=' in instr:
                var = instr.split('=')[0].strip()
                # Keep if it's the last assignment of this var or it's used
                if var not in last_assignment:
                    last_assignment[var] = instr
                else:
                    # Check if previous assignment is used
                    if last_assignment[var].split('=')[0].strip() in used_vars:
                        optimized.append(last_assignment[var])
                    last_assignment[var] = instr
        
        # Add final assignments
        for var, instr in last_assignment.items():
            optimized.append(instr)
        
        return optimized

    def common_subexpression_elimination(self, code):
        """Eliminate redundant computations"""
        seen_exprs = {}
        optimized = []
        
        for instr in code:
            if '=' in instr:
                parts = instr.split('=')
                var = parts[0].strip()
                expr = parts[1].strip()
                
                if expr in seen_exprs:
                    # Reuse previous computation
                    optimized.append(f"{var} = {seen_exprs[expr]}")
                else:
                    seen_exprs[expr] = var
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        return optimized

class OptimizedCode:
    def __init__(self, code_list):
        self.instructions = code_list

    def __repr__(self):
        result = "Optimized Code:\n"
        for i, instr in enumerate(self.instructions, 1):
            result += f"{i}: {instr}\n"
        return result

    def __str__(self):
        return "\n".join(self.instructions)
