goto main

test:
    lwi $3, 0x2f # set write port to bcd1 port
main:
    lwi $3, 0x2f # set write port to bcd1 port
    goto 3