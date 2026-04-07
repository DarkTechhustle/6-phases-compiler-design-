; Assembly Code Generated
section .text
global compute

compute:
    push rbp
    mov rbp, rsp

    mov rax, 132  ; t1 = 132
    mov rax, 6  ; load left operand
    imul rax, rax  ; rax = 6 * t1
    mov rbx, rax  ; store result in t2
    mov rax, 3  ; load left operand
    add rax, rbx  ; rax = 3 + t2
    mov rcx, rax  ; store result in t3

    mov rax, rcx  ; move result to RAX

    pop rbp
    ret