; Calculates prime numbers up to 231
; and displays the numbers on the terminal
; note: will take a VERY long time to reach 231

#include lib/terminal_lib.asm

main:
    lwi $15, 232 ; Set the limit to 231 (+ 1 because of the way the loop is written)
    call t_print_2 ; Print 2 (the first prime number)
    call t_print_comma
    call t_print_space
    lwi $7, 3 ; Start at 4
loop:
    call check_prime
    inc $7
    cmp $7, $15
    jpnZ loop ; loop until $7 = 232
    halt

; Check if number in $7 is prime, then print it if so
check_prime:
    mov $8, $7 ; counter
check_prime_loop:
    dec $8 ; decrement counter
    cmp $8, $1 ; check if counter = 1
    jpZ check_prime_loop_end_print ; loop end if counter = 1, print number
    mov $5, $7 ; dividend
    mov $6, $8 ; divisor (counter)
    mov $9, $7 ; backup number
    call m_div8 ; divide, modifies $5 and $7
    cmp $5, $0 ; check if remainder = 0
    jpZ check_prime_loop_end ; loop end if remainder = 0, don't print
    mov $7, $9 ; restore number
    goto check_prime_loop
check_prime_loop_end:
    mov $7, $9 ; restore number
    ret
check_prime_loop_end_print:
    mov $7, $9 ; restore number
    call t_print_reg_num
    push $7
    call t_print_comma
    call t_print_space
    pop $7
    ret
