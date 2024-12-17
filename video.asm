#define xpos 0xBF
#define ypos 0xDF
#define viddata 0xFF
#define black 0x00
#define white 0x7F

print_black:
sw $6, $7
ret

print_white:
sw $6, $8
ret

# put xpos in $13, ypos in $14
set_cursor:
sw $4, $13
sw $5, $14
ret

set_and_print:
call set_cursor
call print_white
ret


main:
lwi $4, xpos
lwi $5, ypos
lwi $6, viddata
lwi $7, black
lwi $8, white

lwi $13, 0
lwi $14, 0

# counter
lwi $15, 128
loop:
call set_and_print
inc $13
cmp $13, $15
jpnz loop

halt