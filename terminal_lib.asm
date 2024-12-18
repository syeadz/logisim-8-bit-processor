; Library to print things to the terminal in Logisim
; Only capable of printing single ascii characters
; Unable to read data from ROM, so the ascii characters are hardcoded

#define T_TERM_ADDR 0x7F

t_print_a:
lwi $4, 0x41
goto t_print

t_print_b:
lwi $4, 0x42
goto t_print

t_print_c:
lwi $4, 0x43
goto t_print

t_print_d:
lwi $4, 0x44
goto t_print

t_print_e:
lwi $4, 0x45
goto t_print

t_print_f:
lwi $4, 0x46
goto t_print

t_print_g:
lwi $4, 0x47
goto t_print

t_print_h:
lwi $4, 0x48
goto t_print

t_print_i:
lwi $4, 0x49
goto t_print

t_print_j:
lwi $4, 0x4A
goto t_print

t_print_k:
lwi $4, 0x4B
goto t_print

t_print_l:
lwi $4, 0x4C
goto t_print

t_print_m:
lwi $4, 0x4D
goto t_print

t_print_n:
lwi $4, 0x4E
goto t_print

t_print_o:
lwi $4, 0x4F
goto t_print

t_print_p:
lwi $4, 0x50
goto t_print

t_print_q:
lwi $4, 0x51
goto t_print

t_print_r:
lwi $4, 0x52
goto t_print

t_print_s:
lwi $4, 0x53
goto t_print

t_print_t:
lwi $4, 0x54
goto t_print

t_print_u:
lwi $4, 0x55
goto t_print

t_print_v:
lwi $4, 0x56
goto t_print

t_print_w:
lwi $4, 0x57
goto t_print

t_print_x:
lwi $4, 0x58
goto t_print

t_print_y:
lwi $4, 0x59
goto t_print

t_print_z:
lwi $4, 0x5A
goto t_print

t_print_space:
lwi $4, 0x20
goto t_print

t_print_exclamation:
lwi $4, 0x21
goto t_print

t_print_double_quote:
lwi $4, 0x22
goto t_print

t_print_hash:
lwi $4, 0x23
goto t_print

t_print_dollar:
lwi $4, 0x24
goto t_print

t_print_percent:
lwi $4, 0x25
goto t_print

t_print_ampersand:
lwi $4, 0x26
goto t_print

t_print_single_quote:
lwi $4, 0x27
goto t_print

t_print_open_paren:
lwi $4, 0x28
goto t_print

t_print_close_paren:
lwi $4, 0x29
goto t_print

t_print_asterisk:
lwi $4, 0x2A
goto t_print

t_print_plus:
lwi $4, 0x2B
goto t_print

t_print_comma:
lwi $4, 0x2C
goto t_print

t_print_minus:
lwi $4, 0x2D
goto t_print

t_print_dot:
lwi $4, 0x2E
goto t_print

t_print_slash:
lwi $4, 0x2F
goto t_print

t_print_colon:
lwi $4, 0x3A
goto t_print

t_print_semicolon:
lwi $4, 0x3B
goto t_print

t_print_less_than:
lwi $4, 0x3C
goto t_print

t_print_equal:
lwi $4, 0x3D
goto t_print

t_print_greater_than:
lwi $4, 0x3E
goto t_print

t_print_question:
lwi $4, 0x3F
goto t_print

t_print_at:
lwi $4, 0x40
goto t_print

t_print_newline:
lwi $4, 0x0A
goto t_print

; Print an ascii character stored in register $4 and return
t_print:
lwi $2, T_TERM_ADDR
sw $2, $4
ret