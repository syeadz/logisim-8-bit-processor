; Seven Segment Library

#define s_seg0_addr 0x1F
#define s_seg1_addr 0x3F
#define s_seg2_addr 0x5F
#define s_seg3_addr 0x9F


; Function: seg0_display
; Description: Display the value in $7 in SEG0
; Inputs: $7 - value to display
s_seg0_display:
    lwi $2, s_seg0_addr
    sw $2, $7
    ret

; Function: seg1_display
; Description: Display the value in $7 in SEG1
; Inputs: $7 - value to display
s_seg1_display:
    lwi $2, s_seg1_addr
    sw $2, $7
    ret

; Function: seg2_display
; Description: Display the value in $7 in SEG2
; Inputs: $7 - value to display
s_seg2_display:
    lwi $2, s_seg2_addr
    sw $2, $7
    ret

; Function: seg3_display
; Description: Display the value in $7 in SEG3
; Inputs: $7 - value to display
s_seg3_display:
    lwi $2, s_seg3_addr
    sw $2, $7
    ret
