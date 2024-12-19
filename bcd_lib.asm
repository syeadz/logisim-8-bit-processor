; BCD Library

#define b_bcd0_addr 0x1F
#define b_bcd1_addr 0x3F
#define b_bcd2_addr 0x5F
#define b_bcd3_addr 0x9F


; Function: bcd0_display
; Description: Display the value in $7 in BCD0
; Inputs: $7 - value to display
b_bcd0_display:
    lwi $2, b_bcd0_addr
    sw $2, $7
    ret

; Function: bcd1_display
; Description: Display the value in $7 in BCD1
; Inputs: $7 - value to display
b_bcd1_display:
    lwi $2, b_bcd1_addr
    sw $2, $7
    ret

; Function: bcd2_display
; Description: Display the value in $7 in BCD2
; Inputs: $7 - value to display
b_bcd2_display:
    lwi $2, b_bcd2_addr
    sw $2, $7
    ret

; Function: bcd3_display
; Description: Display the value in $7 in BCD3
; Inputs: $7 - value to display
b_bcd3_display:
    lwi $2, b_bcd3_addr
    sw $2, $7
    ret
