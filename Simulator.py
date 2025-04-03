import sys
r = [0] * 32
r[2] = 380

def funct1(dec):
    """Convert decimal to uppercase hexadecimal without '0x' prefix"""
    map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    if dec == 0:
        return '0'
    h = ''
    while dec > 0:
        rem = dec % 16
        if rem < 10:
            h = str(rem) + h
        else:
            h = map[rem] + h
        dec = dec // 16
    return h

def Print_mem():
    start = 65536  
    for i in range(32):
        addr = start + 4 * i
        addr2= funct1(addr) 
        mem_key = addr2.upper()
        val = memory.get(mem_key, 0)
        line = f"0x000{addr2}:0b{twos(val)}\n"
        file.write(line)
        
        
        
def Type_R(I):
    funct7 = I[:7]
    rs2 = int(I[7:12], 2)
    rs1 = int(I[12:17], 2)
    funct3 = I[17:20]
    rd = int(I[20:25], 2)
    if funct7 == "0000000": 
        if funct3 == "000":
            r[rd] = r[rs1] + r[rs2]
        elif funct3 == "010":  
            r[rd] = 1 if r[rs1] < r[rs2] else 0
        elif funct3 == "101": #slt
            sh= r[rs2] & 0b11111
            r[rd] = r[rs1] >>sh
        elif funct3 == "110": 
            r[rd] = r[rs1] | r[rs2]
        elif funct3 == "111": 
            r[rd] = r[rs1] & r[rs2]


    elif funct7 == "0100000":
        if funct3 == "000":
            if (rs1 == 0):
              r[rd] = 0 - r[rs2]
            else:
              r[rd] = r[rs1] - r[rs2]
        else:
          print("Invalid Instruction")

def Load(I):
    rs1 = int(I[-20:-15], 2)
    rd = int(I[-12:-7], 2)
    imm = I[:-20]
    immf=funct4(imm)
    funct3 = I[-15:-12]
    if funct3 == "010": #lw
        offset=immf+r[(rs1)]
        offi=hex(offset)
        r[rd]=memory[offi[2:]]

def Type_I(I):
    opcode = I[-7:]
    rs1 = int(I[-20:-15], 2)
    rd = int(I[-12:-7], 2)
    imm = I[:-20]
    funct3 = I[-15:-12]
    if opcode == "0010011": 
        if funct3 == "000":  
            r[rd] = r[rs1] + funct8(imm)
        elif funct3 == "011": 
            if int(str(funct5(r[rs1])), 2) < int(imm, 2):
                r[rd] = 1

    elif opcode == "1100111": 
        if funct3 == "000":
            immd = funct8(imm) #imm_dec
            target = (r[rs1] + immd) & ~1 
            r[rd] = x["PC"] + 4  
            x["PC"] = target-4
            return

def Type_B(I):
    if(I[-32:-7]=="0"*25):
        return x["PC"]
    imm = I[-32] + I[-8] + I[-31:-25] + I[-12:-8]
    rs1 = int(I[-20:-15], 2)
    rs2 = int(I[-25:-20], 2)
    funct3 = I[-15:-12]
    if funct3 == "000": 
        if r[rs1] == r[rs2]:
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4
    elif funct3 == "001": 
        if r[rs1] != r[rs2]:
           
            x["PC"] += funct8(imm[-12:]+"0")
       
            x["PC"]-=4
    elif funct3 == "100": 
        if r[rs1] < r[rs2]:
            x["PC"] += funct8(imm[-12:]+"10")
            x["PC"]-=4
    elif funct3 == "101":  
        if r[rs1] >= r[rs2]:
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4

    elif funct3 == "110": 
        if int(str(funct5(r[rs1])), 2) < int(str(funct5(r[rs2])), 2):
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4
    elif funct3== "111":  
        if int(str(funct5(r[rs1])), 2) >= int(str(funct5(r[rs2])), 2):
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4

def Type_S(I):

    imm1 = I[-32:-25]
    imm2 = I[-12:-7]
    imm = imm1 + imm2  
    rs2 = int(I[-25:-20], 2)
    rs1 = int(I[-20:-15], 2)
    immf=funct4(imm)
    funct3 = I[-15:-12]
    if funct3 == "010":
        offset=immf+r[rs1]
        memory[funct1(offset)] = r[rs2]

file = open(sys.argv[2], "w")
# file = open("output.txt", "w")
    
def Print_reg():
        file.write(db(x["PC"], 32) + " ")
        for i in range(32):
            ans = db(r[i], 32)
            file.write(ans + " ") 
        file.write("\n")


def Type_J(I):
    imm = I[0] + I[12:20] + I[11] + I[1:11]
    
    rd = int(I[20:25], 2) 
    r[rd] = x["PC"] + 4 
    x["PC"] =x["PC"]+funct8(imm+"0")
    x["PC"]-=4
 
# f = open("input.txt", "r")
f = open(sys.argv[1], "r") 
machine_code = f.read().splitlines()
max_pc = len(machine_code)*4
while x["PC"] < max_pc:
    # print(memory)
    I = machine_code[int(x["PC"]/4)]
    opcode = I[-7:]
    # print(opcode)
    
    # print(instruction)
    if  I == "00000000000000000000000001100011":
        break
    if opcode == "0110011":
        Type_R(I)
    elif opcode == "0000011":
        Load(I)
        # x["PC"]+=4
    elif opcode == "0010011" or opcode == "1100111":
        Type_I(I)
    elif opcode == "0100011":
        # print(opcode)
        Type_S(I)
        # print('s')
        # x["PC"]+=4
    elif opcode == "1100011":
        Type_B(I)
        
    elif opcode == "1101111":
        Type_J(I)
        
    elif I == "11100110000000000000000000000000":  # halt
        print("Program halted.")

    else:
        print("Invalid instruction")
    r[0] = 0
    x["PC"] += 4
    Print_reg()
Print_reg()
file.close()