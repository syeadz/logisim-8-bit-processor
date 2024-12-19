; Library to print things to the terminal in Logisim
; Only capable of printing single ascii characters
; Unable to read data from ROM, so the ascii characters are hardcoded

#include math_lib.asm

#define T_TERM_ADDR 0x7F

; Todo: replace $7 with another register if it causes problems
t_print_a:
    lwi $7, 0x41
    goto t_print

t_print_b:
    lwi $7, 0x42
    goto t_print

t_print_c:
    lwi $7, 0x43
    goto t_print

t_print_d:
    lwi $7, 0x44
    goto t_print

t_print_e:
    lwi $7, 0x45
    goto t_print

t_print_f:
    lwi $7, 0x46
    goto t_print

t_print_g:
    lwi $7, 0x47
    goto t_print

t_print_h:
    lwi $7, 0x48
    goto t_print

t_print_i:
    lwi $7, 0x49
    goto t_print

t_print_j:
    lwi $7, 0x4A
    goto t_print

t_print_k:
    lwi $7, 0x4B
    goto t_print

t_print_l:
    lwi $7, 0x4C
    goto t_print

t_print_m:
    lwi $7, 0x4D
    goto t_print

t_print_n:
    lwi $7, 0x4E
    goto t_print

t_print_o:
    lwi $7, 0x4F
    goto t_print

t_print_p:
    lwi $7, 0x50
    goto t_print

t_print_q:
    lwi $7, 0x51
    goto t_print

t_print_r:
    lwi $7, 0x52
    goto t_print

t_print_s:
    lwi $7, 0x53
    goto t_print

t_print_t:
    lwi $7, 0x54
    goto t_print

t_print_u:
    lwi $7, 0x55
    goto t_print

t_print_v:
    lwi $7, 0x56
    goto t_print

t_print_w:
    lwi $7, 0x57
    goto t_print

t_print_x:
    lwi $7, 0x58
    goto t_print

t_print_y:
    lwi $7, 0x59
    goto t_print

t_print_z:
    lwi $7, 0x5A
    goto t_print

t_print_space:
    lwi $7, 0x20
    goto t_print

t_print_exclamation:
    lwi $7, 0x21
    goto t_print

t_print_double_quote:
    lwi $7, 0x22
    goto t_print

t_print_hash:
    lwi $7, 0x23
    goto t_print

t_print_dollar:
    lwi $7, 0x24
    goto t_print

t_print_percent:
    lwi $7, 0x25
    goto t_print

t_print_ampersand:
    lwi $7, 0x26
    goto t_print

t_print_single_quote:
    lwi $7, 0x27
    goto t_print

t_print_open_paren:
    lwi $7, 0x28
    goto t_print

t_print_close_paren:
    lwi $7, 0x29
    goto t_print

t_print_asterisk:
    lwi $7, 0x2A
    goto t_print

t_print_plus:
    lwi $7, 0x2B
    goto t_print

t_print_comma:
    lwi $7, 0x2C
    goto t_print

t_print_minus:
    lwi $7, 0x2D
    goto t_print

t_print_dot:
    lwi $7, 0x2E
    goto t_print

t_print_slash:
    lwi $7, 0x2F
    goto t_print

t_print_colon:
    lwi $7, 0x3A
    goto t_print

t_print_semicolon:
    lwi $7, 0x3B
    goto t_print

t_print_less_than:
    lwi $7, 0x3C
    goto t_print

t_print_equal:
    lwi $7, 0x3D
    goto t_print

t_print_greater_than:
    lwi $7, 0x3E
    goto t_print

t_print_question:
    lwi $7, 0x3F
    goto t_print

t_print_at:
    lwi $7, 0x40
    goto t_print

t_print_newline:
    lwi $7, 0x0A
    goto t_print

t_print_0:
    lwi $7, 0x30
    goto t_print

t_print_1:
    lwi $7, 0x31
    goto t_print

t_print_2:
    lwi $7, 0x32
    goto t_print

t_print_3:
    lwi $7, 0x33
    goto t_print

t_print_4:
    lwi $7, 0x34
    goto t_print

t_print_5:
    lwi $7, 0x35
    goto t_print

t_print_6:
    lwi $7, 0x36
    goto t_print

t_print_7:
    lwi $7, 0x37
    goto t_print

t_print_8:
    lwi $7, 0x38
    goto t_print

t_print_9:
    lwi $7, 0x39
    goto t_print

t_print_plus:
    lwi $7, 0x2B
    goto t_print

t_print_minus:
    lwi $7, 0x2D
    goto t_print

t_print_divide:
    lwi $7, 0x2F
    goto t_print

t_print_multiply:
    lwi $7, 0x2A
    goto t_print

; Print an ascii character stored in register $7 and return
t_print:
    lwi $2, T_TERM_ADDR
    sw $2, $7
    ret

; Clear the terminal
t_clear:
    lwi $2, T_TERM_ADDR
    lwi $7, 0x80
    sw $2, $7
    ret


; Function: print_reg_num
; Description: Prints the number stored in register $7 to the terminal
; Input: $7 = number to print
; Note: Only works for 8-bit numbers (0-255)
t_print_reg_num:
    push $5
    push $6
    push $7
    lwi $10, 0 ; digit counter
    lwi $6, 10 ; divide by 10
    mov $5, $7 ; save number in $5 as dividend
t_print_reg_num_div_loop:
    cmp $7, $0 ; check if quotient/number is 0
    jpZ t_print_reg_num_div_loop_end
    call m_div8
    push $5 ; save remainder (digit)
    mov $5, $7 ; save quotient as dividend
    inc $10 ; increment digit counter
    goto t_print_reg_num_div_loop
t_print_reg_num_div_loop_end:
    cmp $10, $0 ; check if digit counter is 0
    jpZ t_print_0 ; print 0 if number is 0
t_print_reg_num_print_loop:
    pop $7 ; get digit
    addi $7, 0x30 ; convert to ascii
    lwi $2, T_TERM_ADDR
    sw $2, $7 ; print digit
    dec $10 ; decrement digit counter
    cmp $10, $0 ; check if all digits have been printed
    jpNZ t_print_reg_num_print_loop
    pop $7
    pop $6
    pop $5
    ret
