def encrypt(pt):
    rshift_1 = [0x00] + pt
    rshift_2 = [0x00] + rshift_1
    #print('pwd:', pt)

    xor = [a^b for (a,b) in zip(rshift_1, rshift_2)]
    #print('xor:', xor)

    ct = [(a+b) for (a,b) in zip(xor, rshift_2)][1:]
    #print('ct: ', ct)
    return ct

# Wrong paintext password
password = [0x49, 0x5f, 0x77, 0x61, 0x6e, 0x74, 0x5f, 0x6d, 0x79, 0x5f, 0x63, 0x6f, 0x66, 0x66, 0x65, 0x65]
print('Wrong password:')
print('PT:', ''.join([chr(c) for c in password]))
ct = encrypt(password)
print('CT:', ct)

# Ciphered password h8
h8 = [0x49, 0x5f, 0x87, 0x8d, 0x70, 0x88, 0x9f, 0x91, 0x81, 0x9f, 0x9b, 0x6f, 0x78, 0x66, 0x69, 0x65]
print('h8:', h8)
if ct == h8:
    print('Encryption match with h8!')
else:
    assert()
print()

def decrypt(ct):
    pt = ct[:2]; rshift_1 = [0x00] + pt
    l = len(ct)
    for i in range(2,l):
        x = (ct[i] - rshift_1[i])
        c = (rshift_1[i] ^ x)%128
        pt.append(c); rshift_1.append(c)
        #print(i, ct[i], rshift_1[i], x, c, pt)
        #print(pt, '{' + ''.join([chr(c) for c in pt]) + '}')
    return pt
    #s = ''.join([chr(c%128) for c in pt])
    #print(pt, s, len(s))
    #return s

# Now we need to revert this for the real ciphered password, from the paper:
ct = [0x49, 0xb7, 0x71, 0x9f, 0x90, 0xcc, 0x74, 0x9f, 0xca, 0xa4, 0x64, 0xb9, 0x83, 0x7a, 0x9e, 0x5e]
#ct = [0x49, 0x5f, 0x87, 0x8d, 0x70, 0x88, 0x9f, 0x91, 0x81, 0x9f, 0x9b, 0x6f, 0x78, 0x66, 0x69, 0x65]
print('Encrypted password:')
print('CT', [c for c in ct])
pt = decrypt(ct)
#print('PT:', pt)

pwd = "I'm_n0t_4Dd1ct^^"
test = [ord(c) for c in pwd]
enc = encrypt(list(test))
print('pt', test)
print('ct', enc)
if enc == ct:
    print('Encryption match with g7!')
else:
    assert()

print(pwd)
