#This is our Assembler
#This is for R,S,I,J,B type instructions


import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

f_ans = [] 
with open(input_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:
    for output in f_ans:
        file.write(output + '\n')