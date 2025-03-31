registers = [0] * 32  #32 registers
memory = [0] * 1024   #word addressable memory

#code of the program counter
pc = 0
def update_pc(offset=4):
    global pc
    pc += offset

# Sign-extend a value with the given number of bits
# this is for imm_I, imm_S, and imm_B
# to convert the immediate value to a signed integer
def sign_extend(value, bits):
    if value & (1 << (bits - 1)):
        value -= (1 << bits)
    return value


#extract diffrent bits of information from 32 bit instruction
def extract_fields(instruction):
    opcode = instruction & 0x7F          # 0-6
    rd = (instruction >> 7) & 0x1F       # 7-11
    func3 = (instruction >> 12) & 0x07   # 12-14
    rs1 = (instruction >> 15) & 0x1F     # 15-19
    rs2 = (instruction >> 20) & 0x1F     # 20-24
    func7 = (instruction >> 25) & 0x7F   # 25-31

    imm_I = sign_extend((instruction >> 20) & 0xFFF, 12)  
    imm_S = sign_extend(((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F), 12)  
    imm_B = sign_extend(((instruction >> 31) << 12) | ((instruction >> 7) & 0x1E) | 
                        ((instruction >> 25) & 0x3F) << 5 | ((instruction >> 8) & 0x01) << 11, 13)

    imm_J = sign_extend(((instruction >> 31) << 20) | ((instruction >> 12) & 0xFF) << 12 |
                        ((instruction >> 20) & 0x1) << 11 | ((instruction >> 21) & 0x3FF) << 1, 21)

    return opcode, rd, func3, rs1, rs2, func7, imm_I, imm_S, imm_B, imm_J



#function to fetch the instruction from memory
def get_instruction(memory):
        global pc
        instruction = memory[pc // 4]
        return instruction



#function to execute the 32 bit instruction
def execute(instruction):
    global pc
    opcode, rd, func3, rs1, rs2, func7, imm_I, imm_S, imm_B = extract_fields(instruction)

    # R-Type Instructions
    if opcode == 0b0110011:
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

    # I-Type Instructions
    elif opcode == 0b0010011:  # ADDI
        registers[rd] = registers[rs1] + imm_I
        update_pc()
    
    elif opcode == 0b0000011 and func3 == 0b010:  # LW
        registers[rd] = memory[(registers[rs1] + imm_I) // 4]  # Load from memory
        update_pc()
    
    elif opcode == 0b1100111 and func3 == 0b000:  # JALR
        registers[rd] = pc + 4
        pc = (registers[rs1] + imm_I) & ~1  #PC is even
        return True  #no increment in pc

    # S-Type Instruction
    elif opcode == 0b0100011 and func3 == 0b010:  # SW
        memory[(registers[rs1] + imm_S) // 4] = registers[rs2]
        update_pc()

    # B-Type Instructions
    elif opcode == 0b1100011:
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

    # HALT
    elif opcode == 0b1111111:
        return False  

    return True

#function to run the simulator
def run(memory):
    global pc
    while True:
        current_instruction = get_instruction(memory)
        if not execute(current_instruction):
            break