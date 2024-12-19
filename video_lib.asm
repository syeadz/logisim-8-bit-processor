#define v_xpos 0xBF
#define v_ypos 0xDF
#define v_viddata 0xFF
#define v_black 0x00
#define v_white 0x7F
#define v_red 0x24
#define v_blue 0x64
#define v_yellow 0x34


; Function: print
; Description: Print a character to the screen with current color stored in $4
v_print:
lwi $2, v_viddata
sw $2, $4
ret


; Function: set_black
; Description: Set the current color to black
v_set_black:
lwi $4, v_black
ret


; Function: set_white
; Description: Set the current color to white
v_set_white:
lwi $4, v_white
ret

; Function: set_red
; Description: Set the current color to red
v_set_red:
lwi $4, v_red
ret

; Function: set_blue
; Description: Set the current color to blue
v_set_blue:
lwi $4, v_blue
ret

; Function: set_yellow
; Description: Set the current color to yellow
v_set_yellow:
lwi $4, v_yellow
ret

; Function: clear_screen
; Description: Clear the screen by setting bit 7, which is tied to reset
v_clear_screen:
lwi $4, 0x80
lwi $2, v_viddata
sw $2, $4
ret


; Function: set_cursor
; Description: Set the cursor to the position specified by xpos and ypos
; Input: $5 = xpos, $6 = ypos
v_set_cursor:
lwi $2, v_xpos
sw $2, $5
lwi $2, v_ypos
sw $2, $6
ret


; Function: draw_right
; Description: Draw $7 characters to the right of the cursor (initial position will also be drawn)
; Input: $7 = number of characters to draw
; Side effects: $8 is modified, cursor is moved
v_draw_right:
mov $8, $7
v_draw_right_loop:
call v_print
inc $5
call v_set_cursor
dec $8
cmp $8, $0
jpnz v_draw_right_loop
ret


; Function: draw_left
; Description: Draw $7 characters to the left of the cursor (initial position will also be drawn)
; Input: $7 = number of characters to draw
; Side effects: $8 is modified, cursor is moved
v_draw_left:
mov $8, $7
v_draw_left_loop:
call v_print
dec $5
call v_set_cursor
dec $8
cmp $8, $0
jpnz v_draw_left_loop
ret


; Function: draw_up
; Description: Draw $7 characters above the cursor (initial position will also be drawn)
; Input: $7 = number of characters to draw
; Side effects: $8 is modified, cursor is moved
v_draw_up:
mov $8, $7
v_draw_up_loop:
call v_print
dec $6
call v_set_cursor
dec $8
cmp $8, $0
jpnz v_draw_up_loop
ret


; Function: draw_down
; Description: Draw $7 characters below the cursor (initial position will also be drawn)
; Input: $7 = number of characters to draw
; Side effects: $8 is modified, cursor is moved
v_draw_down:
mov $8, $7
v_draw_down_loop:
call v_print
inc $6
call v_set_cursor
dec $8
cmp $8, $0
jpnz v_draw_down_loop
ret


; Function: draw_square
; Description: Draw a square with sides of length $7, starting at the cursor (top left corner)
; Input: $7 = side length
; Side effects: $8 is modified
v_draw_square:
dec $7
call v_draw_right
call v_draw_down
call v_draw_left
call v_draw_up
inc $7
ret
