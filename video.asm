; Showcase for video library
; Draws squares along the screen

#include video_lib.asm

main:
    lwi $7, 16 ; size of square side
    lwi $6, 0 ; y position

    lwi $14, 8 ; i counter
; loop for y position
outer_loop:
    lwi $5, 0 ; reset x position

    lwi $15, 4 ; j counter
; loop for x position
inner_loop:
    mov $10, $14
    rrc $10
    jpC set_to_red
    call v_set_white
    goto jump_to_draw1
set_to_red:
    call v_set_red
jump_to_draw1:
    call v_set_cursor
    call v_draw_square

    add $5, $7
    call v_set_cursor

    mov $10, $14
    rrc $10
    jpC set_to_blue
    call v_set_yellow
    goto jump_to_draw2
set_to_blue:
    call v_set_blue
jump_to_draw2:
    call v_draw_square

    add $5, $7

    dec $15
    cmp $15, $0
    jpnZ inner_loop
    add $6, $7
    dec $14
    cmp $14, $0
    jpnZ outer_loop

    halt