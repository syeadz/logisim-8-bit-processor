lwi $0, 5 # load 5 into register 0
lwi $1, 10 # load 10 into register 1

lwi $3, 0x1f # set write port to bcd0 port
sw  $3, $0 # write $0 to bcd0 port
lwi $3, 0x2f # set write port to bcd1 port
sw  $3, $1 # write $1 to bcd1 port

add $0, $1 # $0 = $0 + $1

lwi $3, 0x4f # set write port to bcd2 port
sw  $3, $0 # write $0 to bcd2 port

lwi $3, 0x6f # set write port to terminal port
lwi $0, 72 # H
sw  $3, $0 # write to terminal port

lwi $0, 101 # e
sw  $3, $0

lwi $0, 108 # l
sw  $3, $0

lwi $0, 108 # l
sw  $3, $0

lwi $0, 111 # o
sw  $3, $0

lwi $0, 44 # ,
sw $3, $0

lwi $0, 32 # space
sw $3, $0

lwi $0, 87 # W
sw  $3, $0

lwi $0, 111 # o
sw  $3, $0

lwi $0, 114 # r
sw  $3, $0

lwi $0, 108 # l
sw  $3, $0

lwi $0, 100 # d
sw  $3, $0

lwi $0, 33 # !
sw  $3, $0

lwi $0, 10 # newline
sw  $3, $0

lwi $0, 58 # :
sw  $3, $0

lwi $0, 41 # )
sw  $3, $0

lwi $0, 0 # null
sw  $3, $0

goto 44 # infinite loop