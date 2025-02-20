    # R-Type Instruction
    elif data.split()[0] in R_Type:
        opcode = R_Type[data.split()[0]]["opcode"]
        funct3 = R_Type[data.split()[0]]["funct3"]
        funct7 = R_Type[data.split()[0]]["funct7"]
        data = data.replace(",", " ")

        if data.split()[2] not in Registers or data.split()[1] not in Registers or data.split()[3] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = funct7 + Registers[data.split()[3]] + Registers[data.split()[2]] + funct3 + Registers[data.split()[1]] + opcode
        f_ans.append(output)

        # I-Type Instruction
    elif data.split()[0] in I_Type:
        opcode = I_Type[data.split()[0]]["opcode"]
        funct3 = I_Type[data.split()[0]]["funct3"]
        data = data.replace(",", " ")

        if len(data.split()) == 3:
            input_str = data.split()[2]
            opening_index = input_str.find('(')
            number_string = input_str[:opening_index]
            decimal = int(number_string)
            opening_index = input_str.find('(')
            closing_index = input_str.find(')')
            fin_reg = input_str[opening_index + 1:closing_index]
        else:
            decimal = int(data.split()[3])
            fin_reg = data.split()[2]

        if decimal < 0:
            bina = bin(abs(decimal))[2:].zfill(12)
            bina = bina.replace("0", "X").replace("1", "0").replace("X", "1")
            result = funct1(bina, "1")
            imm = result
        else:
            imm = bin(decimal)[2:].zfill(12)

        if fin_reg not in Registers or data.split()[1] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = imm + Registers[fin_reg] + funct3 + Registers[data.split()[1]] + opcode
        f_ans.append(output)
    