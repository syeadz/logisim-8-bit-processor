# 8-bit Processor in Logisim

8-bit single-cycle processor based on the very simple 8-bit processor design from the University of Valladolid which can be seen here: https://www.deeper.uva.es/pages/spg/docs/Conferences/FPGAworld2006a.pdf, created in logisim and with VHDL and Verilog implementations.

Some changes were made to simplify the design and instruction set, notably there are no interrupts and port addressing is limited. Other than that, most of the instruction set has been implemented. There is also an assembler written in Python that can convert assembly instructions to hex code that can be loaded into the ROM on Logisim, allowing you to run programs within Logisim and see how the processor works in real time.

## Memory addressing

* 8-bit memory addresses, first 5 bits for RAM, last 3 bits for specific memory ports [xxx][y yyyy]
* Can store 8-bit words to RAM locations 0x00 to 0x1E
* 8 memory locations are mapped to ports. These ports are linked to different devices and registers in the logisim design.
  * Port 0 (BCD0 Register): 0x1F
  * Port 1 (BCD1 Register): 0x3F
  * Port 2 (BCD2 Register): 0x5F
  * Port 3 (Terminal Input): 0x7F
  * Port 4 (Unused): 0x9F
  * Port 5 (Video X register): 0xBF
  * Port 6 (Video Y register): 0xDF
  * Port 7 (Video Color Input): 0xFF

## Logisim Ports

In the Logisim circuit, you have access to 3 BCDs, 1 Terminal, and 1 128 x 128 Video Output with Atari 2600 color palette (7 bits).

* Bit 7 in terminal input clears the terminal, and bit 7 in video color input clears the video output.

## Limitations

* No interrupts
* Can only store to ram locations 0x00 to 0x1E
