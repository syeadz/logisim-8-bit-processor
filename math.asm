; Showcase for math library
; Will mutiply 5 by 3 and display the result in BCD3
; Will divide 17 by 5 and display the result in BCD1,
; with remainder in BCD0

#include math_lib.asm

main:
; Multiplication
lwi $5, 5
lwi $6, 3
call m_mul8

lwi $2, 0x9F
sw $2, $7

; Division
lwi $5, 17
lwi $6, 5
call m_div8

lwi $2, 0x3F
sw $2, $7
lwi $2, 0x1F
sw $2, $5
halt