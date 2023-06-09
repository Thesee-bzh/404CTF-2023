from pwn import *
import itertools
from sage.all import *

target = remote('challenges.404ctf.fr', 31682)

#Bienvenue dans loracle, qui chiffre ce que vous rentrez. Vous devez dechiffrer : pvfdhtuwgbpxfhocidqcznupamzsezp
line = target.recvline(); print(line.decode())
ct   = line.split()[-1:][0].decode()
secret = ct

# Lets input small variations on input to see the effect on the output
wlists = list()
for pos in range(31):
    wlist = list()
    for i in range(26):
        c = chr(ord('a') + i)
        w = list('a'*31)
        w[pos] = c
        wlist.append(''.join(w))
    wlists.append(wlist)

def oracle(wlist):
    clist = list()
    for w in wlist:
        #message en clair : a
        #message chiffre  : aaaaa
        q = b'message en clair : '
        target.recvuntil(q); #print(q.decode())
        target.send(w.encode() + b'\n')
        line = target.recvline(); #print(line.decode())
        if b'message chiffre' not in line:
            assert()
        ct = line.split()[-1:][0].decode()
        clist.append(ct)
        print(w, ct)
    return clist

clists = list()
for l in wlists:
    clists.append(oracle(l))
#print(wlists)

def get_transform(clist, size):
    dlist = list()
    # loop on characters in block
    for i in range(0, size):
        # loop on encrypted blocks
        for j in range(len(clist)-1):
            w1 = clist[j]; w2 = clist[j+1]
            diff = (ord(w2[i]) - ord(w1[i])) % 26
            # Make sure we have a constant difference
            if j != 0 and diff != delta:
                assert()
            delta = diff
        dlist.append(delta)
    return(dlist)

def get_transfrom_matrix(clist, size):
    m = list()
    for l in clist:
        t = get_transform(l, size)
        m.append(t)
    return m

# Get the transformation matrix
transform = get_transfrom_matrix(clists, 31)
A = Matrix(transform)

""" Output
A = matrix([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  1,  2,  3,  4,  5],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  1,  2,  3,  4,  4],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  1,  2,  3,  3,  3],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  1,  2,  2,  2,  2],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  1,  1,  1,  1,  1],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,  0,  0,  0,  0,  0,  0],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 25, 25, 25, 25, 25, 25],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 24, 24, 24, 24, 24, 24, 24],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9],
            [1, 2, 3, 4, 5, 6, 7, 8, 8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8],
            [1, 2, 3, 4, 5, 6, 7, 7, 7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7],
            [1, 2, 3, 4, 5, 6, 6, 6, 6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6],
            [1, 2, 3, 4, 5, 5, 5, 5, 5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5],
            [1, 2, 3, 4, 4, 4, 4, 4, 4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4],
            [1, 2, 3, 3, 3, 3, 3, 3, 3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3],
            [1, 2, 2, 2, 2, 2, 2, 2, 2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]])
"""
print('Matrix A')
print(A)

# We have: t(A)*x = y, so x = (t(A))^-1 * y
# So we need to ranspose and inverse A
T = A.transpose()
I = T.inverse()

def encrypt1(block):
    x = vector([(ord(c) - ord('a'))%26 for c in block])
    y = T*x
    enc = ''.join([chr(i%26 + ord('a')) for i in y])
    #print(block, x, y, enc)
    return enc

# Check out matrix with one value
# pt = 'aayaaaaaaaaaaaaaaaaaaaaaaaaaaaa'; ct = 'ermzdautlcenazhaycsvsybvjkgtbhm'
# if encrypt1(pt) != ct:
#     assert()
# => Doesn't work...

# Maybe there's an offset vector, like so: Y = t(A)*X + B
# Let's calculate if using a sample
x = 'aaaaaaaaaaaaaaaaaaaalaaaaaaaaaa'; y = 'rrzzqahtycrcrscxxdvazhmiybzoyej'
ax = encrypt1(x)
v = [(ord(y[j]) - ord(ax[j]))%26 for j in range(31)]
B = vector(v)
print('Vector B')
print(B)

def decrypt(block):
    y = vector([(ord(c) - ord('a'))%26 for c in block])
    x = I*(y - B)
    dec = ''.join([chr(i%26 + ord('a')) for i in x])
    #print(block, y, x, dec)
    return dec

def encrypt(block):
    x = vector([(ord(c) - ord('a'))%26 for c in block])
    y = T*x + B
    enc = ''.join([chr(i%26 + ord('a')) for i in y])
    #print(block, x, y, enc)
    return enc

# Check out matrixes now
pt = 'aayaaaaaaaaaaaaaaaaaaaaaaaaaaaa'; ct = 'ermzdautlcenazhaycsvsybvjkgtbhm'
if encrypt(pt) != ct:
     assert()

print('Flag')
print(decrypt(secret))
