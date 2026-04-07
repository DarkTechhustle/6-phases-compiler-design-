# codegen.py
# Code Generation Phase - Generates assembly-like code

class CodeGenerator:
    def __init__(self, optimized_code):
        self.code = optimized_code.instructions
        self.assembly = []
        self.register_map = {}
        self.reg_counter = 0

    def generate(self):
        """Generate assembly-like code from optimized intermediate code"""
        self.assembly.append("; Assembly Code Generated")
        self.assembly.append("section .text")
        self.assembly.append("global compute")
        self.assembly.append("")
        self.assembly.append("compute:")
        self.assembly.append("    push rbp")
        self.assembly.append("    mov rbp, rsp")
        self.assembly.append("")
        
        # Allocate registers for temporaries
        var_set = self.extract_variables()
        self.allocate_registers(var_set)
        
        # Generate assembly for each instruction
        for instr in self.code:
            self.assembly.extend(self.translate_instruction(instr))
        
        # Move result to return register
        if self.register_map:
            last_temp = list(self.register_map.keys())[-1]
            result_reg = self.register_map[last_temp]
            self.assembly.append("")
            self.assembly.append(f"    mov rax, {result_reg}  ; move result to RAX")
        
        self.assembly.append("")
        self.assembly.append("    pop rbp")
        self.assembly.append("    ret")
        
        return self.assembly

    def extract_variables(self):
        """Extract all variables from code"""
        variables = set()
        for instr in self.code:
            if '=' in instr:
                parts = instr.split('=')
                var = parts[0].strip()
                variables.add(var)
                expr = parts[1].strip()
                tokens = expr.split()
                for token in tokens:
                    if token.startswith('t'):
                        variables.add(token)
        return variables

    def allocate_registers(self, variables):
        """Allocate registers to variables"""
        registers = ['rax', 'rbx', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11']
        for i, var in enumerate(sorted(variables)):
            if i < len(registers):
                self.register_map[var] = registers[i]
            else:
                # Use stack for excess variables
                self.register_map[var] = f"[rbp - {(i - len(registers) + 1) * 8}]"

    def translate_instruction(self, instr):
        """Translate three-address code to assembly"""
        asm_lines = []
        
        if '=' in instr:
            parts = instr.split('=')
            var = parts[0].strip()
            expr = parts[1].strip()
            
            tokens = expr.split()
            
            if len(tokens) == 1:
                # Simple assignment: var = value
                value = tokens[0]
                if value in self.register_map:
                    src_reg = self.register_map[value]
                else:
                    src_reg = value
                
                dest_reg = self.register_map[var]
                if src_reg != dest_reg:
                    asm_lines.append(f"    mov {dest_reg}, {src_reg}  ; {var} = {value}")
                else:
                    asm_lines.append(f"    ; {var} already in {dest_reg}")
            
            elif len(tokens) == 3:
                # Binary operation: var = left op right
                left = tokens[0]
                op = tokens[1]
                right = tokens[2]
                
                left_reg = self.register_map.get(left, left)
                right_reg = self.register_map.get(right, right)
                dest_reg = self.register_map[var]
                
                # Use rax as temporary for operation
                if left_reg != 'rax':
                    asm_lines.append(f"    mov rax, {left_reg}  ; load left operand")
                
                if op == '+':
                    asm_lines.append(f"    add rax, {right_reg}  ; rax = {left} + {right}")
                elif op == '-':
                    asm_lines.append(f"    sub rax, {right_reg}  ; rax = {left} - {right}")
                elif op == '*':
                    asm_lines.append(f"    imul rax, {right_reg}  ; rax = {left} * {right}")
                elif op == '/':
                    asm_lines.append(f"    cqo  ; sign extend rax to rdx:rax")
                    asm_lines.append(f"    idiv {right_reg}  ; rax = {left} / {right}")
                
                if dest_reg != 'rax':
                    asm_lines.append(f"    mov {dest_reg}, rax  ; store result in {var}")
        
        return asm_lines

class AssemblyCode:
    def __init__(self, asm_list):
        self.instructions = asm_list

    def __repr__(self):
        result = "Generated Assembly Code:\n"
        for instr in self.instructions:
            result += f"{instr}\n"
        return result

    def __str__(self):
        return "\n".join(self.instructions)

    def save_to_file(self, filename):
        """Save assembly code to file"""
        with open(filename, 'w') as f:
            f.write("\n".join(self.instructions))
        print(f"Assembly code saved to {filename}")
