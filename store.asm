lwi $0, 5 # load 5 into register 0
lwi $3, 0x00 # write to ram at address 0
sw  $3, $0 # write $0 to address 0

lwi $1, 10 # load 10 into register 1
lwi $0, 0x01 # load write to ram at address 1 
sw $0, $1 # write $1 to address 1
