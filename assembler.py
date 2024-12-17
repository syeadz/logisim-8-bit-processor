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
    "CMP": {
        "instructions": ["MOV $temp, {rN}", "SUB $temp, {rM}"],
        "format": Format.OP_R_R,
    },
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
    "ANDI": {
        "instructions": ["LWI $temp, {imm}", "AND {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "ORI": {
        "instructions": ["LWI $temp, {imm}", "OR {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "XORI": {
        "instructions": ["LWI $temp, {imm}", "XOR {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "ADDI": {
        "instructions": ["LWI $temp, {imm}", "ADD {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "ADCI": {
        "instructions": ["LWI $temp, {imm}", "ADC {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "SUBI": {
        "instructions": ["LWI $temp, {imm}", "SUB {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "SBCI": {
        "instructions": ["LWI $temp, {imm}", "SBC {rN}, $temp"],
        "format": Format.OP_R_I,
    },
    "CLR": {"instructions": ["MOV {rN}, $zero"], "format": Format.OP_R},
}


REG_MAP = {
    "$zero": "0",
    "$one": "1",
    "$temp": "2",
    "$sp": "3",
}


SYMBOL_TABLE = dict()

LABEL_TABLE = dict()

instruction_count = 0


# First pass to expand macros and store labels
def first_pass(lines: list[str]) -> list[str]:
    expanded_lines = []

    pc = 3  # we always have 3 instructions at the start
    expanded_lines.append("lwi $one, 1")
    expanded_lines.append("lwi $sp, 30")  # stack pointer points at before last
    expanded_lines.append("goto main")

    ind = 0
    while ind < len(lines):
        line_original = lines[ind]
        ind += 1

        line = line_original.strip()  # Remove extra spaces or newline characters
        if line.startswith("#define"):
            parts = line.split()
            SYMBOL_TABLE[parts[1]] = parts[2]
        if line.startswith("#include"):
            file_name = line.split()[1]
            lines = handle_include(file_name, lines, lines.index(line_original))
        if (
            not line or line.startswith("#") or line.startswith(";")
        ):  # Skip empty lines or comments
            continue
        mnemonic, operands = parse_line(line)

        if len(operands) == 1 and operands[0]:
            if operands[0] in SYMBOL_TABLE:
                operands[0] = SYMBOL_TABLE[operands[0]]
                line = f"{mnemonic} {operands[0]}"
        if len(operands) == 2:
            if operands[0] in SYMBOL_TABLE:
                operands[0] = SYMBOL_TABLE[operands[0]]
                line = f"{mnemonic} {operands[0]}, {operands[1]}"
            if operands[1] in SYMBOL_TABLE:
                operands[1] = SYMBOL_TABLE[operands[1]]
                line = f"{mnemonic} {operands[0]}, {operands[1]}"

        if mnemonic in MACRO_SET:  # Check if the mnemonic is a macro
            if mnemonic == "HALT":  # HALT, write pc
                expanded_lines.append(f"goto {pc}")
                continue
            macro_expansion = expand_macro(mnemonic, operands)
            for expansion in macro_expansion:
                expanded_lines.append(expansion)
                pc += 1
        if mnemonic in INSTRUCTION_SET:
            expanded_lines.append(line)
            pc += 1
        if mnemonic.endswith(":"):
            LABEL_TABLE[mnemonic.strip(":")] = pc

    if "MAIN" not in LABEL_TABLE:
        raise ValueError("No main label found in the program")
    return expanded_lines


# Handle include directive
def handle_include(file_name: str, lines: list[str], line_index: int) -> list[str]:
    try:
        with open(file_name, "r") as f:
            included_lines = f.readlines()
        # Insert included lines into the current lines
        if len(lines) == line_index + 1:
            return lines + included_lines
        else:
            return lines[:line_index] + included_lines + lines[line_index + 1 :]
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_name}")


# Parse the line into mnemonic and operands
def parse_line(line: str) -> tuple[str, list[str]]:
    parts = line.split()
    mnemonic = parts[0].upper()
    operands = [operand.strip(",") for operand in parts[1:3]]
    for ind, operand in enumerate(operands):
        if operand in REG_MAP:
            operands[ind] = REG_MAP[operand]
    return mnemonic, operands


# Expand the macro into a list of instructions
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
        rN = operands[0].removeprefix("$")
        rM = operands[1].removeprefix("$")
        for instruction in instructions:
            instruction = instruction.format(rN=rN, rM=rM)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_R:
        rN = operands[0].removeprefix("$")
        for instruction in instructions:
            instruction = instruction.format(rN=rN)
            mnemonic, operands = parse_line(instruction)
            if mnemonic in MACRO_SET:
                expansion_list = expansion_list + expand_macro(mnemonic, operands)
            else:
                expansion_list.append(instruction)
    elif instr_type == Format.OP_R_I:
        rN = operands[0].removeprefix("$")
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


# Assemble the instruction into binary
def assemble_instruction(mnemonic, operands) -> str:
    if mnemonic not in INSTRUCTION_SET:
        raise ValueError(f"Unknown mnemonic: {mnemonic}")
    instr = INSTRUCTION_SET[mnemonic]
    opcode = instr["opcode"]
    instr_type = instr["format"]

    if instr_type == Format.OP_DEST:
        dest = None
        if operands[0].upper() in LABEL_TABLE:
            dest = LABEL_TABLE[operands[0].upper()]
        else:
            dest = literal_eval(operands[0])
        binary = opcode + f"{dest:010b}"
    elif instr_type == Format.OP_R_R:
        rN = operands[0].removeprefix("$")
        rM = operands[1].removeprefix("$")
        binary = opcode + f"{int(rM):04b}" + f"{int(rN):04b}"
    elif instr_type == Format.OP_R:
        rN = operands[0].removeprefix("$")
        binary = opcode + f"{int(rN):08b}"
    elif instr_type == Format.OP_R_I:
        rN = operands[0].removeprefix("$")
        binary = opcode + f"{literal_eval(operands[1]):08b}" + f"{int(rN):04b}"
    elif instr_type == Format.OP_SYS:
        binary = opcode + "00000000"
    else:
        raise ValueError(f"Unsupported instruction format: {instr_type}")

    global instruction_count
    instruction_count += 1
    # Add padding to make it 16 bits
    padded_binary = f"00{binary}"
    return padded_binary


# Convert binary string to hex
def binary_to_hex(binary_str: str) -> str:
    return f"{int(binary_str, 2):04x}"


if __name__ == "__main__":
    # Read the input file
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "main.asm"

    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = f"{file_name[:-4]}.hex"

    with open(file_name, "r") as file:
        lines = file.readlines()

    # First pass to expand macros and store labels
    expanded_lines = first_pass(lines)

    count = 0
    # Second pass to assemble the instructions and write to the output file
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
            hex_instruction = binary_to_hex(binary)
            f.write(f"{hex_instruction} ")
            # todo: replace label name with address
            print(f"{count}:\t{binary[:2]} {binary[2:]}\t{line.split('#', 1)[0]}")
            count += 1

    # Print the number of instructions and the percentage of total memory used
    percentage = "{:.1%}".format(instruction_count / 1024)
    print(
        f"Number of instructions: {instruction_count} ({percentage} of total memory)."
    )
