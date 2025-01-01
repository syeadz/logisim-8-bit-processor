; Calculates the fibonacci sequence up to 13 (233)
; And displays the result in the 7-segment display

#include lib/sevseg_lib.asm

main:
    lwi $7, 0 # fib 0
    lwi $8, 1 # fib 1

    lwi $9, 0 # counter
    lwi $10, 12 # max

fib:
    # display numbers
    sw $13, $7
    sw $14, $8
    add $7, $8
    # swap
    mov $12, $7
    mov $7, $8 
    mov $8, $12

    # loop control
    cmp $9, $10
    jpZ end
    inc $9
    goto fib

end:
    # print fib to bcd
    call s_seg0_display
    halt