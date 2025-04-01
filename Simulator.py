registers = [i for i in range(32)]# 32 registers
memory = [0] * 1024   # word-addressable memory
pc = 0  # program counter

def update_pc(offset=4):
    global pc
    pc += offset

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    if (value & sign_bit) != 0:
        extended_value = value - (1 << bits)
    else:
        extended_value = value
    return extended_value

# convert instruction to list MSB to LSB
def list_maker(instruction):
    bits = []
    for i in range(31, -1, -1):
        bit = (instruction >> i) & 1
        bits.append(bit)
    return bits


# Convert list to integer MSB to LSB
def int_maker(bits):
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value

# Extract fields from the bit array
def extract_fields(instruction):
    opcode_bits = instruction[25:32]
    rd_bits = instruction[20:25]
    func3_bits = instruction[17:20]
    rs1_bits = instruction[12:17]
    rs2_bits = instruction[7:12]
    func7_bits = instruction[0:7]

    opcode = int_maker(opcode_bits)
    rd = int_maker(rd_bits)
    func3 = int_maker(func3_bits)
    rs1 = int_maker(rs1_bits)
    rs2 = int_maker(rs2_bits)
    func7 = int_maker(func7_bits)

    imm_I_bits = instruction[0:12]
    imm_S_bits = instruction[0:7] + instruction[20:25]
    imm_B_bits = [instruction[0]] + [instruction[24]] + instruction[1:7] + instruction[20:24] + [0]
    imm_J_bits = [instruction[0]] + instruction[12:20] + [instruction[11]] + instruction[1:11] + [0]

    imm_I = sign_extend(int_maker(imm_I_bits), 12)
    imm_S = sign_extend(int_maker(imm_S_bits), 12)
    imm_B = sign_extend(int_maker(imm_B_bits), 13)
    imm_J = sign_extend(int_maker(imm_J_bits), 21)

    return opcode, rd, func3, rs1, rs2, func7, imm_I, imm_S, imm_B, imm_J


def get_instruction(memory):
    global pc
    index = pc // 4
    instruction = memory[index]
    instruction_bits = list_maker(instruction)
    return instruction_bits

def execute(bits):
    global pc
    opcode, rd, func3, rs1, rs2, func7, imm_I, imm_S, imm_B, imm_J = extract_fields(bits)

    if opcode == 0b0110011:  # R-Type
        if func3 == 0b000 and func7 == 0b0000000:  # ADD
            registers[rd] = registers[rs1] + registers[rs2]
        elif func3 == 0b000 and func7 == 0b0100000:  # SUB
            registers[rd] = registers[rs1] - registers[rs2]
        elif func3 == 0b010 and func7 == 0b0000000:  # SLT
            registers[rd] = int(registers[rs1] < registers[rs2])
        elif func3 == 0b101 and func7 == 0b0000000:  # SRL
            registers[rd] = registers[rs1] >> registers[rs2]
        elif func3 == 0b110 and func7 == 0b0000000:  # OR
            registers[rd] = registers[rs1] | registers[rs2]
        elif func3 == 0b111 and func7 == 0b0000000:  # AND
            registers[rd] = registers[rs1] & registers[rs2]
        update_pc()

    elif opcode == 0b0010011:  # ADDI (I-Type)
        registers[rd] = registers[rs1] + imm_I
        update_pc()

    elif opcode == 0b0000011 and func3 == 0b010:  # LW (I-Type)
        registers[rd] = memory[(registers[rs1] + imm_I) // 4]
        update_pc()

    elif opcode == 0b1100111 and func3 == 0b000:  # JALR (I-Type)
        registers[rd] = pc + 4
        pc = (registers[rs1] + imm_I) & ~1
        return True

    elif opcode == 0b0100011 and func3 == 0b010:  # SW (S-Type)
        memory[(registers[rs1] + imm_S) // 4] = registers[rs2]
        update_pc()

    elif opcode == 0b1100011:  # B-Type
        if func3 == 0b000:  # BEQ
            if registers[rs1] == registers[rs2]:
                update_pc(imm_B)
            else:
                update_pc()
        elif func3 == 0b001:  # BNE
            if registers[rs1] != registers[rs2]:
                update_pc(imm_B)
            else:
                update_pc()

    elif opcode == 0b1111111:  # HALT
        return False
    registers[0] = 0  # x0 always stays 0
    return True

def run(memory):
    global pc
    while True:
        instruction_bits = get_instruction(memory)
        if not execute(instruction_bits):
            break