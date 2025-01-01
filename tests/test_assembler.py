import unittest

from assembler import assemble_instruction, expand_macro

pf = "00"


class TestAssembleInstruction(unittest.TestCase):
    def test_call(self):
        mnemonic = "CALL"
        operands = ["0x335"]
        expected = pf + "00001100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_goto(self):
        mnemonic = "GOTO"
        operands = ["0x335"]
        expected = pf + "00011100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_return(self):
        mnemonic = "RET"
        operands = []
        expected = pf + "00100000000000"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_sw(self):
        mnemonic = "SW"
        operands = ["$1", "$2"]
        expected = pf + "00110000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_jpz(self):
        mnemonic = "JPZ"
        operands = ["0x335"]
        expected = pf + "01001100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_jpnz(self):
        mnemonic = "JPNZ"
        operands = ["0x335"]
        expected = pf + "01011100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_jpc(self):
        mnemonic = "JPC"
        operands = ["0x335"]
        expected = pf + "01101100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_jpnc(self):
        mnemonic = "JPNC"
        operands = ["0x335"]
        expected = pf + "01111100110101"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_lwi(self):
        mnemonic = "LWI"
        operands = ["$1", "0x2D5"]
        expected = pf + "1010110101010001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_mov(self):
        mnemonic = "MOV"
        operands = ["$1", "$2"]
        expected = pf + "11000000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_xnor(self):
        mnemonic = "XNOR"
        operands = ["$1", "$2"]
        expected = pf + "11000100100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_or(self):
        mnemonic = "OR"
        operands = ["$1", "$2"]
        expected = pf + "11001000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_and(self):
        mnemonic = "AND"
        operands = ["$1", "$2"]
        expected = pf + "11001100100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_add(self):
        mnemonic = "ADD"
        operands = ["$1", "$2"]
        expected = pf + "11010000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_adc(self):
        mnemonic = "ADC"
        operands = ["$1", "$2"]
        expected = pf + "11010100100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_sub(self):
        mnemonic = "SUB"
        operands = ["$1", "$2"]
        expected = pf + "11011000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_sbc(self):
        mnemonic = "SBC"
        operands = ["$1", "$2"]
        expected = pf + "11011100100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_asr(self):
        mnemonic = "ASR"
        operands = ["$1"]
        expected = pf + "11100000000001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_rrc(self):
        mnemonic = "RRC"
        operands = ["$1"]
        expected = pf + "11100100000001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_ror(self):
        mnemonic = "ROR"
        operands = ["$1"]
        expected = pf + "11101000000001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_rol(self):
        mnemonic = "ROL"
        operands = ["$1"]
        expected = pf + "11101100000001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    def test_lw(self):
        mnemonic = "LW"
        operands = ["$1", "$2"]
        expected = pf + "11110000100001"
        self.assertEqual(assemble_instruction(mnemonic, operands), expected)

    # macro instructions

    def test_nop(self):
        mnemonic = "NOP"
        operands = []
        expected = ["ADD $zero, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_inc(self):
        mnemonic = "INC"
        operands = ["$1"]
        expected = ["ADD $1, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_dec(self):
        mnemonic = "DEC"
        operands = ["$1"]
        expected = ["SUB $1, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_not(self):
        mnemonic = "NOT"
        operands = ["$1"]
        expected = ["XNOR $1, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_neg(self):
        mnemonic = "NEG"
        operands = ["$1"]
        expected = ["XNOR $1, $zero", "ADD $1, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_xor(self):
        mnemonic = "XOR"
        operands = ["$1", "$2"]
        expected = ["XNOR $1, $2", "XNOR $1, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_cmp(self):
        mnemonic = "CMP"
        operands = ["$1", "$2"]
        expected = ["MOV $temp, $1", "SUB $temp, $2"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_setc(self):
        mnemonic = "SETC"
        operands = []
        expected = ["LWI $temp, 0xFF", "ADD $2, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_clrc(self):
        mnemonic = "CLRC"
        operands = []
        expected = ["ADD $zero, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_rlc(self):
        mnemonic = "RLC"
        operands = ["$1"]
        expected = ["ADC $1, $1"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_sl0(self):
        mnemonic = "SL0"
        operands = ["$1"]
        expected = ["ADD $1, $1"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_sl1(self):
        mnemonic = "SL1"
        operands = ["$1"]
        expected = ["ADD $1, $1", "ADD $1, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_sr0(self):
        mnemonic = "SR0"
        operands = ["$1"]
        expected = ["ADD $zero, $zero", "ADC $1, $1"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_sr1(self):
        mnemonic = "SR1"
        operands = ["$1"]
        expected = ["LWI $temp, 0xFF", "ADD $2, $one", "RRC $1"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_push(self):
        mnemonic = "PUSH"
        operands = ["$1"]
        expected = ["SW $sp, $1", "SUB $3, $one"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_pop(self):
        mnemonic = "POP"
        operands = ["$1"]
        expected = ["ADD $3, $one", "LW $1, $sp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_andi(self):
        mnemonic = "ANDI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "AND $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_ori(self):
        mnemonic = "ORI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "OR $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_xori(self):
        mnemonic = "XORI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "XNOR $1, $2", "XNOR $1, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_addi(self):
        mnemonic = "ADDI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "ADD $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_adci(self):
        mnemonic = "ADCI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "ADC $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_subi(self):
        mnemonic = "SUBI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "SUB $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_sbci(self):
        mnemonic = "SBCI"
        operands = ["$1", "0x2D5"]
        expected = ["LWI $temp, 0x2D5", "SBC $1, $temp"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)

    def test_clr(self):
        mnemonic = "CLR"
        operands = ["$1"]
        expected = ["MOV $1, $zero"]
        self.assertEqual(expand_macro(mnemonic, operands), expected)
