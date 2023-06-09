# Counter range
N = 8

# ROMs
A = 2 * [0x45de459c, 0x3db7a9ba, 0xabb7b7ae, 0xa7b449ae]
B = 2 * [0xc9bd6b8b, 0xef13cb56, 0xbdfbb9da, 0xc96d31fb]

# Helper function to get 15lsb from 32bit
def low(w):
    return w & 0x0000ffff

# Helper function to get 15hsb from 32bit
def high(w):
    return (w & 0xffff0000) >> 16

# Left / Right MUX and combined output
L = [low(B[0]), high(B[1]), high(B[2]), low(B[3]), high(B[4]), high(A[5]), high(A[6]), high(B[7])]
R = [high(A[0]), low(A[1]), low(A[2]), high(A[3]), low(A[4]), low(B[5]), low(B[6]), low(A[7])]
M = [(l << 16) | r for (l, r) in zip(L, R)]

def get_bit(v, b):
    return (v >> b) & 1

def set_bit(v, b):
    return v | (1 << b)

def clear_bit(v, b):
    return v & ~(1 << b)

# NAND
def nand(a, b):
    out = a
    for i in range(32):
        x = get_bit(a, i)
        y = get_bit(b, i)
        if x == 1 and y == 1:
            out = clear_bit(out, i)
        else:
            out = set_bit(out, i)
    return out

# Blackbox: 3 times the same block of 5 NAND gates
def blackbox(r, i):
    d1 = nand(r,r); d2 = nand(i,i); d3 = nand(d1,d2); d4 = nand(r,i); d5 = nand(d3,d4)
    b1 = nand(nand(d1,d2),d4)
    b2 = nand(nand(nand(b1,b1),nand(i,i)),nand(b1,i))
    b3 = nand(nand(nand(b2,b2),nand(i,i)),nand(b2,i))
    return b3

def circuit(count, i):
    return blackbox(M[count], i)

# Expected output: Un_c
un_c_l = [0b01011110, 0b10001010, 0b00000100, 0b10001100]
un_c = (un_c_l[0] << 24) | (un_c_l[1] << 16) |(un_c_l[2] << 8) | (un_c_l[3])

# Now we search for an input i such that:
# > circuit(count, i) == un_c

# Blackbox is involutive (reverse is itself)
# So to get input i, we simply apply it to the expected output un_c
for count in range(N):
    i = circuit(count, un_c)
    print(count, '{:032b}'.format(i))

#0 1100.1010 1111.1110 1011.1110 1010.1101 => Un_cHIFFrA9e_A55e2_bi3n_d3PreCie
#1 0100.1110 0110.0110 0101.0010 1100.1001
#2 0001.1100 1000.1110 0100.1100 1101.1101
#3 1001.0000 1000.1110 0101.1100 1100.0111
#4 0110.1000 1100.1000 1011.1110 1110.1111
#5 1001.1100 1100.0010 0011.0000 0010.0101
#6 0000.1010 1100.0010 0100.0010 1010.1001
#7 0110.1000 0001.1000 1011.0010 1101.1101



