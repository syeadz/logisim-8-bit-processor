; Math library
; has functions for 8-bit multiplication and division, and 16-bit addition and subtraction

; Function: mul8
; Description: Multiply two non-negative 8-bit numbers
; Input: $5 = multiplicand, $6 = multiplier
; Output: $7 = result
; Side effects: $6 is modified
m_mul8:
clr $7
cmp $0, $5
jpZ m_ret_0
cmp $0, $6
jpZ m_ret_0
# todo: check which number is smaller, use that as counter
m_mul8_loop:
cmp $0, $6
jpZ m_ret
add $7, $5
dec $6
goto m_mul8_loop


; Function: div8
; Description: Divide two non-negative 8-bit numbers
; Input: $5 = dividend, $6 = divisor
; Output: $7 = result, $5 = remainder
; Note: does not handle divide by 0 errors, returns as 0
m_div8:
clr $7
cmp $0, $5
jpZ m_ret_0
cmp $0, $6
jpZ m_ret_0
m_div8_loop:
; dividend < divisor, so return
cmp $5, $6
jpC m_ret
sub $5, $6
inc $7
; division complete, return
cmp $5, $0
jpZ m_ret
goto m_div8_loop


; Set return value to 0 and return
m_ret_0:
lwi $7, 0
ret

; Return
m_ret:
ret
