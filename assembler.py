import sys
from enum import Enum
from ast import literal_eval


class Format(Enum):
    OP_DEST = (1,)
    OP_R_R = (2,)
    OP_R = (3,)
    OP_R_I = (4,)
    OP_SYS = (5,)


INSTRUCTION_SET = {
    # Load/Store
    "SW": {"opcode": "001100", "format": Format.OP_R_R},
    "LWI": {"opcode": "10", "format": Format.OP_R_I},
    "LW": {"opcode": "111100", "format": Format.OP_R_R},
    "MOV": {"opcode": "110000", "format": Format.OP_R_R},
    # Arithmetic
    "XNOR": {"opcode": "110001", "format": Format.OP_R_R},
    "OR": {"opcode": "110010", "format": Format.OP_R_R},
    "AND": {"opcode": "110011", "format": Format.OP_R_R},
    "ADD": {"opcode": "110100", "format": Format.OP_R_R},
    "ADC": {"opcode": "110101", "format": Format.OP_R_R},
    "SUB": {"opcode": "110110", "format": Format.OP_R_R},
    "SBC": {"opcode": "110111", "format": Format.OP_R_R},
    "ASR": {"opcode": "111000", "format": Format.OP_R},
    "RRC": {"opcode": "111001", "format": Format.OP_R},
    "ROR": {"opcode": "111010", "format": Format.OP_R},
    "ROL": {"opcode": "111011", "format": Format.OP_R},
    # Jump
    "CALL": {"opcode": "0000", "format": Format.OP_DEST},
    "GOTO": {"opcode": "0001", "format": Format.OP_DEST},
    "JPZ": {"opcode": "0100", "format": Format.OP_DEST},
    "JPNZ": {"opcode": "0101", "format": Format.OP_DEST},
    "JPC": {"opcode": "0110", "format": Format.OP_DEST},
    "JPNC": {"opcode": "0111", "format": Format.OP_DEST},
    # System
    "RET": {"opcode": "001000", "format": Format.OP_SYS},
}


MACRO_SET = {
    "NOP": {"instructions": ["ADD $zero, $zero"], "format": Format.OP_SYS},
    "INC": {"instructions": ["ADD {rN}, $one"], "format": Format.OP_R},
    "DEC": {"instructions": ["SUB {rN}, $one"], "format": Format.OP_R},
    "NOT": {"instructions": ["XNOR {rN}, $zero"], "format": Format.OP_R},
    "NEG": {"instructions": ["NOT {rN}", "INC {rN}"], "format": Format.OP_R},
    "XOR": {"instructions": ["XNOR {rN}, {rM}", "NOT {rN}"], "format": Format.OP_R_R},
    "CMP": {"instructions": ["MOV $temp, {rN}", "SUB $temp, {rM}"], "format": Format.OP_R_R},
    "SETC": {"instructions": ["LWI $temp, 0xFF", "INC $temp"], "format": Format.OP_SYS},
    "CLRC": {"instructions": ["ADD $zero, $zero"], "format": Format.OP_SYS},
    "RLC": {"instructions": ["ADC {rN}, {rN}"], "format": Format.OP_R},
    "SL0": {"instructions": ["ADD {rN}, {rN}"], "format": Format.OP_R},
    "SL1": {"instructions": ["ADD {rN}, {rN}", "INC {rN}"], "format": Format.OP_R},
    "SR0": {"instructions": ["CLRC", "RLC {rN}"], "format": Format.OP_R},
    "SR1": {"instructions": ["SETC", "RRC {rN}"], "format": Format.OP_R},
    "PUSH": {"instructions": ["SW $sp, {rN}", "INC $sp"], "format": Format.OP_R},
    "POP": {"instructions": ["DEC $sp", "LW {rN}, $sp"], "format": Format.OP_R},
    "HALT": {},
    "ANDI": {"instructions": ["LWI $temp, {imm}", "AND {rN}, $temp"], "format": Format.OP_R_I},
    "ORI": {"instructions": ["LWI $temp, {imm}", "OR {rN}, $temp"], "format": Format.OP_R_I},
    "XORI": {"instructions": ["LWI $temp, {imm}", "XOR {rN}, $temp"], "format": Format.OP_R_I},
    "ADDI": {"instructions": ["LWI $temp, {imm}", "ADD {rN}, $temp"], "format": Format.OP_R_I},
    "ADCI": {"instructions": ["LWI $temp, {imm}", "ADC {rN}, $temp"], "format": Format.OP_R_I},
    "SUBI": {"instructions": ["LWI $temp, {imm}", "SUB {rN}, $temp"], "format": Format.OP_R_I},
    "SBCI": {"instructions": ["LWI $temp, {imm}", "SBC {rN}, $temp"], "format": Format.OP_R_I},
    "CLR": {"instructions": ["MOV {rN}, $zero"], "format": Format.OP_R},
}


REG_MAP = {
    "$zero": 0,
    "$one": 1,
    "$temp": 2,
    "$sp": 3,
}


SYMBOL_TABLE = dict()

LABEL_TABLE = dict()

instruction_count = 0

def first_pass(lines: list[str]) -> list[str]:
    expanded_lines = []

    pc = 0
    for line in lines:
        line = line.strip()  # Remove extra spaces or newline characters
        if line.startswith("#define"):
            pass
        if line.startswith("#include"):
            pass
        if (
            not line or line.startswith("#") or line.startswith(";")
        ):  # Skip empty lines or comments
            continue
        mnemonic, operands = parse_line(line)
        if mnemonic in MACRO_SET:  # Check if the mnemonic is a macro
            if mnemonic == "HALT":  # HALT, write pc
                expanded_lines.append(f"goto {pc}")
                continue
            macro_expansion = expand_macro(mnemonic, operands)
            for expansion in macro_expansion:
                expanded_lines.append(expansion)
                pc += 1
                print(expansion)
        if mnemonic in INSTRUCTION_SET:
            expanded_lines.append(line)
            pc += 1
        if mnemonic.endswith(":"):
            SYMBOL_TABLE[mnemonic.strip(":")] = pc

    return expanded_lines


def parse_line(line: str) -> tuple[str, list[str]]:
    parts = line.split()
    mnemonic = parts[0].upper()
    operands = [operand.strip(",") for operand in parts[1:]]
    for ind, operand in enumerate(operands):
        if operand in REG_MAP:
            operands[ind] = REG_MAP[operand]
    return mnemonic, operands


def expand_macro(macro: str, operands: list[str]) -> list[str]:
    expansion_list = []
    instructions = MACRO_SET[macro]["instructions"]
    instr_type = MACRO_SET[macro]["format"]

    if instr_type == Format.OP_DEST:
        dest = operands[0]
        for instruction in instructions:
            instruction = instruction.format(dest=dest)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_R_R:
        rN = operands[0].removeprefix('$')
        rM = operands[1].removeprefix('$')
        for instruction in instructions:
            instruction = instruction.format(rN=rN, rM=rM)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_R:
        rN = operands[0].removeprefix('$')
        for instruction in instructions:
            instruction = instruction.format(rN=rN)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_R_I:
        rN = operands[0].removeprefix('$')
        imm = operands[1]
        for instruction in instructions:
            instruction = instruction.format(rN=rN, imm=imm)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_SYS:
        for instruction in instructions:
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    else:
        raise ValueError(f"Unsupported instruction format: {instr_type}")

    return expansion_list


def assemble_instruction(mnemonic, operands) -> str:
    if mnemonic not in INSTRUCTION_SET:
        raise ValueError(f"Unknown mnemonic: {mnemonic}")
    instr = INSTRUCTION_SET[mnemonic]
    opcode = instr["opcode"]
    instr_type = instr["format"]

    if instr_type == Format.OP_DEST:
        dest = None
        if operands[0].upper() in SYMBOL_TABLE:
            dest = SYMBOL_TABLE[operands[0].upper()]
        else:
            dest = literal_eval(operands[0])
        binary = opcode + f"{dest:010b}"
    elif instr_type == Format.OP_R_R:
        binary = opcode + f"{int(operands[1][1:]):04b}" + f"{int(operands[0][1:]):04b}"
    elif instr_type == Format.OP_R:
        binary = opcode + f"{int(operands[0][1:]):08b}"
    elif instr_type == Format.OP_R_I:
        binary = (
            opcode + f"{literal_eval(operands[1]):08b}" + f"{int(operands[0][1:]):04b}"
        )
    elif instr_type == Format.OP_SYS:
        binary = opcode + "00000000"
    else:
        raise ValueError(f"Unsupported instruction format: {instr_type}")

    global instruction_count
    instruction_count += 1
    # Add padding to make it 16 bits
    padded_binary = f"00{binary}"
    return padded_binary


def binary_to_hex(binary_str: str) -> str:
    return f"{int(binary_str, 2):04x}"


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "arith.asm"

    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{file_name[:-4]}.hex"

    with open(file_name, "r") as file:
        lines = file.readlines()

    expanded_lines = first_pass(lines)

    with open(output_file, "w") as f:
        f.write("v2.0 raw\n")  # Write the hex file header
        for line in expanded_lines:
            line = line.strip()  # Remove extra spaces or newline characters
            if (
                not line or line.startswith("#") or line.startswith(";")
            ):  # Skip empty lines or comments
                continue
            mnemonic, operands = parse_line(line)
            if mnemonic.endswith(":"):
                continue
            binary = assemble_instruction(mnemonic, operands)
            print(binary)
            hex_instruction = binary_to_hex(binary)
            f.write(f"{hex_instruction} ")

    percentage = "{:.1%}".format(instruction_count / 1024)
    print(
        f"Number of instructions: {instruction_count} ({percentage} of total memory)."
    )
