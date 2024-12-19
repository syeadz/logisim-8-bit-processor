; Showcase for the BCD library
; Will display 0xFF (255), 0x01 (1), 0x23 (35), 0x45 (69) on the BCD displays

#include bcd_lib.asm

main:
lwi $7, 0xFF
call b_bcd0_display

lwi $7, 0x01
call b_bcd1_display

lwi $7, 0x23
call b_bcd2_display

lwi $7, 0x45
call b_bcd3_display

halt