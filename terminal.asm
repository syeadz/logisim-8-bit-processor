; Showcasing the terminal library
; This program prints "Hello world!" to the terminal
; It also demonstrates the use of the math library to multiply and divide two numbers
; which is then printed to the terminal

#include terminal_lib.asm

#define MUL_A 0x27
#define MUL_B 0x6
#define DIV_A 0xFF
#define DIV_B 0x2F

main:
call t_print_h
call t_print_e
call t_print_l
call t_print_l
call t_print_o
call t_print_space
call t_print_w
call t_print_o
call t_print_r
call t_print_l
call t_print_d
call t_print_exclamation

call t_print_newline

lwi $7, MUL_A
mov $5, $7
call t_print_reg_num
call t_print_space
call t_print_multiply
call t_print_space
lwi $7, MUL_B
mov $6, $7
call t_print_reg_num
call t_print_space
call t_print_equal
call t_print_space
call m_mul8
call t_print_reg_num

call t_print_newline

lwi $7, DIV_A
mov $5, $7
call t_print_reg_num
call t_print_space
call t_print_divide
call t_print_space
lwi $7, DIV_B
mov $6, $7
call t_print_reg_num
call t_print_space
call t_print_equal
call t_print_space
call m_div8
call t_print_reg_num
call t_print_comma
call t_print_space
call t_print_r
call t_print_e
call t_print_m
call t_print_colon
call t_print_space
mov $7, $5
call t_print_reg_num

halt