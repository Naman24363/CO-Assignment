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