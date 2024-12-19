# Calculates the fibonacci sequence up to 13 (233)

#define bcd0 0x1F
#define bcd1 0x3F
#define bcd2 0x5F

main:
    lwi $7, 0 # fib 0
    lwi $8, 1 # fib 1

    lwi $9, 0 # counter
    lwi $10, 12 # max

    lwi $13, bcd0 # address for bcd0
    lwi $14, bcd1 # address for bcd1
    lwi $15, bcd2 # address for bcd2


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
    sw $15, $7 # store fib result
    halt