; Showcase for the 7-segment display library
; Will display 0xFF (255), 0x01 (1), 0x23 (35), 0x45 (69) on the BCD displays

#include lib/sevseg_lib.asm

main:
    lwi $7, 0xFF
    call s_seg0_display

    lwi $7, 0x01
    call s_seg1_display

    lwi $7, 0x23
    call s_seg2_display

    lwi $7, 0x45
    call s_seg3_display

    halt