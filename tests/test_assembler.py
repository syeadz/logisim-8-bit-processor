import unittest

from assembler import assemble_instruction

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
