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
    # Arithmetic
    "ADD": {"opcode": "110100", "format": Format.OP_R_R},
    "SUB": {"opcode": "110110", "format": Format.OP_R_R},
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

SYMBOL_TABLE = dict()

instruction_count = 0


def generate_symbol_table(lines: list[str]):
    pc = 0
    for line in lines:
        line = line.strip()  # Remove extra spaces or newline characters
        if not line or line.startswith("#") or line.startswith(";"):  # Skip empty lines or comments
            continue
        mnemonic, _ = parse_line(line)
        if mnemonic in INSTRUCTION_SET:
            pc += 1
        if mnemonic.endswith(':'):
            SYMBOL_TABLE[mnemonic.strip(':')] = pc
            

def parse_line(line: str) -> tuple[str, list[str]]:
    parts = line.split()
    mnemonic = parts[0].upper()
    operands = [operand.strip(",") for operand in parts[1:]]
    return mnemonic, operands


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
        binary = opcode + operands[0][:0]  # Placeholder logic, adjust as needed
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
        file_name = "labels.asm"

    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = "labels.hex"

    with open(file_name, "r") as file:
        lines = file.readlines()

    generate_symbol_table(lines)

    with open(output_file, "w") as f:
        f.write("v2.0 raw\n")  # Write the hex file header
        for line in lines:
            line = line.strip()  # Remove extra spaces or newline characters
            if not line or line.startswith("#") or line.startswith(";"):  # Skip empty lines or comments
                continue
            mnemonic, operands = parse_line(line)
            if mnemonic.endswith(':'):
                continue
            binary = assemble_instruction(mnemonic, operands)
            print(binary)
            hex_instruction = binary_to_hex(binary)
            f.write(f"{hex_instruction} ")

    percentage = "{:.1%}".format(instruction_count/1000)
    print(f"Number of instructions: {instruction_count} ({percentage} of total memory).")