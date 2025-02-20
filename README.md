# CO-Assignment
This is our Co-Project Assignment
In this we have made a working assembler fot R,I,B,J,S type instructions
Our group has the following people - 
    1. Anoushka Malik - 2024086
    2. Cho Hnin Lwin - 2024165
    3. Parth Kumar - 2024404
    4. Naman Chug - 2024363
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

f_ans = [] 
with open(input_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:
    for output in f_ans:
        file.write(output + '\n')

Registers = {
    "zero": "00000",
    "ra": "00001",  
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

B_type = {
    "beq": {"opcode": "1100011", "funct3": "000"},
    "bne": {"opcode": "1100011", "funct3": "001"},
}

S_Type = {
        "sw": {"opcode": "0100011", "funct3": "010"}
}

R_Type = {
        "add": {"opcode": "0110011", "funct3": "000", "funct7": "0000000"},
        "sub": {"opcode": "0110011", "funct3": "000", "funct7": "0100000"},
        "slt": {"opcode": "0110011", "funct3": "010", "funct7": "0000000"},
        "srl": {"opcode": "0110011", "funct3": "101", "funct7": "0000000"},
        "or": {"opcode": "0110011", "funct3": "110", "funct7": "0000000"},
        "and": {"opcode": "0110011", "funct3": "111", "funct7": "0000000"}

}

I_Type = {
        "lw": {"opcode": "0000011", "funct3": "010"},
        "addi": {"opcode": "0010011", "funct3": "000"},
        "jalr": {"opcode": "1100111", "funct3": "000"}
}

def funct1(a: str, b: str) -> str: #2's complement
    s = []
    carry = 0
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 or j >= 0 or carry:
        if i >= 0:
            carry += int(a[i])
            i -= 1
        if j >= 0:
            carry += int(b[j])
            j -= 1
        s.append(str(carry % 2))
        carry //= 2
    return ''.join(reversed(s))


def funct2(lines): #parse_mips
    labels = {}
    for idx, line in enumerate(lines, 1):
        if ':' in line:
            label = line.split(':')[0].strip()
            labels[label] = idx
    return labels


def funct3(lines): #remove labels
    l = []
    for line in lines:
        if ':' in line:
            label, statement = line.split(':', 1)
            l.append(statement.strip())
        else:
            l.append(line.strip())
    return l


with open(input_file, 'r') as file:
    lines = file.readlines()
