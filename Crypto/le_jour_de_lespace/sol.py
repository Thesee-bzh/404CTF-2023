from pwn import *
import itertools
from sage.all import *

c = remote('challenges.404ctf.fr', 31451)

#bienvenue dans loracle. Le message a dechiffrer est : ueomaspblbppadgidtfn
line = c.recvline(); print(line.decode())
ct   = line.split()[-1:][0].decode()

# Data blocks of size=5 are ciphered independantly
n = 5
chunks = [ct[i:i+n] for i in range(0, len(ct), n)]

# Lets input small variations on blocks of size=5 to see the effect on the output:
wlist1 = ['aaaaa','baaaa','caaaa','daaaa','eaaaa']
wlist2 = ['aaaaa','abaaa','acaaa','adaaa','aeaaa']
wlist3 = ['aaaaa','aabaa','aacaa','aadaa','aaeaa']
wlist4 = ['aaaaa','aaaba','aaaca','aaada','aaaea']
wlist5 = ['aaaaa','aaaab','aaaac','aaaad','aaaae']
wlists = [wlist1, wlist2, wlist3, wlist4, wlist5]

def oracle(wlist):
    clist = list()
    for w in wlist:
        #message en clair : a
        #message chiffre  : aaaaa
        q = b'message en clair : '
        c.recvuntil(q); #print(q.decode())
        c.send(w.encode() + b'\n')
        line = c.recvline(); #print(line.decode())
        if b'message chiffre' not in line:
            assert()
        ct = line.split()[-1:][0].decode()
        clist.append(ct)
    return clist

for l in wlists:
    print(l, oracle(l))

# Output:
clist1 = ['aaaaa','jlfnt','swkbn','cipoh','ltucb']
clist2 = ['aaaaa','eagov','iamdr','masrn','qaygj']
clist3 = ['aaaaa','schpw','leoft','egvuq','widkn']
clist4 = ['aaaaa','ubkqx','pcuhv','kdfxt','fepor']
clist5 = ['aaaaa','idmry','qgyjx','yjlbw','hmxsv']

clists = [clist1, clist2, clist3, clist4, clist5]

def get_transform(clist):
    dlist = list()
    # loop on characters in block
    for i in range(0, 5):
        # loop on encrypted blocks
        for j in range(len(clist)-1):
            w1 = clist[j]; w2 = clist[j+1]
            diff = (ord(w2[i]) - ord(w1[i])) % 25
            # Make sure we have a constant difference
            if j != 0 and diff != delta:
                assert()
            delta = diff
        dlist.append(delta)
    return(dlist)

def get_transfrom_matrix(clist):
    m = list()
    for l in clist:
        t = get_transform(l)
        m.append(t)
    return m

# Get the transformation matrix
transform = get_transfrom_matrix(clists)
A = Matrix(transform)
print(A)

# Output:
# [ 9 11  5 13 19]
# [ 4  0  6 14 21]
# [18  2  7 15 22]
# [20  1 10 16 23]
# [ 8  3 12 17 24]

# We have: t(A)*x = y, so x = (t(A))^-1 * y
# So we need to ranspose and inverse A
T = A.transpose()
I = T.inverse()

def encrypt(block):
    x = vector([(ord(c) - ord('a'))%25 for c in block])
    y = T*x
    enc = ''.join([chr(i%25 + ord('a')) for i in y])
    #print(block, x, y, enc)
    return enc

def decrypt(block):
    y = vector([(ord(c) - ord('a'))%25 for c in block])
    x = I*y
    dec = ''.join([chr(i%25 + ord('a')) for i in x])
    #print(block, y, x, dec)
    return dec

def flag(chunks):
    dec = list()
    for chunk in chunks:
        x  = decrypt(chunk)
        x_ = encrypt(x)
        if x_ != chunk:
            assert()
        dec.append(x)
    return ''.join([w for w in dec])

print(flag(chunks))
